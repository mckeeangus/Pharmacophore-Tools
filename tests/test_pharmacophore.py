"""Unit tests for Stage 4 pharmacophore assembly + IO — pure, offline."""

from __future__ import annotations

import numpy as np

from pharmpipe.clustering import KMeansSilhouette
from pharmpipe.features.extract import FeaturePoint, FeatureTable
from pharmpipe.pharmacophore.build import (
    _merge_overlapping,
    best_representative,
    build_pharmacophore,
    feature_radius,
)
from pharmpipe.pharmacophore.config import SelectionConfig, ToleranceConfig
from pharmpipe.pharmacophore.model import Pharmacophore, PharmacophoreFeature


def test_density_quantile_radius_ignores_outliers():
    # a tight core of 9 points at 0.5 A plus one point at 6 A (a far member of the
    # cluster). RMS is dragged up by the outlier; the density quantile sits on the core.
    d = np.array([0.5] * 9 + [6.0])
    rmsd = feature_radius(d, None, ToleranceConfig(method="rmsd", min=0.1, max=10.0))
    quant = feature_radius(
        d, None, ToleranceConfig(method="density_quantile", quantile=0.75,
                                 min=0.1, max=10.0))
    assert rmsd > 1.5              # the 6 A outlier inflates the RMS radius
    assert quant == 0.5           # the quantile radius rests on the dense core
    assert quant < rmsd


def _table_two_donor_clusters() -> FeatureTable:
    """6 ligands, each with a donor near (0,0,0) and one near (10,0,0)."""
    pts = []
    ligands = [f"L{i}" for i in range(6)]
    rng = np.random.default_rng(1)
    for lig in ligands:
        a = rng.normal(scale=0.2, size=3)
        b = np.array([10.0, 0.0, 0.0]) + rng.normal(scale=0.2, size=3)
        pts.append(FeaturePoint("Donor", *a, lig))
        pts.append(FeaturePoint("Donor", *b, lig))
    return FeatureTable(points=pts, ligand_ids=ligands)


def test_build_yields_two_supported_features():
    table = _table_two_donor_clusters()
    res = build_pharmacophore(
        table, KMeansSilhouette(k_min=2, k_max=4),
        SelectionConfig(min_support_fraction=0.5, min_cluster_size=2),
        ToleranceConfig(method="rmsd", min=1.0, max=3.0), name="test")
    donors = [f for f in res.pharmacophore.features if f.family == "Donor"]
    assert len(donors) == 2
    for f in donors:
        assert f.support == 1.0            # all 6 ligands present in both clusters
        assert 1.0 <= f.radius <= 3.0       # tolerance clamped
        assert f.n_ligands == 6


def test_low_support_cluster_is_dropped():
    # 4 ligands at the main site; one stray point from a single ligand far away.
    pts = [FeaturePoint("Acceptor", 0, 0, 0, f"L{i}") for i in range(4)]
    pts.append(FeaturePoint("Acceptor", 50, 50, 50, "L0"))
    table = FeatureTable(points=pts, ligand_ids=[f"L{i}" for i in range(4)])
    res = build_pharmacophore(
        table, KMeansSilhouette(k_min=2, k_max=3),
        SelectionConfig(min_support_fraction=0.5, min_cluster_size=2),
        ToleranceConfig(), name="test")
    accs = [f for f in res.pharmacophore.features if f.family == "Acceptor"]
    assert len(accs) == 1                   # the lone stray cluster is below support
    assert accs[0].n_ligands == 4


def test_top_n_caps_features_per_family():
    table = _table_two_donor_clusters()
    res = build_pharmacophore(
        table, KMeansSilhouette(k_min=2, k_max=4),
        SelectionConfig(min_support_fraction=0.5, min_cluster_size=2, top_n_per_family=1),
        ToleranceConfig(), name="test")
    assert len([f for f in res.pharmacophore.features if f.family == "Donor"]) == 1


def test_json_round_trip():
    table = _table_two_donor_clusters()
    res = build_pharmacophore(
        table, KMeansSilhouette(k_min=2, k_max=4),
        SelectionConfig(), ToleranceConfig(), name="rt")
    data = res.pharmacophore.to_dict()
    back = Pharmacophore.from_dict(data)
    assert back.name == "rt"
    assert len(back.features) == len(res.pharmacophore.features)
    assert back.features[0].family == res.pharmacophore.features[0].family


