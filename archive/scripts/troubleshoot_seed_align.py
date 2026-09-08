#!/usr/bin/env python
"""Troubleshoot + benchmark the seed-5 / depth-100 seed-alignment recipe on 5KXI/nAChR.

Sweeps the alignment parameters one axis at a time from a sensible base and scores each build
against ground truth: the **crystal nicotine** (NCT in 5KXI.cif, absolute distances), the
**known-actives** model (internal geometry), and the **literature** (Beers-Reich cation-acceptor
~5.35 A). Also runs a determinism check (a repeated build must be identical). Conformer ensembles
are embedded once per (seed_k, depth, conformer-params) and reused across the clique/RMSD sweep,
so the expensive step runs a handful of times, not once per row.

Offline; uses the GNINA-docked poses in data/screening/nachr_a4b2_positive/ as the seed source
(stand-in for AutoDockFR). Run: pixi run python scripts/troubleshoot_seed_align.py.
Writes a report to catalogue/screening_eval/nachr_a4b2_positive/seed5_benchmark.md.
"""

from __future__ import annotations

import json
import os
import sys
from dataclasses import asdict, replace
from pathlib import Path

os.environ.setdefault("OMP_NUM_THREADS", "1")
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))

import numpy as np  # noqa: E402
from rdkit import RDLogger  # noqa: E402

RDLogger.DisableLog("rdApp.*")

from pharmpipe.features.conformers import generate_conformers  # noqa: E402
from pharmpipe.features.dock_load import (  # noqa: E402
    load_docked_set,
    read_protonated_smiles,
    read_rank_index,
)
from pharmpipe.features.extract import (  # noqa: E402
    FeaturePoint,
    FeatureTable,
    conformer_features,
    feature_factory,
)
from pharmpipe.pharmacophore.align import seed_align  # noqa: E402
from pharmpipe.pharmacophore.config import load_pharmacophore_config  # noqa: E402
from pharmpipe.pharmacophore.density import build_density  # noqa: E402
from pharmpipe.screening.compare import summarise  # noqa: E402
from pharmpipe.util.paths import CATALOGUE_DIR, REPO_ROOT  # noqa: E402

SCREEN = REPO_ROOT / "data" / "screening" / "nachr_a4b2_positive"
INDEX = SCREEN / "index_nachr_a4b2_positive.csv"
CIF = REPO_ROOT / "data" / "targets" / "nachr_a4b2" / "structures" / "5KXI.cif"
KA = (CATALOGUE_DIR / "nachr_a4b2" / "pharmacophores" / "orthosteric__positive"
      / "pharmacophore.json")
REPORT = CATALOGUE_DIR / "screening_eval" / "nachr_a4b2_positive" / "seed5_benchmark.md"
SHORT = {"PosIonizable": "cation", "Aromatic": "aromatic", "Acceptor": "acceptor"}
LIT_CAT_ACC = 5.35  # Beers-Reich nicotinic cationic-N -> H-bond acceptor

CFG = load_pharmacophore_config()
FAC = feature_factory(CFG.features.fdef)
FAMILIES = CFG.alignment.align_families or CFG.features.families
HIER = CFG.features.feature_hierarchy


# ---- ground truth --------------------------------------------------------------
def native_nicotine() -> dict[str, np.ndarray]:
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
    raise RuntimeError("NCT not found in 5KXI.cif")


NAT = native_nicotine()
KA_SUM = summarise(json.loads(KA.read_text())["features"])


# ---- conformer pool (cached per conf-params key) -------------------------------
_POOL_CACHE: dict = {}


