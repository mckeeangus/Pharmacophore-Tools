"""Unit tests for the one-shot CLI plumbing (Stage 4) — offline, no pkasolver/PyMOL.

Covers the general ``_protonate_rows`` CSV round-trip (with ``_protonate_one`` stubbed,
so the pkasolver stack is never imported) and the ``--input`` argument guards of the
build driver.
"""

from __future__ import annotations

import importlib.util
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[1]


def _load(name: str):
    """Import a repo ``scripts/*.py`` module by path (they are not a package)."""
    spec = importlib.util.spec_from_file_location(name, REPO / "scripts" / f"{name}.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


# --- protonate_ligands general mode ----------------------------------------------------

def test_protonate_rows_roundtrip_and_reuse(tmp_path, monkeypatch):
    mod = _load("protonate_ligands")
    calls: list[str] = []

    def fake_one(smiles, query_model, ph, guard):
        calls.append(smiles)
        return f"{smiles}_H", 1, "7.10", "", "pkasolver"

    monkeypatch.setattr(mod, "_protonate_one", fake_one)
    rows = [{"het_code": "AAA", "smiles": "CCO"},
            {"het_code": "BBB", "smiles": "CCN"},
            {"het_code": "", "smiles": "skip"}]        # missing HET is ignored
    out = tmp_path / "protonated_ligands.csv"

    changed, reused = mod._protonate_rows(rows, out, None, 7.4, force=True, guard=[])
    assert (changed, reused) == (2, 0)
    assert calls == ["CCO", "CCN"]

    import csv
    written = list(csv.DictReader(out.open(encoding="utf-8")))
    assert [r["het_code"] for r in written] == ["AAA", "BBB"]
    assert written[0]["protonated_smiles"] == "CCO_H"
    assert set(written[0]) == set(mod.FIELDS)

    # Second pass without --force reuses the cached HETs (no protonation call).
    calls.clear()
    changed, reused = mod._protonate_rows(rows, out, None, 7.4, force=False, guard=[])
    assert (changed, reused) == (0, 2)
    assert calls == []


# --- build_pharmacophore --input/--out guards -------------------------------------------

def test_normalise_csv_index_accepts_all_input_shapes(tmp_path):
    """align-molecules should accept a full ranked CSV, a header-less smiles,score screen output,
    a headered smiles,score with no mol_id, and a bare one-column SMILES list."""
    mod = _load("align_molecules")
    from pharmpipe.features.dock_load import read_rank_index

    def hits(text, name):
        p = tmp_path / name
        p.write_text(text, encoding="utf-8")
        return read_rank_index(mod._normalise_csv_index(p, tmp_path))

    # 1. header-less smiles,score (raw retrieval.py output) -> mol_id generated, ranked by score
    h = hits("CCO,4.68\nCCN,4.10\n", "a.csv")
    assert [x.smiles for x in h] == ["CCO", "CCN"]
    assert h[0].score == 4.68 and h[0].mol_id.startswith("hit")

    # 2. headered smiles,score with NO mol_id -> mol_id generated, score honoured
    h = hits("smiles,score\nCCO,1.0\nc1ccccc1,2.0\n", "b.csv")
    assert h[0].smiles == "c1ccccc1" and all(x.mol_id for x in h)   # higher score first

    # 3. full ranked CSV with mol_id -> ids preserved
    h = hits("mol_id,smiles,drugclip_score\nX1,CCO,5\nX2,CCN,9\n", "c.csv")
    assert h[0].mol_id == "X2" and h[0].smiles == "CCN"

    # 4. bare one-column SMILES list -> input order (no score)
    h = hits("CCO\nCCN\n", "d.csv")
    assert [x.smiles for x in h] == ["CCO", "CCN"]


def test_crystal_smiles_map_skips_pkasolver_by_default(tmp_path, monkeypatch):
    """Without --pkasolver, build-pharmacophore must not shell out to pkasolver, and must
    ignore a protonated_ligands.csv even if one already sits beside --smiles."""
    mod = _load("build_pharmacophore")

    def fail(*a, **k):
        raise AssertionError("pkasolver must not run without --pkasolver")

    monkeypatch.setattr(mod, "_run_pkasolver", fail)
    smiles_csv = tmp_path / "ligands.csv"
    smiles_csv.write_text("het_code,smiles\nLIG,CCO\n", encoding="utf-8")
    (tmp_path / "protonated_ligands.csv").write_text(
        "het_code,smiles,protonated_smiles\nLIG,CCO,[O-]CC\n", encoding="utf-8")

    smiles_map = mod._crystal_smiles_map(smiles_csv, False)
    assert smiles_map == {"LIG": "CCO"}  # neutral SMILES, protonated_ligands.csv ignored


def test_crystal_smiles_map_runs_pkasolver_when_requested(tmp_path, monkeypatch):
    mod = _load("build_pharmacophore")

    def fake_run(smiles_csv, out_csv):
        out_csv.write_text("het_code,smiles,protonated_smiles\nLIG,CCO,[O-]CC\n",
                           encoding="utf-8")

    monkeypatch.setattr(mod, "_run_pkasolver", fake_run)
    smiles_csv = tmp_path / "ligands.csv"
    smiles_csv.write_text("het_code,smiles\nLIG,CCO\n", encoding="utf-8")

    smiles_map = mod._crystal_smiles_map(smiles_csv, True)
    assert smiles_map == {"LIG": "[O-]CC"}


def test_build_requires_out(tmp_path):
    mod = _load("build_pharmacophore")
    with pytest.raises(SystemExit):
        mod.main(["--input", str(tmp_path)])


def test_build_rejects_unknown_input(tmp_path):
    mod = _load("build_pharmacophore")
    bad = tmp_path / "x.txt"
    bad.write_text("")
    with pytest.raises(SystemExit):
        mod.main(["--input", str(bad), "--out", str(tmp_path / "o")])


# --- visualise_pharmacophore auto-compounds detection -----------------------------------

def test_auto_compounds_finds_source_input(tmp_path):
    """visualise-pharmacophore should locate the aligned ligands a model was built from via
    the sibling pharmacophore_model.json's metadata.source, with no --compounds passed."""
    import json

    mod = _load("visualise_pharmacophore")
    aligned = tmp_path / "aligned_compounds.sdf"
    aligned.write_text("", encoding="utf-8")
    (tmp_path / "pharmacophore_model.json").write_text(
        json.dumps({"metadata": {"source": {"input": str(aligned)}}}), encoding="utf-8")

    found = mod._auto_compounds(tmp_path / "pharmacophore.csv")
    assert found == aligned


def test_auto_compounds_none_when_json_or_path_missing(tmp_path):
    mod = _load("visualise_pharmacophore")
    assert mod._auto_compounds(tmp_path / "pharmacophore.csv") is None  # no sibling JSON

    import json
    (tmp_path / "pharmacophore_model.json").write_text(
        json.dumps({"metadata": {"source": {"input": str(tmp_path / "missing.sdf")}}}),
        encoding="utf-8")
    assert mod._auto_compounds(tmp_path / "pharmacophore.csv") is None  # source path gone
