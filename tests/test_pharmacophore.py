"""Unit tests for Stage 4 shared assembly primitives + IO — pure, offline.

The density consensus path itself is covered in ``test_density.py``; this file exercises
the strategy-agnostic building blocks in ``build.py`` (tolerance radius, the cross-family
overlap merge and its records, representative-ligand pick) and the model schema.
"""

from __future__ import annotations

import numpy as np

from pharmpipe.features.extract import FeaturePoint, FeatureTable
from pharmpipe.pharmacophore.build import (
    _merge_overlapping,
    best_representative,
    feature_radius,
)
from pharmpipe.pharmacophore.config import ToleranceConfig
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


def _feat(family: str, x: float, n_points: int, radius: float = 1.0) -> PharmacophoreFeature:
    return PharmacophoreFeature(family=family, x=x, y=0.0, z=0.0, radius=radius,
                                n_points=n_points, n_ligands=n_points, support=1.0)


def test_merge_overlapping_keeps_largest_geometric():
    # Two donors 0.5 A apart (< the 1.0 radius -> overlap); the bigger one wins.
    a = _feat("Donor", 0.0, n_points=8, radius=1.0)
    b = _feat("Donor", 0.5, n_points=3, radius=1.0)
    kept, dropped = _merge_overlapping([(a, 0), (b, 1)], merge_radius=None)
    assert [f.n_points for f, _ in kept] == [8]
    # the dropped feature records the winner that displaced it
    assert len(dropped) == 1
    dfeat, _dpay, wfeat, wpay = dropped[0]
    assert dfeat.n_points == 3 and wfeat.n_points == 8 and wpay == 0


def test_merge_overlapping_spares_distinct_lobes():
    a = _feat("Donor", 0.0, n_points=8, radius=1.0)
    b = _feat("Donor", 10.0, n_points=6, radius=1.0)   # well separated
    kept, dropped = _merge_overlapping([(a, 0), (b, 1)], merge_radius=None)
    assert len(kept) == 2
    assert dropped == []


def test_merge_overlapping_absolute_radius():
    a = _feat("Donor", 0.0, n_points=8, radius=1.0)
    b = _feat("Donor", 0.6, n_points=3, radius=1.0)
    # 0.6 A apart: merged under the geometric rule, spared under a 0.5 A cutoff.
    assert len(_merge_overlapping([(a, 0), (b, 1)], merge_radius=None)[0]) == 1
    assert len(_merge_overlapping([(a, 0), (b, 1)], merge_radius=0.5)[0]) == 2


def test_merge_default_keeps_colocated_different_families():
    # Default (same-family only): a donor and an acceptor on the same spot are BOTH kept —
    # one region can genuinely be two pharmacophore types (e.g. a pyridine N).
    donor = _feat("Donor", 0.0, n_points=8, radius=1.0)
    acceptor = _feat("Acceptor", 0.4, n_points=4, radius=1.0)
    kept, dropped = _merge_overlapping([(donor, ("Donor", 0)), (acceptor, ("Acceptor", 0))],
                                       merge_radius=1.0)
    assert sorted(f.family for f, _ in kept) == ["Acceptor", "Donor"]
    assert dropped == []


def test_merge_same_family_still_dedups():
    # Two same-family peaks on the same spot: the denser is kept, the other dropped.
    a = _feat("Donor", 0.0, n_points=8, radius=1.0)
    b = _feat("Donor", 0.4, n_points=4, radius=1.0)
    kept, dropped = _merge_overlapping([(a, ("Donor", 0)), (b, ("Donor", 1))], merge_radius=1.0)
    assert [f.family for f, _ in kept] == ["Donor"] and len(dropped) == 1


def test_merge_cross_family_opt_in_restores_old_behaviour():
    # cross_family=True: the dominant family displaces the co-located other (old behaviour).
    donor = _feat("Donor", 0.0, n_points=8, radius=1.0)
    acceptor = _feat("Acceptor", 0.4, n_points=4, radius=1.0)
    kept, dropped = _merge_overlapping([(donor, ("Donor", 0)), (acceptor, ("Acceptor", 0))],
                                       merge_radius=1.0, cross_family=True)
    assert [f.family for f, _ in kept] == ["Donor"]
    assert dropped[0][0].family == "Acceptor" and dropped[0][3] == ("Donor", 0)


def test_best_representative_prefers_the_fitting_ligand():
    # Model wants a Donor at the origin. L_fit has one there; L_off does not.
    table = FeatureTable(
        points=[FeaturePoint("Donor", 0.1, 0.0, 0.0, "L_fit"),
                FeaturePoint("Donor", 9.0, 0.0, 0.0, "L_off")],
        ligand_ids=["L_off", "L_fit"])  # L_off first, so order can't decide it
    ph = Pharmacophore(name="t", features=[_feat("Donor", 0.0, n_points=2, radius=1.0)])
    assert best_representative(table, ph) == "L_fit"


def test_json_round_trip():
    ph = Pharmacophore(
        name="rt",
        features=[PharmacophoreFeature("Donor", 0.0, 0.0, 0.0, radius=1.5, n_points=6,
                                       n_ligands=6, support=1.0, label="Donor 1")],
        metadata={"consensus_method": "density"})
    back = Pharmacophore.from_dict(ph.to_dict())
    assert back.name == "rt"
    assert len(back.features) == 1
    assert back.features[0].family == "Donor" and back.features[0].label == "Donor 1"


def test_bad_schema_rejected():
    try:
        Pharmacophore.from_dict({"schema": "nope", "name": "x", "features": []})
    except ValueError as exc:
        assert "schema" in str(exc)
    else:  # pragma: no cover
        raise AssertionError("expected ValueError")
