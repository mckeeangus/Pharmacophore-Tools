#!/usr/bin/env python
"""Does 'the seed is not necessary' generalise beyond nAChR?

For every screening target that has a built known-actives model (the crystal-derived ground
truth), build the feature-alignment model two ways from the same top-100 DrugCLIP compounds —
**docked** (top-5 docked seed) and **seedless** (top-ranked compound's energy-min conformer) —
and score each against the known-actives model by feature-family recall + frame-independent
internal geometry (`screening.compare.compare_models`). If seedless matches the known-actives as
well as the docked seed does across targets, the nAChR result (chemistry carries the geometry;
the seed is not necessary for correct geometry) generalises.

Lighter conformer budget than the production recipe so all targets are tractable here; models go
to a gitignored scratch dir, never overwriting the tracked recipe models. Resumable: a built
(target, init) is reused. Run: pixi run python scripts/seed_necessity_all.py [--only k1,k2]
[--report-only]. Writes catalogue/screening_eval/seed_necessity_report.md.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from dataclasses import replace
from pathlib import Path

os.environ.setdefault("OMP_NUM_THREADS", "1")
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))

from rdkit import RDLogger  # noqa: E402

RDLogger.DisableLog("rdApp.*")

from pharmpipe.features.dock_load import read_protonated_smiles, read_rank_index  # noqa: E402
from pharmpipe.pharmacophore.config import load_pharmacophore_config  # noqa: E402
from pharmpipe.pharmacophore.run import build_from_seed_alignment  # noqa: E402
from pharmpipe.screening.compare import compare_models, summarise  # noqa: E402
from pharmpipe.screening.crosswalk import SCREENING_DIR, load_crosswalk  # noqa: E402
from pharmpipe.util.paths import CATALOGUE_DIR, REPO_ROOT  # noqa: E402

PROBE = REPO_ROOT / "data" / "_geom_probe" / "seednec"
REPORT = CATALOGUE_DIR / "screening_eval" / "seed_necessity_report.md"
DEPTH = 100
# lighter than the recipe (64/40) so the feature-rich targets finish; the geometry metric is robust
CFG = replace(load_pharmacophore_config(),
              alignment=replace(load_pharmacophore_config().alignment,
                                n_conformers=16, max_confs=8, energy_window=10.0, em_iterations=3))


def _ka_features(slug: str, cell: str) -> list[dict] | None:
    p = CATALOGUE_DIR / slug / "pharmacophores" / cell / "pharmacophore.json"
    return json.loads(p.read_text())["features"] if p.exists() else None


def _smiles_map(docked_dir: Path, index: Path) -> dict[str, str]:
    return {h.mol_id: read_protonated_smiles(docked_dir, h.mol_id) or h.smiles
            for h in read_rank_index(index)[:DEPTH]}


def _build(key: str, init: str, docked_dir: Path, index: Path, smap: dict) -> dict | None:
    out = PROBE / key / init
    if not (out / "pharmacophore.json").exists():
        print(f"building {key}/{init}...", flush=True)
        build_from_seed_alignment(docked_dir, index, out, CFG, top_n_hits=DEPTH,
                                  seed_k=CFG.alignment.seed_k, name=f"{key}_{init}",
                                  smiles_map=smap, seedless=(init == "seedless"))
    p = out / "pharmacophore.json"
    if not p.exists():
        return None
    js = json.loads(p.read_text())
    return {"features": js["features"],
            "em": (js["metadata"]["source"].get("em_convergence") or []),
            "n_aligned": js["metadata"]["source"].get("n_aligned")}


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--only", help="comma-separated target keys")
    ap.add_argument("--report-only", action="store_true")
    ap.add_argument("--build-only", action="store_true")
    args = ap.parse_args()
    only = set(args.only.split(",")) if args.only else None

    _, targets = load_crosswalk()
    rows = []
    for t in targets:
        if t.cell is None:                       # need a known-actives ground truth
            continue
        if only and t.key not in only:
            continue
        docked_dir = SCREENING_DIR / t.key
        idxs = list(docked_dir.glob("index_*.csv"))
        ka = _ka_features(t.slug, t.cell)
        if not idxs or ka is None:
            continue
        index = idxs[0]
        smap = _smiles_map(docked_dir, index)
        ka_sum = summarise(ka)
        rec = {"key": t.key, "slug": t.slug}
        for init in ("docked", "seedless"):
            if args.report_only and not (PROBE / t.key / init / "pharmacophore.json").exists():
                rec[init] = None
                continue
            try:
                b = _build(t.key, init, docked_dir, index, smap)
            except Exception as e:  # noqa: BLE001
                print(f"  {t.key}/{init} FAILED: {e}", flush=True)
                b = None
            if b is None:
                rec[init] = None
                continue
            c = compare_models(summarise(b["features"]), ka_sum)
            rec[init] = {"verdict": c.verdict, "recall": round(c.family_recall, 2),
                         "geom": round(c.mean_geom_delta, 2) if c.mean_geom_delta is not None
                         else None, "n_aligned": b["n_aligned"], "em": len(b["em"])}
        rows.append(rec)
        if not args.build_only:
            print(f"{t.key}: docked={rec.get('docked')} seedless={rec.get('seedless')}", flush=True)

    if args.build_only:
        print("build-only: done")
        return 0

    lines = ["# Does 'the seed is not necessary' generalise? — docked vs seedless per target", "",
             "Both inits built from the same top-100 DrugCLIP compounds, scored vs the "
             "**known-actives** model (crystal-derived ground truth) by family recall + "
             "frame-independent internal geometry (mean pairwise-distance delta, A). If seedless "
             "matches the known-actives as well as the docked seed, chemistry alone suffices.", "",
             "| target | docked recall | docked geomD | seedless recall | seedless geomD | seedless ~ docked? |",  # noqa: E501
             "|---|--:|--:|--:|--:|:--:|"]
    persists = 0
    scored = 0
    for r in rows:
        d, s = r.get("docked"), r.get("seedless")
        if not d or not s:
            lines.append(f"| {r['key']} | {'-' if not d else d['recall']} | "
                         f"{'-' if not d else d['geom']} | {'-' if not s else s['recall']} | "
                         f"{'-' if not s else s['geom']} | (incomplete) |")
            continue
        scored += 1
        # seedless "as good as" docked: recall >= docked's and geometry no worse by > 0.75 A
        ok = (s["recall"] >= d["recall"] - 1e-9
              and (s["geom"] is None or d["geom"] is None or s["geom"] <= d["geom"] + 0.75))
        persists += ok
        lines.append(f"| {r['key']} | {d['recall']} | {d['geom']} | {s['recall']} | {s['geom']} "
                     f"| {'YES' if ok else 'no'} |")
    lines += ["", "## Verdict", "",
              f"- Targets scored (both inits built): **{scored}**; seedless matches or beats the "
              f"docked seed vs ground truth in **{persists}/{scored}**.",
              "- If this fraction is high, the nAChR finding generalises: **a docked/crystal seed "
              "is not necessary for correct geometry** — the shared rigid cores carry it, and the "
              "seed at most speeds convergence. Where seedless underperforms, note whether the "
              "target is flexible / lacks a rigid multi-feature core to anchor the consensus.",
              "", "Lighter conformer budget (16 embeds) for tractability; the deep full-recipe "
              "3-way (crystal/docked/seedless) result is nAChR in `seed_necessity.md`."]
    REPORT.write_text("\n".join(lines), encoding="utf-8")
    print("\n" + "\n".join(lines[-6:]))
    print(f"\n-> {REPORT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