def build_clouds(seed_k: int, depth: int, acfg):
    key = (seed_k, depth, acfg.n_conformers, acfg.energy_window, acfg.max_confs, acfg.rmsd_prune)
    if key in _POOL_CACHE:
        return _POOL_CACHE[key]
    seed_mols, _, _ = load_docked_set(SCREEN, INDEX, seed_k, 1, pose_score="cnnaffinity")
    seed_points = [(fam, xyz, d, lig)
                   for lig, mol in seed_mols
                   for fam, xyz, d in conformer_features(mol, FAC, FAMILIES, HIER, conf_id=0)]
    seed_mol_ids = {lig.split("__", 1)[0] for lig, _ in seed_mols}
    compounds = []
    for hit in read_rank_index(INDEX)[:depth]:
        if hit.mol_id in seed_mol_ids:
            continue
        # faithful to the real pipeline: use the pH-7.4 microstate (offline, from the docked
        # SDF) rather than the neutral index SMILES — protonation changes cation/acceptor perception
        smi = read_protonated_smiles(SCREEN, hit.mol_id) or hit.smiles
        gen = generate_conformers(smi, acfg)
        if gen is None:
            continue
        mol, cids, _e = gen
        compounds.append((hit.mol_id,
                          [conformer_features(mol, FAC, FAMILIES, HIER, conf_id=c) for c in cids]))
    _POOL_CACHE[key] = (seed_points, compounds)
    return seed_points, compounds


def run(seed_k, depth, acfg, dcfg=None):
    dcfg = dcfg or CFG.density
    seed_points, compounds = build_clouds(seed_k, depth, acfg)
    res = seed_align(seed_points, compounds, dist_tol=acfg.dist_tol, min_clique=acfg.min_clique,
                     membership_radius=dcfg.membership_radius,
                     max_align_rmsd=acfg.max_align_rmsd,
                     use_directions=acfg.use_directions, projected_length=acfg.projected_length)
    ligs = sorted({lig for *_, lig in res.points})
    n_aligned = sum(1 for r in res.manifest if r.source == "aligned" and r.aligned)
    n_dropped = sum(1 for r in res.manifest if r.source == "aligned" and not r.aligned)
    pts = [FeaturePoint(f, float(x[0]), float(x[1]), float(x[2]), lig)
           for f, x, d, lig in res.points]
    table = FeatureTable(points=pts, ligand_ids=ligs)
    build = build_density(table, dcfg, CFG.tolerance, "x",
                          {"selection": asdict(CFG.selection), "tolerance": asdict(CFG.tolerance)},
                          min_support=CFG.selection.min_support_fraction)
    s = summarise([{"family": f.family, "x": f.x, "y": f.y, "z": f.z, "support": f.support}
                   for f in build.pharmacophore.features])
    return s, res, n_aligned, n_dropped


def metrics(s) -> dict:
    dom = {SHORT[k]: v[0] for k, v in s.dominant.items() if k in SHORT}
    m = {"nfeat": sum(s.counts.values()),
         "fams": "+".join(sorted(SHORT[f][:3] for f in s.dominant if f in SHORT))}
    for k in ("cation", "aromatic", "acceptor"):
        m[f"d_{k}"] = float(np.linalg.norm(dom[k] - NAT[k])) if k in dom else None
    def dist(a, b):
        return float(np.linalg.norm(dom[a] - dom[b])) if a in dom and b in dom else None
    m["cat_arom"] = dist("cation", "aromatic")
    m["cat_acc"] = dist("cation", "acceptor")
    return m


def fmt(v, nd=2):
    return f"{v:.{nd}f}" if isinstance(v, (int, float)) else "-"


def _ka_d(fam: str) -> float:
    """Internal distance cation->fam in the known-actives model."""
    return float(np.linalg.norm(KA_SUM.dominant["PosIonizable"][0] - KA_SUM.dominant[fam][0]))


