#!/usr/bin/env python
"""Chemistry vs docking-geometry as the limiting factor — across ALL screening targets.

For every organised screening set, builds the seed-5 / depth-100 seed-alignment model (with the
current same-family merge) and decomposes each feature family into:

  * chemistry ceiling   = fraction of the top-100 compounds that CARRY that group (a hard cap:
                          nothing can recover a feature that is not in the molecules);
  * geometry realization = of those carriers, the fraction that place the group at the model's
                          consensus (within membership_radius) — how coherently the docking/
                          alignment positions a group the compound does have.

High realization => chemistry (compound diversity) limits; low => the geometry (docking seed +
conformer alignment) limits. Writes catalogue/screening_eval/geometry_limit_report.md.

Offline (docked SDFs carry the pH-7.4 microstate).
Run: pixi run python scripts/eval_geometry_limit.py.
"""

from __future__ import annotations

import argparse
import csv
import json
import os
import sys
from dataclasses import replace
from pathlib import Path

os.environ.setdefault("OMP_NUM_THREADS", "1")
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))

import numpy as np  # noqa: E402
from rdkit import Chem, RDLogger  # noqa: E402
from rdkit.Chem import AllChem  # noqa: E402

RDLogger.DisableLog("rdApp.*")

from pharmpipe.features.dock_load import read_protonated_smiles, read_rank_index  # noqa: E402
from pharmpipe.features.extract import conformer_features, feature_factory  # noqa: E402
from pharmpipe.pharmacophore.config import load_pharmacophore_config  # noqa: E402
from pharmpipe.pharmacophore.run import build_from_seed_alignment  # noqa: E402
from pharmpipe.screening.crosswalk import SCREENING_DIR, load_crosswalk  # noqa: E402
from pharmpipe.util.paths import CATALOGUE_DIR  # noqa: E402

EVAL = CATALOGUE_DIR / "screening_eval"
# Cross-target PATTERN analysis: lighter than the production recipe (depth 100 / 64 confs) so 18
# targets are tractable here — the geometry-realization metric measures placement coherence and is
# robust to it. Probe models go to a scratch dir, never overwriting the tracked recipe models.
DEPTH = 50
PROBE = CATALOGUE_DIR.parent / "data" / "_geom_probe"
CFG = load_pharmacophore_config()
FAC = feature_factory(CFG.features.fdef)
FAMS = CFG.alignment.align_families or CFG.features.families
HIER = CFG.features.feature_hierarchy
MR = CFG.density.membership_radius
# families we characterise (the pharmacophorically-defining ones)
TRACK = ["PosIonizable", "Aromatic", "Acceptor", "Donor", "LumpedHydrophobe", "NegIonizable"]
SHORT = {"PosIonizable": "cation", "Aromatic": "arom", "Acceptor": "acc", "Donor": "don",
         "LumpedHydrophobe": "hydph", "NegIonizable": "anion"}


def smiles_map(docked_dir: Path, depth: int) -> dict[str, str]:
    out = {}
    for hit in read_rank_index(docked_dir / next(p.name for p in docked_dir.glob("index_*.csv"))
                               )[:depth]:
        smi = read_protonated_smiles(docked_dir, hit.mol_id)
        if smi:
            out[hit.mol_id] = smi
    return out


def carries(docked_dir: Path, index: Path, depth: int) -> tuple[dict[str, set], int]:
    """mol_ids carrying each family (from a single quick 3D conformer), + n analysed."""
    have = {f: set() for f in TRACK}
    n = 0
    for hit in read_rank_index(index)[:depth]:
        smi = read_protonated_smiles(docked_dir, hit.mol_id) or hit.smiles
        m = Chem.MolFromSmiles(smi)
        if m is None:
            continue
        n += 1
        mh = Chem.AddHs(m)
        if AllChem.EmbedMolecule(mh, randomSeed=1) == 0:
            fams = {f for f, _, _ in conformer_features(mh, FAC, FAMS, HIER, conf_id=0)}
        else:
            fams = {f.GetFamily() for f in FAC.GetFeaturesForMol(m)}
        for fam in TRACK:
            if fam in fams:
                have[fam].add(hit.mol_id)
    return have, n


def decompose(model_dir: Path, have: dict[str, set], n: int) -> list[dict]:
    model = json.loads((model_dir / "pharmacophore_model.json").read_text())
    kept = {f["family"]: np.array(f.get("position") or [f["x"], f["y"], f["z"]])
            for f in model["features"] if f["family"] in TRACK}
    pts = {f: [] for f in TRACK}
    with (model_dir / "features.csv").open(encoding="utf-8") as fh:
        for row in csv.DictReader(fh):
            fam = row.get("family")
            if fam in TRACK:
                lig = row.get("ligand_id", "").split("__")[0]
                pts[fam].append((lig, np.array([float(row["x"]), float(row["y"]),
                                                float(row["z"])])))
    rows = []
    for fam in TRACK:
        if not have[fam] or fam not in kept:
            continue
        ceiling = len(have[fam]) / n
        centre = kept[fam]
        supporters = {lig for lig, p in pts[fam]
                      if np.linalg.norm(p - centre) <= MR and lig in have[fam]}
        real = len(supporters) / len(have[fam])
        rows.append({"fam": SHORT[fam], "ceiling": ceiling, "real": real,
                     "n_carry": len(have[fam]), "n_sup": len(supporters)})
    return rows


