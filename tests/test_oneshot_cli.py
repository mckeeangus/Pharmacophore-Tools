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
