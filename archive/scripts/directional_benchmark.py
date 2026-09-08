#!/usr/bin/env python
"""Does orientation-aware matching fix the acceptor? — A/B on nAChR/5KXI.

Builds the docked-seed model (crystal frame, so absolute distances to the crystal nicotine are
meaningful) with directional matching OFF vs ON, and reports each consensus feature's absolute
distance to the crystal nicotine (NCT) atom it should sit on — cation = pyrrolidinium N2,
aromatic = pyridine centroid, acceptor = pyridine N1. If the acceptor's off-native distance drops
with directions on, the projected-point orientation term has resolved the ring-flip.

Offline. Run: pixi run python scripts/directional_benchmark.py.
Writes catalogue/screening_eval/nachr_a4b2_positive/directional_benchmark.md.
"""

from __future__ import annotations

import json
import os
import sys
from dataclasses import replace
from pathlib import Path

os.environ.setdefault("OMP_NUM_THREADS", "1")
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))

import numpy as np  # noqa: E402
from rdkit import RDLogger  # noqa: E402

RDLogger.DisableLog("rdApp.*")

from pharmpipe.features.dock_load import read_protonated_smiles, read_rank_index  # noqa: E402
from pharmpipe.pharmacophore.config import load_pharmacophore_config  # noqa: E402
from pharmpipe.pharmacophore.run import build_from_seed_alignment  # noqa: E402
from pharmpipe.util.paths import CATALOGUE_DIR, REPO_ROOT  # noqa: E402

SCREEN = REPO_ROOT / "data" / "screening" / "nachr_a4b2_positive"
INDEX = SCREEN / "index_nachr_a4b2_positive.csv"
CIF = REPO_ROOT / "data" / "targets" / "nachr_a4b2" / "structures" / "5KXI.cif"
OUT = CATALOGUE_DIR / "screening_eval" / "nachr_a4b2_positive"
SHORT = {"PosIonizable": "cation", "Aromatic": "aromatic", "Acceptor": "acceptor"}
BASE = load_pharmacophore_config()


def native() -> dict[str, np.ndarray]:
    import gemmi
    st = gemmi.read_structure(str(CIF))
    for model in st:
        for chain in model:
            for r in chain:
                if r.name == "NCT" and chain.name == "A":
                    p = {a.name: np.array([a.pos.x, a.pos.y, a.pos.z]) for a in r}
                    ring = ["N1", "C1", "C2", "C3", "C4", "C5"]
                    return {"cation": p["N2"], "acceptor": p["N1"],
                            "aromatic": np.mean([p[n] for n in ring], axis=0)}
    raise RuntimeError("NCT not found")


NAT = native()
SMAP = {h.mol_id: read_protonated_smiles(SCREEN, h.mol_id) or h.smiles
        for h in read_rank_index(INDEX)[:100]}


def run(use_directions: bool) -> dict:
    cfg = replace(BASE, alignment=replace(BASE.alignment, use_directions=use_directions))
    out = REPO_ROOT / "data" / "_geom_probe" / f"nachr_dir_{use_directions}"
    build_from_seed_alignment(SCREEN, INDEX, out, cfg, top_n_hits=100,
                              seed_k=cfg.alignment.seed_k, smiles_map=SMAP,
                              name=f"nachr_dir_{use_directions}")
    feats = json.loads((out / "pharmacophore.json").read_text())["features"]
    dom = {}
    for f in feats:
        fam = f["family"]
        if fam in SHORT and (fam not in dom or f["support"] > dom[fam]["support"]):
            dom[fam] = f
    d = {}
    for fam, key in SHORT.items():
        if fam in dom:
            f = dom[fam]
            pos = np.array(f.get("position") or [f["x"], f["y"], f["z"]])
            d[key] = {"d_native": float(np.linalg.norm(pos - NAT[key])),
                      "support": dom[fam]["support"],
                      "has_dir": dom[fam].get("direction") is not None}
    return d


print("building directions OFF...")
off = run(False)
print("building directions ON...")
on = run(True)

lines = ["# Directional matching A/B — nAChR/5KXI (docked seed, crystal frame)", "",
         "Absolute distance (A) of each consensus feature to the crystal nicotine atom it should "
         "sit on, with orientation-aware matching OFF vs ON. The acceptor is the directional "
         "feature the ring-flip corrupts; cation/aromatic are pose-invariant controls.", "",
         "| feature | dist OFF | dist ON | support OFF | support ON | direction set (ON) |",
         "|---|--:|--:|--:|--:|:--:|"]
def _cell(rec, field, fmt="{:.2f}"):
    return fmt.format(rec[field]) if rec else "-"


for key in ("cation", "aromatic", "acceptor"):
    o, n = off.get(key), on.get(key)
    dir_set = "yes" if n and n["has_dir"] else "no"
    lines.append(f"| {key} | {_cell(o, 'd_native')} | {_cell(n, 'd_native')} | "
                 f"{_cell(o, 'support')} | {_cell(n, 'support')} | {dir_set} |")
acc_off = off.get("acceptor", {}).get("d_native")
acc_on = on.get("acceptor", {}).get("d_native")
verdict = ("improves" if acc_off and acc_on and acc_on < acc_off - 0.3
           else "no change" if acc_off and acc_on else "n/a")
lines += ["", "## Verdict", "",
          f"- Acceptor off-native distance: **{acc_off:.2f} A -> {acc_on:.2f} A** "
          f"({verdict}) with directional matching."
          if acc_off and acc_on else "- Acceptor not recovered in one arm.",
          "- Cation/aromatic (controls) should be ~unchanged — directions only add an H-bond "
          "orientation term, they do not move the pose-invariant anchors."]
report = OUT / "directional_benchmark.md"
report.write_text("\n".join(lines), encoding="utf-8")
print("\n".join(lines))
print(f"\n-> {report}")
