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
    resolve_coincident,
)
from pharmpipe.pharmacophore.config import ToleranceConfig
from pharmpipe.pharmacophore.io import read_model_csv, write_model_csv
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


# --- coincident-feature resolution -------------------------------------------

def _coincident_pair():
    """A pyridine-like Aromatic (x=0) + Acceptor (x=1.4) pair, both radius 1.0, within 2 A."""
    return (_feat("Aromatic", 0.0, n_points=4, radius=1.0), ("Aromatic", 0)), \
           (_feat("Acceptor", 1.4, n_points=7, radius=1.0), ("Acceptor", 0))


def _pt(family, x, lig):
    return FeaturePoint(family, x, 0.0, 0.0, lig)


def test_resolve_coincident_drops_the_undecoupled_feature():
    # 4 coupled ligands (aromatic@0 + acceptor@1.4); 3 more present the acceptor decoupled
    # (acceptor@1.4, no aromatic) — like acetylcholine at the nAChR cation/acceptor locus.
    aro, acc = _coincident_pair()
    points = []
    for i in range(4):
        points += [_pt("Aromatic", 0.0, f"C{i}"), _pt("Acceptor", 1.4, f"C{i}")]
    for i in range(3):
        points += [_pt("Acceptor", 1.4, f"A{i}")]
    kept, events = resolve_coincident([aro, acc], points, radius=2.0, min_support=2)
    assert [f.family for f, _ in kept] == ["Acceptor"]        # aromatic dropped
    assert len(events) == 1
    *_, dec_w, dec_l, coup, resolved, both = events[0]
    assert resolved and not both and dec_w == 3 and dec_l == 0 and coup == 4
    assert events[0][0].family == "Acceptor"                  # winner


def test_resolve_coincident_keeps_both_when_confounded():
    # Only coupled ligands: neither feature is ever decoupled -> no evidence -> keep both.
    aro, acc = _coincident_pair()
    points = []
    for i in range(5):
        points += [_pt("Aromatic", 0.0, f"C{i}"), _pt("Acceptor", 1.4, f"C{i}")]
    kept, events = resolve_coincident([aro, acc], points, radius=2.0, min_support=2)
    assert sorted(f.family for f, _ in kept) == ["Acceptor", "Aromatic"]
    assert len(events) == 1 and not events[0][-2] and not events[0][-1]  # not resolved, not both


def test_resolve_coincident_keeps_both_when_each_stands_alone():
    # Both features are decoupled in >= min_support ligands -> both critical -> keep both.
    aro, acc = _coincident_pair()
    points = []
    for i in range(3):                                        # aromatic alone
        points += [_pt("Aromatic", 0.0, f"R{i}")]
    for i in range(3):                                        # acceptor alone
        points += [_pt("Acceptor", 1.4, f"A{i}")]
    kept, events = resolve_coincident([aro, acc], points, radius=2.0, min_support=2)
    assert sorted(f.family for f, _ in kept) == ["Acceptor", "Aromatic"]
    assert events[0][-1] is True                              # both_standalone


def test_resolve_coincident_ignores_distant_pairs():
    # Features farther apart than `radius` are not one locus -> never resolved.
    aro = (_feat("Aromatic", 0.0, n_points=4, radius=1.0), ("Aromatic", 0))
    acc = (_feat("Acceptor", 5.0, n_points=7, radius=1.0), ("Acceptor", 0))
    points = [_pt("Acceptor", 5.0, f"A{i}") for i in range(3)]
    kept, events = resolve_coincident([aro, acc], points, radius=2.0, min_support=2)
    assert len(kept) == 2 and events == []


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


def test_model_csv_round_trip(tmp_path):
    # the tool-2 -> tool-3 interchange: families/positions/support/direction survive, and
    # the total ligand count is recovered into metadata for the visualiser's support sweep.
    ph = Pharmacophore(
        name="orig",
        features=[
            PharmacophoreFeature("PosIonizable", -0.95, 0.17, 1.28, radius=3.0, n_points=21,
                                 n_ligands=21, support=1.0, label="PosIonizable 1"),
            PharmacophoreFeature("Acceptor", 2.45, -2.01, -1.72, radius=3.0, n_points=18,
                                 n_ligands=21, support=0.857, direction=(0.0, 0.0, 1.0),
                                 label="Acceptor 1"),
        ])
    csv_path = tmp_path / "pharmacophore.csv"
    write_model_csv(ph, csv_path)
    back = read_model_csv(csv_path)
    assert back.name == "pharmacophore"  # name = file stem
    assert [f.family for f in back.features] == ["PosIonizable", "Acceptor"]
    assert back.features[0].direction is None
    assert back.features[1].direction == (0.0, 0.0, 1.0)
    assert abs(back.features[1].support - 0.857) < 1e-6
    assert back.metadata["source"]["n_ligands"] == 21  # feeds the support sweep


def test_bad_schema_rejected():
    try:
        Pharmacophore.from_dict({"schema": "nope", "name": "x", "features": []})
    except ValueError as exc:
        assert "schema" in str(exc)
    else:  # pragma: no cover
        raise AssertionError("expected ValueError")