BASE = CFG.alignment  # the config defaults (seed_k=5, depth via top_hits below, gate 1.5)
DEPTH = 100
lines = ["# Seed-5 / depth-100 seed-alignment — 5KXI/nAChR benchmark", "",
         "Method: dock the top-5 DrugCLIP hits (GNINA stand-in for AutoDockFR), seed a feature "
         "model, then incrementally align + fold in ranked compounds 6..100 by feature-clique "
         "matching on relative intra-molecular distances. Scored vs the **crystal nicotine** "
         "(absolute A), the **known-actives** model, and **Beers-Reich** (cation-acceptor "
         f"~{LIT_CAT_ACC} A).", "",
         f"Ground truth internal geometry: known-actives cat-arom {fmt(_ka_d('Aromatic'))} A, "
         f"cat-acc {fmt(_ka_d('Acceptor'))} A; native nicotine cat-acc "
         f"{fmt(np.linalg.norm(NAT['cation']-NAT['acceptor']))} A.", "",
         "| sweep | value | align/drop | feats | families | d_cat | d_arom | d_acc "
         "| cat-arom | cat-acc |",
         "|---|---|---|--:|---|--:|--:|--:|--:|--:|"]


def row(label, value, seed_k, depth, acfg, dcfg=None):
    s, res, na, nd = run(seed_k, depth, acfg, dcfg)
    m = metrics(s)
    lines.append(f"| {label} | {value} | {na}/{nd} | {m['nfeat']} | {m['fams']} | "
                 f"{fmt(m['d_cation'])} | {fmt(m['d_aromatic'])} | {fmt(m['d_acceptor'])} | "
                 f"{fmt(m['cat_arom'])} | {fmt(m['cat_acc'])} |")
    return m


print("base (config defaults, seed_k=5, depth=100)...")
base_m = row("**base**", "seed5/d100", BASE.seed_k, DEPTH, BASE)

for sk in (3, 5, 10):
    row("seed_k", sk, sk, DEPTH, BASE)
for dt in (1.0, 1.5, 2.0):
    row("dist_tol", dt, BASE.seed_k, DEPTH, replace(BASE, dist_tol=dt))
for mc in (3, 4):
    row("min_clique", mc, BASE.seed_k, DEPTH, replace(BASE, min_clique=mc))
for gate in (0.75, 1.0, 1.5, None):
    row("max_align_rmsd", gate, BASE.seed_k, DEPTH, replace(BASE, max_align_rmsd=gate))
for mc_ew in ((32, 10.0), (64, 15.0), (128, 20.0)):
    nc, ew = mc_ew
    row("conformers(n,ewin)", f"{nc},{ew}", BASE.seed_k, DEPTH,
        replace(BASE, n_conformers=nc, energy_window=ew))
# The pyridine-N acceptor is co-located with the aromatic centroid. The default same-family-only
# merge keeps both; the OLD cross-family merge deleted the acceptor into the aromatic. Show both.
row("merge_cross_family", "True (old)", BASE.seed_k, DEPTH, BASE,
    replace(CFG.density, merge_cross_family=True))

# determinism
s1, *_ = run(BASE.seed_k, DEPTH, BASE)
s2, *_ = run(BASE.seed_k, DEPTH, BASE)
det = all(np.allclose(s1.dominant[f][0], s2.dominant[f][0]) for f in s1.dominant) \
    and set(s1.dominant) == set(s2.dominant)
lines += ["", f"**Determinism:** two identical builds {'MATCH (identical)' if det else 'DIFFER'}.",
          "", "## Reading", "",
          "- `d_*` = absolute distance of the consensus feature to the crystal nicotine atom "
          "(cation=pyrrolidinium N, aromatic=pyridine centroid, acceptor=pyridine N).",
          "- `cat-acc` is inflated by the GNINA seed **ring-flip** (acceptor low-confidence); "
          "`cat-arom` + the absolute cation/aromatic accuracy are the trustworthy signals.",
          "- Base result: cation/aromatic within ~"
          f"{fmt(max(base_m['d_cation'] or 0, base_m['d_aromatic'] or 0), 1)} A of the crystal."]
REPORT.parent.mkdir(parents=True, exist_ok=True)
REPORT.write_text("\n".join(lines), encoding="utf-8")
print("\n".join(lines))
print(f"\n-> {REPORT}")
