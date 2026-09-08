#!/usr/bin/env python
"""Is a seed necessary for correct convergence? — nAChR/5KXI.

Builds the feature-alignment model three ways from the same top-100 DrugCLIP compounds and
compares them, to test the thesis that the *chemistry* carries the geometry (a seed only helps
convergence):

  * crystal  — seed frame = the crystal nicotine (NCT, from the aligned pose);
  * docked   — seed frame = the GNINA top-5 docked poses;
  * seedless — no seed; frame = the top-ranked compound's lowest-energy conformer.

Comparison is **frame-independent internal geometry** (cation-aromatic / cation-acceptor /
aromatic-acceptor distances) vs the known-actives model and Beers-Reich (cation-acceptor ~5.35 A),
plus each build's **EM convergence**. If seedless reaches the same internal geometry as the seeded
builds, the seed is not necessary for correct geometry (only, at most, for faster convergence).

Offline. Run: pixi run python scripts/seed_necessity.py. Writes
catalogue/screening_eval/nachr_a4b2_positive/seed_necessity.md.
"""

from __future__ import annotations

import json
import os
import sys
from dataclasses import asdict
from itertools import combinations
from pathlib import Path

os.environ.setdefault("OMP_NUM_THREADS", "1")
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))

import numpy as np  # noqa: E402
from rdkit import Chem, RDLogger  # noqa: E402

RDLogger.DisableLog("rdApp.*")

from pharmpipe.features.dock_load import read_protonated_smiles, read_rank_index  # noqa: E402
from pharmpipe.features.load import load_pose  # noqa: E402
from pharmpipe.pharmacophore.config import load_pharmacophore_config  # noqa: E402
from pharmpipe.pharmacophore.run import build_from_seed_alignment  # noqa: E402
from pharmpipe.screening.compare import summarise  # noqa: E402
from pharmpipe.util.paths import CATALOGUE_DIR, REPO_ROOT  # noqa: E402

SCREEN = REPO_ROOT / "data" / "screening" / "nachr_a4b2_positive"
INDEX = SCREEN / "index_nachr_a4b2_positive.csv"
NCT_MOL2 = REPO_ROOT / "data/targets/nachr_a4b2/ligands/aligned_mol2/5KXI_NCT_D402.mol2"
NCT_SMILES = "C[N@@]1CCC[C@H]1c2cccnc2"
KA = json.loads((CATALOGUE_DIR / "nachr_a4b2" / "pharmacophores" / "orthosteric__positive"
                 / "pharmacophore_model.json").read_text())
OUTBASE = CATALOGUE_DIR / "screening_eval" / "nachr_a4b2_positive"
SHORT = {"PosIonizable": "cation", "Aromatic": "aromatic", "Acceptor": "acceptor"}
LIT_CAT_ACC = 5.35
CFG = load_pharmacophore_config()


def smiles_map(depth: int) -> dict[str, str]:
    return {h.mol_id: read_protonated_smiles(SCREEN, h.mol_id) or h.smiles
            for h in read_rank_index(INDEX)[:depth]}


def make_crystal_seed(path: Path) -> Path:
    """Crystal nicotine (NCT) as a seed SDF, bonds from the SMILES template."""
    mol, method = load_pose(NCT_MOL2, NCT_SMILES)
    if mol is None:
        raise RuntimeError(f"could not load crystal NCT ({method})")
    mol.SetProp("_Name", "NCT_crystal")
    with Chem.SDWriter(str(path)) as w:
        w.write(mol)
    return path


def internal(features: list[dict]) -> dict[str, float]:
    s = summarise(features)
    dom = {SHORT[k]: v[0] for k, v in s.dominant.items() if k in SHORT}
    out = {}
    for a, b in combinations(("cation", "aromatic", "acceptor"), 2):
        if a in dom and b in dom:
            out[f"{a[:3]}-{b[:3]}"] = float(np.linalg.norm(dom[a] - dom[b]))
    out["families"] = "+".join(sorted(SHORT[f][:3] for f in s.dominant if f in SHORT))
    return out


