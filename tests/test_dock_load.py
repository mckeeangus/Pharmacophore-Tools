"""Unit tests for the DrugCLIP -> GNINA docked-set loader (Stage 4, offline)."""

from __future__ import annotations

import csv

import pytest
from rdkit import Chem
from rdkit.Chem import AllChem

from pharmpipe.features.dock_load import (
    load_docked_set,
    read_rank_index,
    write_manifest,
)


def _write_docked_sdf(path, smiles: str, n_poses: int, scores: list[dict] | None = None) -> None:
    """Write ``n_poses`` docked poses of ``smiles``.

    ``scores[i]`` optionally sets that pose's GNINA tags (``CNNscore`` / ``CNNaffinity`` /
    ``CNN_VS`` / ``minimizedAffinity``); poses are written in the given (SDF/CNNscore) order.
    """
    mol = Chem.AddHs(Chem.MolFromSmiles(smiles))
    AllChem.EmbedMultipleConfs(mol, numConfs=n_poses, randomSeed=0xF00D)
    mol = Chem.RemoveHs(mol)                       # docked SDFs are heavy-atom-only
    writer = Chem.SDWriter(str(path))
    for i, conf in enumerate(mol.GetConformers()):
        rec = Chem.Mol(mol)
        rec.SetProp("protonated_smiles", smiles)
        for tag, val in (scores[i].items() if scores else []):
            rec.SetProp(tag, str(val))
        writer.write(rec, confId=conf.GetId())
    writer.close()


def _write_index(path, rows: list[tuple[str, str, float | str]]) -> None:
    """rows = [(mol_id, smiles, drugclip_score), ...] in arbitrary order."""
    with path.open("w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["entity_id", "mol_id", "library_name", "smiles",
                    "drugclip_score", "vina_docking_score"])
        for i, (mol_id, smi, score) in enumerate(rows):
            w.writerow([f"e{i}", mol_id, "lib", smi, score, ""])


def _fixture(tmp_path, rows, poses_per_sdf=3, make_sdf=None, scores=None):
    index = tmp_path / "index_test_output.csv"
    _write_index(index, rows)
    make_sdf = rows if make_sdf is None else make_sdf
    for mol_id, smi, _ in make_sdf:
        _write_docked_sdf(tmp_path / f"{mol_id}_docked.sdf", smi, poses_per_sdf, scores)
    return index


def test_index_ranks_by_score_descending(tmp_path):
    index = _fixture(tmp_path, [("low", "CCO", 1.0), ("high", "CCN", 5.0),
                                ("mid", "CCC", 3.0)])
    hits = read_rank_index(index)
    assert [h.mol_id for h in hits] == ["high", "mid", "low"]
    assert [h.rank for h in hits] == [1, 2, 3]


def test_index_blank_score_sorts_last(tmp_path):
    index = _fixture(tmp_path, [("a", "CCO", ""), ("b", "CCN", 2.0)])
    hits = read_rank_index(index)
    assert [h.mol_id for h in hits] == ["b", "a"]


def test_top_hits_and_one_pose_default(tmp_path):
    rows = [("a", "c1ccccc1O", 9.0), ("b", "c1ccncc1", 8.0), ("c", "CCCCCO", 7.0)]
    index = _fixture(tmp_path, rows)  # no GNINA tags -> falls back to stable SDF order
    molecules, report, manifest = load_docked_set(tmp_path, index, top_n_hits=2)
    assert [lid for lid, _ in molecules] == ["a__p1", "b__p1"]
    assert all(r.selected_rank == 1 and r.gnina_rank == 1 for r in manifest)
    assert {r.mol_id for r in manifest} == {"a", "b"}
    assert report.by_method


def test_top_poses_takes_multiple_per_hit(tmp_path):
    rows = [("a", "c1ccccc1O", 9.0), ("b", "c1ccncc1", 8.0)]
    index = _fixture(tmp_path, rows, poses_per_sdf=3)
    molecules, _, manifest = load_docked_set(tmp_path, index, top_n_hits=1, top_n_poses=3)
    ids = [lid for lid, _ in molecules]
    assert ids == ["a__p1", "a__p2", "a__p3"]
    assert len({r.ligand_id for r in manifest}) == 3


