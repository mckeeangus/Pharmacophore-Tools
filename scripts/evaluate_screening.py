#!/usr/bin/env python
"""Library-wide evaluation of the DrugCLIP pharmacophore methods vs known-actives + literature.

For every organised screening set (data/screening/<key>/), builds BOTH methods —
full-docking over all docked poses (`--docked-dir` semantics) and minimum-docking seed
alignment (`--seed-docked`, at config `alignment_depth`) — into the tracked deliverable
catalogue/screening_eval/<key>/{docked,seed_align}/, then compares each model to the target's
known-actives model (where one exists) and to the literature, writing comparison_report.md +
results.json. Reuses the built modes; no new build logic. Offline (docked SDFs carry their
pH-7.4 microstate). Run: pixi run python scripts/evaluate_screening.py [--only key1,key2].
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

os.environ.setdefault("OMP_NUM_THREADS", "1")
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from rdkit import RDLogger  # noqa: E402

RDLogger.DisableLog("rdApp.*")

from pharmpipe.pharmacophore.config import load_pharmacophore_config  # noqa: E402
from pharmpipe.pharmacophore.run import (  # noqa: E402
    build_from_docked_set,
    build_from_seed_alignment,
)
from pharmpipe.screening.compare import (  # noqa: E402
    compare_models,
    compare_to_literature,
    summarise,
)
from pharmpipe.screening.crosswalk import SCREENING_DIR, load_crosswalk  # noqa: E402
from pharmpipe.screening.literature import load_literature  # noqa: E402
from pharmpipe.util.paths import CATALOGUE_DIR  # noqa: E402

EVAL_DIR = CATALOGUE_DIR / "screening_eval"
DOCKED_HITS = 1000  # "all the docked poses"


def _features(model_dir: Path) -> list[dict] | None:
    p = model_dir / "pharmacophore.json"
    return json.loads(p.read_text())["features"] if p.exists() else None


def _ka_features(slug: str, cell: str | None) -> list[dict] | None:
    if not cell:
        return None
    p = CATALOGUE_DIR / slug / "pharmacophores" / cell / "pharmacophore.json"
    return json.loads(p.read_text())["features"] if p.exists() else None


def _fam_list(summary) -> str:
    short = {"PosIonizable": "cation+", "NegIonizable": "anion-", "Aromatic": "arom",
             "Acceptor": "acc", "Donor": "don", "LumpedHydrophobe": "hydph"}
    return ", ".join(f"{short.get(f, f)}({summary.dominant[f][1]:.2f})"
                     for f in sorted(summary.dominant)) or "(none)"


def evaluate(cfg, depth, targets, literature, only, force=False) -> list[dict]:
    EVAL_DIR.mkdir(parents=True, exist_ok=True)
    results = []
    for t in targets:
        if only and t.key not in only:
            continue
        docked_dir = SCREENING_DIR / t.key
        index = docked_dir / f"index_{t.key}.csv"
        if not index.exists():
            print(f"  SKIP {t.key}: not organised ({index} missing)")
            continue
        print(f"\n=== {t.key} (slug={t.slug}, cell={t.cell}, lit={t.literature}) ===")
        rec: dict = {"key": t.key, "slug": t.slug, "cell": t.cell, "literature": t.literature,
                     "methods": {}}
        ka = _ka_features(t.slug, t.cell)
        ka_sum = summarise(ka) if ka else None
        lit = literature.get(t.literature) if t.literature else None
        for method in ("docked", "seed_align"):
            out = EVAL_DIR / t.key / method
            model = out / "pharmacophore.json"
            if force or not model.exists():       # build only when missing (resumable)
                try:
                    if method == "docked":
                        res = build_from_docked_set(
                            docked_dir, index, out, cfg, top_n_hits=DOCKED_HITS,
                            top_n_poses=1, pose_score="cnnaffinity", name=f"{t.key}/docked")
                    else:
                        res = build_from_seed_alignment(
                            docked_dir, index, out, cfg, top_n_hits=depth,
                            seed_k=cfg.alignment.seed_k, name=f"{t.key}/seed_align")
                except Exception as e:  # noqa: BLE001 — record and continue the batch
                    print(f"  {method}: FAILED ({e})")
                    rec["methods"][method] = {"error": str(e)}
                    continue
                if res is None:
                    print(f"  {method}: skipped (< min_ligands)")
                    rec["methods"][method] = {"skipped": True}
                    continue
            if not model.exists():
                rec["methods"][method] = {"skipped": True}
                continue
            js = json.loads(model.read_text())
            a = summarise(js["features"])
            n_lig = js.get("metadata", {}).get("source", {}).get("n_ligands")
            m: dict = {"n_ligands": n_lig,
                       "n_features": sum(a.counts.values()), "families": _fam_list(a)}
            if ka_sum is not None:
                c = compare_models(a, ka_sum)
                m["vs_known"] = {"verdict": c.verdict, "recall": round(c.family_recall, 2),
                                 "shared": c.shared, "missing": c.only_b, "extra": c.only_a,
                                 "geom": {k: round(v, 2) for k, v in c.geom.items()},
                                 "mean_geom_delta": (round(c.mean_geom_delta, 2)
                                                     if c.mean_geom_delta is not None else None)}
            if lit is not None:
                lc = compare_to_literature(a, lit.families)
                m["vs_literature"] = {"verdict": lc.verdict, "recall": round(lc.recall, 2),
                                      "recovered": lc.recovered, "missing": lc.missing,
                                      "extra": lc.extra, "citation": lit.citation}
            rec["methods"][method] = m
            kv = m.get("vs_known", {}).get("verdict", "-")
            lv = m.get("vs_literature", {}).get("verdict", "-")
            print(f"  {method:<10} {m['n_features']}feat n={m['n_ligands']}  "
                  f"vsKA={kv} vsLit={lv}  [{m['families']}]")
        results.append(rec)
    return results


def _diagnose(rec: dict) -> str:
    """Heuristic per-target diagnosis line from the comparison data."""
    d = rec["methods"].get("docked", {})
    s = rec["methods"].get("seed_align", {})
    notes = []
    if isinstance(d, dict) and d.get("n_features") == 1 and isinstance(s, dict) \
            and (s.get("n_features") or 0) >= 2:
        notes.append("full-docking over all poses diluted to 1 feature; seed-align (top slice) "
                     "richer — dilution, not method failure")
    for label, m in (("docked", d), ("seed_align", s)):
        vk = m.get("vs_known") if isinstance(m, dict) else None
        if vk and vk.get("missing"):
            notes.append(f"{label} missing vs known: {', '.join(vk['missing'])}")
        gd = vk.get("mean_geom_delta") if vk else None
        if gd is not None and gd > 1.5:
            notes.append(f"{label} geometry off known by {gd} A mean")
    if isinstance(s, dict) and s.get("skipped"):
        notes.append("seed-align skipped (too few aligned — conformer/clique coverage)")
    return "; ".join(notes) or "families + geometry broadly consistent"


def write_report(results, depth) -> Path:
    lines = ["# DrugCLIP screening — pharmacophore evaluation vs known-actives + literature", "",
             f"Two methods per target: **docked** (full-docking consensus over all "
             f"{DOCKED_HITS} poses) and **seed_align** (minimum-docking, top-{depth} by DrugCLIP, "
             f"seed_k=3). Verdicts: MATCH / PARTIAL / MISMATCH on feature-family recall + internal "
             "geometry (frame-independent). `vsKA` needs a built known-actives model; `vsLit` a "
             "literature entry.", "",
             "| Target | Method | Feats | Ligands | vs Known | recall | geomD | vs Lit | recall |",
             "|---|---|--:|--:|:--:|--:|--:|:--:|--:|"]
    for r in results:
        for method in ("docked", "seed_align"):
            m = r["methods"].get(method, {})
            if not isinstance(m, dict) or m.get("error") or m.get("skipped"):
                state = "ERR" if m.get("error") else "skip"
                lines.append(f"| {r['key']} | {method} | - | - | {state} | - | - | - | - |")
                continue
            vk = m.get("vs_known", {})
            vl = m.get("vs_literature", {})
            gd = vk.get("mean_geom_delta")
            lines.append(
                f"| {r['key']} | {method} | {m['n_features']} | {m['n_ligands']} | "
                f"{vk.get('verdict', '-')} | {vk.get('recall', '-')} | "
                f"{gd if gd is not None else '-'} | {vl.get('verdict', '-')} | "
                f"{vl.get('recall', '-')} |")
    lines += ["", "## Per-target diagnosis", ""]
    for r in results:
        lines.append(f"- **{r['key']}** — {_diagnose(r)}")
    lines += ["", "See each `catalogue/screening_eval/<key>/{docked,seed_align}/` for the model "
              "+ `model_summary.md`; `results.json` for the full comparison data."]
    path = EVAL_DIR / "comparison_report.md"
    path.write_text("\n".join(lines), encoding="utf-8")
    return path


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--only", help="comma-separated target keys to evaluate (default: all)")
    ap.add_argument("--depth", type=int, default=None, help="override alignment depth")
    ap.add_argument("--force", action="store_true",
                    help="rebuild models even if already present (default: reuse = resumable)")
    args = ap.parse_args(argv)

    cfg = load_pharmacophore_config()
    depth, targets = load_crosswalk()
    depth = args.depth or depth
    literature = load_literature()
    only = set(args.only.split(",")) if args.only else None

    results = evaluate(cfg, depth, targets, literature, only, force=args.force)
    EVAL_DIR.mkdir(parents=True, exist_ok=True)
    (EVAL_DIR / "results.json").write_text(json.dumps(results, indent=2), encoding="utf-8")
    report = write_report(results, depth)
    print(f"\nEvaluated {len(results)} target(s) at depth {depth} -> {report}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