def build(tag: str, **kw) -> dict:
    out = REPO_ROOT / "data" / "_geom_probe" / f"seed_necessity_{tag}"   # gitignored scratch
    res = build_from_seed_alignment(SCREEN, INDEX, out, CFG, top_n_hits=100,
                                    seed_k=CFG.alignment.seed_k, name=f"nachr_{tag}",
                                    smiles_map=SMAP, **kw)
    if res is None or res.pharmacophore is None:
        return {"tag": tag, "ok": False}
    src = res.pharmacophore.metadata["source"]
    geom = internal([asdict(f) for f in res.pharmacophore.features])
    conv = src.get("em_convergence") or []
    return {"tag": tag, "ok": True, "geom": geom, "n_aligned": src["n_aligned"],
            "em_iters": len(conv), "em_shift": round(conv[-1][1], 3) if conv else None}


SMAP = smiles_map(100)
ka_geom = internal(KA["features"])
print("building crystal seed...")
_scratch = REPO_ROOT / "data" / "_geom_probe"       # gitignored (under data/)
_scratch.mkdir(parents=True, exist_ok=True)
crystal_seed = make_crystal_seed(_scratch / "nct_crystal_seed.sdf")

rows = []
print("build crystal-seeded...")
rows.append(build("crystal", seed_poses=crystal_seed))
print("build docked-seeded...")
rows.append(build("docked"))
print("build seedless...")
rows.append(build("seedless", seedless=True))

lines = ["# Is the seed necessary for correct convergence? — nAChR/5KXI", "",
         "Three inits of the same top-100 DrugCLIP compounds; compared by **frame-independent "
         "internal geometry** (A) vs the known-actives model and Beers-Reich (cation-acceptor "
         f"~{LIT_CAT_ACC}). Ground truth internal geometry (known actives): "
         + ", ".join(f"{k} {v:.2f}" for k, v in ka_geom.items() if k != "families") + ".", "",
         "| init | families | cat-aro | cat-acc | aro-acc | aligned | EM iters | final shift (A) |",
         "|---|---|--:|--:|--:|--:|--:|--:|"]
for r in rows:
    if not r["ok"]:
        lines.append(f"| {r['tag']} | (failed) | - | - | - | - | - | - |")
        continue
    g = r["geom"]
    lines.append(f"| {r['tag']} | {g.get('families','-')} | {g.get('cat-aro',float('nan')):.2f} | "
                 f"{g.get('cat-acc',float('nan')):.2f} | {g.get('aro-acc',float('nan')):.2f} | "
                 f"{r['n_aligned']} | {r['em_iters']} | "
                 f"{r['em_shift'] if r['em_shift'] is not None else '-'} |")

# verdict: do all inits recover the 3 families with internal geometry near known-actives?
def ok3(r):
    return r["ok"] and r["geom"].get("families") == "acc+aro+cat"
def close(r):
    g = r["ok"] and r["geom"]
    return g and abs(g.get("cat-aro", 99) - ka_geom["cat-aro"]) < 1.0
allrec = all(ok3(r) for r in rows)
seedless = next(r for r in rows if r["tag"] == "seedless")
lines += ["", "## Verdict", "",
          f"- All three inits recover the 3-point model: **{allrec}**.",
          f"- Seedless recovers the families **{ok3(seedless)}** and matches the known-actives "
          f"cation-aromatic within 1 A **{close(seedless)}**.",
          "- **Interpretation:** if seedless reaches the same internal geometry as the crystal/"
          "docked seeds, a seed is **not** necessary for correct geometry on nAChR — the shared "
          "rigid cores carry it — and its role is at most faster/safer convergence. The acceptor "
          "stays low-confidence (positional matching; directionality is the next iteration)."]
report = OUTBASE / "seed_necessity.md"
report.parent.mkdir(parents=True, exist_ok=True)
report.write_text("\n".join(lines), encoding="utf-8")
print("\n".join(lines))
print(f"\n-> {report}")