def _feat(family: str, x: float, n_points: int, radius: float = 1.0) -> PharmacophoreFeature:
    return PharmacophoreFeature(family=family, x=x, y=0.0, z=0.0, radius=radius,
                                n_points=n_points, n_ligands=n_points, support=1.0)


def test_merge_overlapping_keeps_largest_geometric():
    # Two donors 0.5 A apart (< the 1.0 radius -> overlap); the bigger one wins.
    a = _feat("Donor", 0.0, n_points=8, radius=1.0)
    b = _feat("Donor", 0.5, n_points=3, radius=1.0)
    kept = _merge_overlapping([(a, 0), (b, 1)], merge_radius=None)
    assert [f.n_points for f, _ in kept] == [8]


def test_merge_overlapping_spares_distinct_lobes():
    a = _feat("Donor", 0.0, n_points=8, radius=1.0)
    b = _feat("Donor", 10.0, n_points=6, radius=1.0)   # well separated
    kept = _merge_overlapping([(a, 0), (b, 1)], merge_radius=None)
    assert len(kept) == 2


def test_merge_overlapping_absolute_radius():
    a = _feat("Donor", 0.0, n_points=8, radius=1.0)
    b = _feat("Donor", 0.6, n_points=3, radius=1.0)
    # 0.6 A apart: merged under the geometric rule, spared under a 0.5 A cutoff.
    assert len(_merge_overlapping([(a, 0), (b, 1)], merge_radius=None)) == 1
    assert len(_merge_overlapping([(a, 0), (b, 1)], merge_radius=0.5)) == 2


def test_merge_drops_overlapping_across_families():
    # A donor and an acceptor cluster occupy the same region; a donor and acceptor
    # cannot both describe one binding spot, so only the dominant cluster survives.
    pts = []
    ligands = [f"L{i}" for i in range(6)]
    rng = np.random.default_rng(2)
    for i, lig in enumerate(ligands):
        # every ligand has a donor near the origin; the first four also drop a
        # weaker acceptor nearby, so the donor cluster is the dominant one.
        pts.append(FeaturePoint("Donor", *rng.normal(scale=0.2, size=3), lig))
        if i < 4:
            pts.append(FeaturePoint("Acceptor", *rng.normal(scale=0.2, size=3), lig))
    table = FeatureTable(points=pts, ligand_ids=ligands)
    res = build_pharmacophore(
        table, KMeansSilhouette(k_min=2, k_max=3),
        SelectionConfig(min_support_fraction=0.5, min_cluster_size=2),
        ToleranceConfig(method="rmsd", min=1.0, max=3.0), name="xfam")
    fams = {f.family for f in res.pharmacophore.features}
    assert fams == {"Donor"}          # the overlapping acceptor was displaced
    assert len(res.pharmacophore.features) == 1


def test_merge_spares_distinct_family_features_apart():
    # A donor and an acceptor in *different* regions both survive.
    pts = []
    ligands = [f"L{i}" for i in range(6)]
    rng = np.random.default_rng(3)
    for lig in ligands:
        pts.append(FeaturePoint("Donor", *rng.normal(scale=0.2, size=3), lig))
        pts.append(FeaturePoint(
            "Acceptor", *(np.array([10.0, 0.0, 0.0]) + rng.normal(scale=0.2, size=3)), lig))
    table = FeatureTable(points=pts, ligand_ids=ligands)
    res = build_pharmacophore(
        table, KMeansSilhouette(k_min=2, k_max=3),
        SelectionConfig(min_support_fraction=0.5, min_cluster_size=2),
        ToleranceConfig(method="rmsd", min=1.0, max=3.0), name="apart")
    assert {f.family for f in res.pharmacophore.features} == {"Donor", "Acceptor"}


def test_best_representative_prefers_the_fitting_ligand():
    # Model wants a Donor at the origin. L_fit has one there; L_off does not.
    table = FeatureTable(
        points=[FeaturePoint("Donor", 0.1, 0.0, 0.0, "L_fit"),
                FeaturePoint("Donor", 9.0, 0.0, 0.0, "L_off")],
        ligand_ids=["L_off", "L_fit"])  # L_off first, so order can't decide it
    ph = Pharmacophore(name="t", features=[_feat("Donor", 0.0, n_points=2, radius=1.0)])
    assert best_representative(table, ph) == "L_fit"


def test_bad_schema_rejected():
    try:
        Pharmacophore.from_dict({"schema": "nope", "name": "x", "features": []})
    except ValueError as exc:
        assert "schema" in str(exc)
    else:  # pragma: no cover
        raise AssertionError("expected ValueError")