def test_pose_selection_by_cnnaffinity_reorders(tmp_path):
    # pose 2 (SDF/CNNscore rank 2) has the BEST CNNaffinity; the default picks it.
    scores = [{"CNNscore": 0.9, "CNNaffinity": 4.0, "minimizedAffinity": -5.0},
              {"CNNscore": 0.8, "CNNaffinity": 6.0, "minimizedAffinity": -6.0},
              {"CNNscore": 0.7, "CNNaffinity": 5.0, "minimizedAffinity": -4.0}]
    index = _fixture(tmp_path, [("a", "c1ccncc1", 9.0)], poses_per_sdf=3, scores=scores)
    mols, _, man = load_docked_set(tmp_path, index, top_n_hits=1, top_n_poses=1)  # cnnaffinity
    assert mols[0][0] == "a__p2" and man[0].gnina_rank == 2
    # cnnscore selection keeps the SDF-first pose instead
    mols_cs, _, _ = load_docked_set(tmp_path, index, top_n_hits=1, top_n_poses=1,
                                    pose_score="cnnscore")
    assert mols_cs[0][0] == "a__p1"
    # vina selection prefers the most negative (pose 2 at -6.0)
    mols_v, _, _ = load_docked_set(tmp_path, index, top_n_hits=1, top_n_poses=1,
                                   pose_score="vina")
    assert mols_v[0][0] == "a__p2"


def test_max_vina_filters_clashes(tmp_path):
    # pose 1 clashes (Vina +13) though it has the best CNNaffinity; max_vina=0 drops it.
    scores = [{"CNNaffinity": 6.0, "minimizedAffinity": 13.0},
              {"CNNaffinity": 5.0, "minimizedAffinity": -5.0},
              {"CNNaffinity": 4.0, "minimizedAffinity": -4.0}]
    index = _fixture(tmp_path, [("a", "c1ccncc1", 9.0)], poses_per_sdf=3, scores=scores)
    mols, _, _ = load_docked_set(tmp_path, index, top_n_hits=1, top_n_poses=1, max_vina=0.0)
    assert mols[0][0] == "a__p2"  # the clashing best-CNNaffinity pose was filtered out


def test_invalid_pose_score_raises(tmp_path):
    index = _fixture(tmp_path, [("a", "c1ccncc1", 9.0)])
    with pytest.raises(ValueError, match="pose_score"):
        load_docked_set(tmp_path, index, top_n_hits=1, pose_score="nonsense")


def test_missing_sdf_is_skipped_and_recorded(tmp_path):
    rows = [("has", "c1ccccc1O", 9.0), ("missing", "CCN", 8.0)]
    index = _fixture(tmp_path, rows, make_sdf=[("has", "c1ccccc1O", 9.0)])
    molecules, report, manifest = load_docked_set(tmp_path, index, top_n_hits=2)
    assert [r.mol_id for r in manifest] == ["has"]
    assert ("missing", "no_sdf") in report.skipped


def test_top_poses_capped_by_available(tmp_path):
    index = _fixture(tmp_path, [("a", "c1ccccc1O", 9.0)], poses_per_sdf=2)
    molecules, _, _ = load_docked_set(tmp_path, index, top_n_hits=1, top_n_poses=5)
    assert len(molecules) == 2  # only 2 poses exist, never fabricated


def test_write_manifest_roundtrip(tmp_path):
    rows = [("a", "c1ccccc1O", 9.0), ("b", "c1ccncc1", 8.0)]
    index = _fixture(tmp_path, rows)
    _, _, manifest = load_docked_set(tmp_path, index, top_n_hits=2)
    out = write_manifest(manifest, tmp_path / "docked_manifest.csv")
    with out.open(encoding="utf-8") as fh:
        rows_read = list(csv.DictReader(fh))
    assert [r["ligand_id"] for r in rows_read] == ["a__p1", "b__p1"]
    assert rows_read[0]["drugclip_rank"] == "1"
    assert rows_read[0]["drugclip_score"] == "9"
    assert rows_read[0]["pose_metric"] == "cnnaffinity"
