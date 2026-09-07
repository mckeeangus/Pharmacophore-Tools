"""Unit tests for the screening crosswalk + pharmacophore comparison (offline, pure)."""

from __future__ import annotations

import numpy as np

from pharmpipe.screening.compare import (
    compare_models,
    compare_to_literature,
    summarise,
)
from pharmpipe.screening.crosswalk import (
    ScreeningTarget,
    docked_mol_ids,
    load_crosswalk,
    validate_overlap,
)


def _feat(family, x, y, z, support):
    return {"family": family, "x": x, "y": y, "z": z, "support": support}


def _model(spec):
    """spec: list of (family, x, y, z, support)."""
    return summarise([_feat(*s) for s in spec])


def test_summarise_dominant_and_drops_ev():
    s = summarise([_feat("Aromatic", 0, 0, 0, 0.4), _feat("Aromatic", 1, 0, 0, 0.9),
                   {"family": "ExcludedVolume", "x": 5, "y": 5, "z": 5}])
    assert s.families == {"Aromatic"}
    assert s.counts["Aromatic"] == 2
    assert s.dominant["Aromatic"][1] == 0.9              # highest support kept
    assert np.allclose(s.dominant["Aromatic"][0], [1, 0, 0])


def test_compare_models_match_and_geometry():
    # identical family triangle in a different frame (translated) -> MATCH
    a = _model([("PosIonizable", 0, 0, 0, 0.9), ("Aromatic", 5, 0, 0, 1.0),
                ("Acceptor", 0, 5, 0, 0.8)])
    b = _model([("PosIonizable", 10, 0, 0, 0.8), ("Aromatic", 15, 0, 0, 0.9),
                ("Acceptor", 10, 5, 0, 0.9)])
    c = compare_models(a, b)
    assert c.verdict == "MATCH"
    assert c.family_recall == 1.0
    assert c.mean_geom_delta < 1e-6                       # same internal geometry


def test_compare_models_partial_missing_family():
    a = _model([("PosIonizable", 0, 0, 0, 0.9), ("Aromatic", 5, 0, 0, 1.0)])
    b = _model([("PosIonizable", 0, 0, 0, 0.9), ("Aromatic", 5, 0, 0, 1.0),
                ("Acceptor", 0, 5, 0, 0.8)])
    c = compare_models(a, b)
    assert c.verdict == "PARTIAL"
    assert c.only_b == ["Acceptor"]


def test_compare_models_geometry_off_downgrades():
    a = _model([("PosIonizable", 0, 0, 0, 0.9), ("Aromatic", 9, 0, 0, 1.0)])
    b = _model([("PosIonizable", 0, 0, 0, 0.9), ("Aromatic", 4, 0, 0, 1.0)])
    c = compare_models(a, b)                              # same families, 5 A apart
    assert c.family_recall == 1.0 and c.verdict == "PARTIAL"


def test_compare_to_literature():
    a = _model([("PosIonizable", 0, 0, 0, 0.9), ("Aromatic", 5, 0, 0, 1.0)])
    lc = compare_to_literature(a, ["PosIonizable", "Aromatic", "Acceptor"])
    assert lc.recovered == ["Aromatic", "PosIonizable"]
    assert lc.missing == ["Acceptor"]
    assert lc.verdict == "PARTIAL"


def test_load_crosswalk_reads_config():
    depth, targets = load_crosswalk()                    # the real config/screening.yaml
    assert depth >= 1
    keys = {t.key for t in targets}
    assert "nachr_a4b2_positive" in keys and "esr1" in keys


def test_validate_overlap(tmp_path):
    docked = tmp_path / "d"
    docked.mkdir()
    for mid in ("A1", "A2", "B3"):
        (docked / f"{mid}_docked.sdf").write_text("")
    assert docked_mol_ids(docked) == {"A1", "A2", "B3"}
    idx_dir = tmp_path / "idx"
    idx_dir.mkdir()
    (idx_dir / "t.csv").write_text(
        "entity_id,mol_id,library_name,smiles,drugclip_score,vina_docking_score\n"
        "e,A1,lib,CCO,3.0,\ne,A2,lib,CCN,2.0,\ne,ZZ,lib,CCC,1.0,\n")
    t = ScreeningTarget("k", "P", "t.csv", "slug", None, None)
    assert validate_overlap(t, docked, idx_dir) == 2 / 3  # A1,A2 match; B3 does not
