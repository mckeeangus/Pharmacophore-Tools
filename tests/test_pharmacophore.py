"""Unit tests for Stage 4 pharmacophore assembly + IO — pure, offline."""

from __future__ import annotations

import numpy as np

from pharmpipe.clustering import KMeansSilhouette
from pharmpipe.features.extract import FeaturePoint, FeatureTable
from pharmpipe.pharmacophore.build import build_pharmacophore
from pharmpipe.pharmacophore.config import SelectionConfig, ToleranceConfig
from pharmpipe.pharmacophore.model import Pharmacophore


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


def test_bad_schema_rejected():
    try:
        Pharmacophore.from_dict({"schema": "nope", "name": "x", "features": []})
    except ValueError as exc:
        assert "schema" in str(exc)
    else:  # pragma: no cover
        raise AssertionError("expected ValueError")
