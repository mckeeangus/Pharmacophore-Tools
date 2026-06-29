"""Unit tests for the density-based consensus strategy (Stage 4) — pure, offline."""

from __future__ import annotations

import numpy as np

from pharmpipe.features.extract import FeaturePoint, FeatureTable
from pharmpipe.pharmacophore.config import DensityConfig, ToleranceConfig
from pharmpipe.pharmacophore.density import EV_FAMILY, _excluded_volume, build_density


def _tol() -> ToleranceConfig:
    return ToleranceConfig(method="rmsd", min=1.0, max=3.0)


def test_two_lobes_yield_two_features_no_k():
    # 6 ligands, each a Donor near the origin and one near (10,0,0): two conserved
    # sub-sites -> two peaks -> two features, with no k chosen.
    pts, ligs = [], [f"L{i}" for i in range(6)]
    rng = np.random.default_rng(0)
    for lig in ligs:
        pts.append(FeaturePoint("Donor", *rng.normal(scale=0.3, size=3), lig))
        pts.append(FeaturePoint(
            "Donor", *(np.array([10.0, 0, 0]) + rng.normal(scale=0.3, size=3)), lig))
    table = FeatureTable(points=pts, ligand_ids=ligs)
    res = build_density(table, DensityConfig(occupancy_floor=2.0), _tol(), "two")
    donors = [f for f in res.pharmacophore.features if f.family == "Donor"]
    assert len(donors) == 2
    xs = sorted(f.x for f in donors)
    assert xs[0] < 2.0 and xs[1] > 8.0
    for f in donors:
        assert 1.0 <= f.radius <= 3.0


def test_evidence_unit_is_the_molecule_not_the_point():
    # One molecule dumps 6 points at the origin; three other molecules each place one
    # point at (10,0,0). With the floor at 2 effective molecules, the dense single-
    # molecule blob is dropped while the 3-molecule site is kept.
    pts = [FeaturePoint("Acceptor", *(np.random.default_rng(i).normal(scale=0.2, size=3)),
                        "L0") for i in range(6)]
    for j, lig in enumerate(["L1", "L2", "L3"]):
        pts.append(FeaturePoint("Acceptor", 10.0 + 0.1 * j, 0.0, 0.0, lig))
    table = FeatureTable(points=pts, ligand_ids=["L0", "L1", "L2", "L3"])
    res = build_density(table, DensityConfig(occupancy_floor=2.0), _tol(), "mol")
    accs = [f for f in res.pharmacophore.features if f.family == "Acceptor"]
    assert len(accs) == 1            # the single-molecule blob did not clear the floor
    assert accs[0].x > 8.0
    assert accs[0].n_ligands == 3


def test_occupancy_floor_filters():
    pts, ligs = [], [f"L{i}" for i in range(4)]
    for lig in ligs:
        pts.append(FeaturePoint("Donor", 0.0, 0.0, 0.0, lig))
    table = FeatureTable(points=pts, ligand_ids=ligs)
    kept = build_density(table, DensityConfig(occupancy_floor=3.0), _tol(), "f")
    dropped = build_density(table, DensityConfig(occupancy_floor=5.0), _tol(), "f")
    assert len(kept.pharmacophore.features) == 1     # 4 molecules >= 3
    assert len(dropped.pharmacophore.features) == 0   # 4 molecules < 5


def test_density_is_deterministic():
    pts, ligs = [], [f"L{i}" for i in range(5)]
    rng = np.random.default_rng(7)
    for lig in ligs:
        pts.append(FeaturePoint("Aromatic", *rng.normal(scale=0.4, size=3), lig))
    table = FeatureTable(points=pts, ligand_ids=ligs)
    a = build_density(table, DensityConfig(), _tol(), "d")
    b = build_density(table, DensityConfig(), _tol(), "d")
    pa = [(f.family, round(f.x, 6), round(f.y, 6), round(f.z, 6)) for f in a.pharmacophore.features]
    pb = [(f.family, round(f.x, 6), round(f.y, 6), round(f.z, 6)) for f in b.pharmacophore.features]
    assert pa == pb


def test_excluded_volume_picks_bordering_atoms_only():
    # ligand cloud at the origin; protein atoms at 1 A (occupied), 4 A (border) and
    # 20 A (too far). Only the 4 A shell should yield excluded-volume spheres.
    ligand = np.zeros((5, 3))
    occupied = np.array([[1.0, 0, 0], [0, 1.0, 0]])
    border = np.array([[4.0, 0, 0], [0, 4.0, 0], [0, 0, 4.0]])
    far = np.array([[20.0, 0, 0]])
    protein = np.vstack([occupied, border, far])
    dcfg = DensityConfig(ev_shell=5.0, ev_clearance=2.0, ev_voxel=2.0, ev_radius=1.0)
    feats = _excluded_volume(protein, ligand, dcfg)
    assert feats and all(f.family == EV_FAMILY for f in feats)
    for f in feats:
        d = np.linalg.norm(np.array(f.position) - ligand, axis=1).min()
        assert dcfg.ev_clearance < d <= dcfg.ev_shell


def test_excluded_volume_appended_in_full_build():
    pts, ligs = [], [f"L{i}" for i in range(4)]
    for lig in ligs:
        pts.append(FeaturePoint("Donor", 0.0, 0.0, 0.0, lig))
    table = FeatureTable(points=pts, ligand_ids=ligs)
    ligand_atoms = np.zeros((4, 3))
    protein = np.array([[4.0, 0, 0], [0, 4.0, 0]])
    res = build_density(table, DensityConfig(occupancy_floor=2.0), _tol(), "ev",
                        ligand_atoms=ligand_atoms, protein_atoms=protein)
    assert any(f.family == EV_FAMILY for f in res.pharmacophore.features)
