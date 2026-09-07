"""Unit tests for the density-based consensus strategy (Stage 4) — pure, offline."""

from __future__ import annotations

import numpy as np

from pharmpipe.features.extract import FeaturePoint, FeatureTable
from pharmpipe.pharmacophore.config import DensityConfig, ToleranceConfig
from pharmpipe.pharmacophore.density import (
    EV_FAMILY,
    _excluded_volume,
    _local_maxima,
    build_density,
)


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


def test_position_is_peak_local_not_dragged_by_diffuse_tail():
    # A tight, fully-conserved Donor mode at the origin (all 8 ligands) plus a diffuse
    # minority lobe a few A away (3 ligands). When the two lobes fall in one basin, the
    # feature POSITION must stay on the dense mode (peak-local centroid), not drift toward
    # the diffuse tail — otherwise the membership support of the real mode collapses.
    ligs = [f"L{i}" for i in range(8)]
    pts = [FeaturePoint("Donor", 0.0, 0.0, 0.0, lig) for lig in ligs]
    for lig in ("L0", "L1", "L2"):                     # diffuse secondary spot at ~2.6 A
        pts.append(FeaturePoint("Donor", 2.6, 0.0, 0.0, lig))
    table = FeatureTable(points=pts, ligand_ids=ligs)
    res = build_density(table, DensityConfig(occupancy_floor=2.0, membership_radius=1.5),
                        _tol(), "peak")
    donors = [f for f in res.pharmacophore.features if f.family == "Donor"]
    dense = min(donors, key=lambda f: abs(f.x))        # the origin mode
    assert abs(dense.x) < 1.0                           # centre stays on the dense mode
    assert dense.support == 1.0                         # all 8 ligands within membership_radius


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


def test_support_floor_drops_low_fraction_peak():
    # 10 ligands, but a Donor site drawn from only 3 of them: clears the occupancy floor
    # (3 molecules >= 2) yet support 0.3 < 0.5 -> dropped by the shared support floor.
    ligs = [f"L{i}" for i in range(10)]
    pts = [FeaturePoint("Donor", 0.0, 0.0, 0.0, lig) for lig in ("L0", "L1", "L2")]
    table = FeatureTable(points=pts, ligand_ids=ligs)
    dropped = build_density(table, DensityConfig(occupancy_floor=2.0), _tol(), "s")
    assert len(dropped.pharmacophore.features) == 0
    # ...relax the floor to 0 and the same peak is kept, at support 0.3.
    kept = build_density(table, DensityConfig(occupancy_floor=2.0), _tol(), "s",
                         min_support=0.0)
    assert len(kept.pharmacophore.features) == 1
    assert kept.pharmacophore.features[0].support == 0.3


def test_features_get_per_family_ordinal_labels():
    # two Donor sub-sites -> "Donor 1" and "Donor 2".
    pts, ligs = [], [f"L{i}" for i in range(6)]
    rng = np.random.default_rng(3)
    for lig in ligs:
        pts.append(FeaturePoint("Donor", *rng.normal(scale=0.3, size=3), lig))
        pts.append(FeaturePoint(
            "Donor", *(np.array([10.0, 0, 0]) + rng.normal(scale=0.3, size=3)), lig))
    table = FeatureTable(points=pts, ligand_ids=ligs)
    res = build_density(table, DensityConfig(occupancy_floor=2.0), _tol(), "lab")
    labels = {f.label for f in res.pharmacophore.features}
    assert labels == {"Donor 1", "Donor 2"}
    # the raw-feature plot data carries the same (label, support) per kept peak.
    donor_assignment = next(a for a in res.assignments if a.family == "Donor")
    assert set(donor_assignment.feature_labels) == set(donor_assignment.kept_labels)


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


def test_colocated_families_both_kept_by_default():
    # A donor and an acceptor cluster sit on the same spot. By default the merge is
    # same-family only, so BOTH survive (a region can be two pharmacophore types at once).
    pts, ligs = [], [f"L{i}" for i in range(6)]
    rng = np.random.default_rng(11)
    for i, lig in enumerate(ligs):
        pts.append(FeaturePoint("Donor", *rng.normal(scale=0.2, size=3), lig))
        if i < 5:                                   # acceptor slightly less populous
            pts.append(FeaturePoint("Acceptor", *rng.normal(scale=0.2, size=3), lig))
    table = FeatureTable(points=pts, ligand_ids=ligs)
    default = build_density(table, DensityConfig(occupancy_floor=2.0,
                                                 merge_overlapping=True), _tol(), "d")
    assert {f.family for f in default.pharmacophore.features} == {"Donor", "Acceptor"}
    # ...but opting back into the cross-family merge keeps only the dominant one.
    merged = build_density(table, DensityConfig(occupancy_floor=2.0, merge_overlapping=True,
                                                merge_cross_family=True), _tol(), "m")
    assert len(merged.pharmacophore.features) == 1
    assert merged.pharmacophore.features[0].family == "Donor"


def test_local_maxima_dedup_by_bandwidth():
    # Two field maxima 2.0 A apart (voxel 1.0). The dedup keeps both when bandwidth < 2,
    # and collapses to the taller one when bandwidth > 2 — the min peak spacing is the
    # smoothing bandwidth itself.
    field = np.zeros((7, 5, 5))
    field[2, 2, 2] = 1.0      # taller peak
    field[4, 2, 2] = 0.9      # shorter peak, 2 voxels (2.0 A) away
    origin = np.zeros(3)
    both = _local_maxima(field, origin, DensityConfig(voxel=1.0, bandwidth=1.0))
    assert len(both) == 2
    merged = _local_maxima(field, origin, DensityConfig(voxel=1.0, bandwidth=3.0))
    assert len(merged) == 1
    assert np.allclose(merged[0], np.array([2.5, 2.5, 2.5]))   # the taller peak survives


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