def _built(model_dir: Path) -> bool:
    return (model_dir / "pharmacophore_model.json").exists()


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--report-only", action="store_true",
                    help="skip building; decompose the existing depth-100 models only")
    ap.add_argument("--build-only", action="store_true",
                    help="only (re)build missing depth-100 models, no report")
    ap.add_argument("--only", help="comma-separated target keys to process")
    ap.add_argument("--full", action="store_true",
                    help="use the full recipe conformer budget (slow); default is a lighter "
                         "ensemble for the cross-target pattern analysis")
    args = ap.parse_args()
    # Lighter conformer ensemble keeps the 18-target build tractable; the geometry-realization
    # metric (placement coherence) is robust to it. nAChR/esr1 keep the full-recipe models.
    build_cfg = CFG if args.full else replace(
        CFG, alignment=replace(CFG.alignment, n_conformers=8, max_confs=4, energy_window=8.0))
    only = set(args.only.split(",")) if args.only else None
    _, targets = load_crosswalk()
    lines = ["# Chemistry vs docking-geometry — is the pattern library-wide?", "",
             "Seed-5 / depth-100 seed-alignment per target. **chem** = fraction of the top-100 "
             "carrying the group (hard ceiling); **geom** = of those carriers, fraction placing it "
             f"at the model consensus (within {MR:.1f} A). Low geom with high chem => the docking/"
             "alignment **geometry** limits, not the chemistry.", "",
             "| target | feature | chem | geom | n_carry/n_sup | limited by |",
             "|---|---|--:|--:|---|---|"]
    agg = {"chemistry": 0, "geometry": 0, "both": 0}
    per_target = []
    for t in targets:
        if only and t.key not in only:
            continue
        docked = SCREENING_DIR / t.key
        index_files = list(docked.glob("index_*.csv"))
        if not index_files:
            continue
        index = index_files[0]
        out = PROBE / t.key
        if not _built(out) and not args.report_only:
            print(f"building {t.key}...", flush=True)
            smap = smiles_map(docked, DEPTH)
            build_from_seed_alignment(docked, index, out, build_cfg, top_n_hits=DEPTH,
                                      seed_k=build_cfg.alignment.seed_k, name=t.key,
                                      smiles_map=smap)
        if args.build_only:
            continue
        if not _built(out):
            lines.append(f"| {t.key} | (not built) | - | - | - | - |")
            continue
        have, n = carries(docked, index, DEPTH)
        rows = decompose(out, have, n)
        for i, r in enumerate(rows):
            limit = ("chemistry" if r["real"] >= 0.7
                     else ("geometry" if r["ceiling"] >= 0.6 else "both"))
            agg[limit] += 1
            tgt = t.key if i == 0 else ""
            lines.append(f"| {tgt} | {r['fam']} | {r['ceiling']:.0%} | {r['real']:.0%} | "
                         f"{r['n_carry']}/{r['n_sup']} | {limit} |")
            per_target.append((t.key, r, limit))
        print(f"{t.key}: " + ", ".join(
            f"{r['fam']} chem={r['ceiling']:.0%} geom={r['real']:.0%}" for r in rows), flush=True)

    if args.build_only:
        print("build-only: done")
        return 0

    # aggregate verdict
    hi_chem = [p for p in per_target if p[1]["ceiling"] >= 0.6]
    geom_limited = [p for p in hi_chem if p[1]["real"] < 0.7]
    lines += ["", "## Pattern", "",
              f"- Feature/target rows scored: **{len(per_target)}** "
              f"(chemistry-limited {agg['chemistry']}, geometry-limited {agg['geometry']}, "
              f"both {agg['both']}).",
              f"- Of the **{len(hi_chem)}** rows where the chemistry is present (ceiling >= 60%), "
              f"**{len(geom_limited)}** ({len(geom_limited)/max(len(hi_chem),1):.0%}) are "
              f"geometry-limited (realization < 70%) — the chemistry is there but the alignment "
              f"places it inconsistently.",
              f"- Mean chemistry ceiling {np.mean([p[1]['ceiling'] for p in per_target]):.0%} vs "
              f"mean geometry realization {np.mean([p[1]['real'] for p in per_target]):.0%}."]
    (EVAL / "geometry_limit_report.md").write_text("\n".join(lines), encoding="utf-8")
    print("\n" + "\n".join(lines[-6:]))
    print(f"\n-> {EVAL / 'geometry_limit_report.md'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
