"""Unit tests for Stage 4 feature extraction — pure, offline (no file IO)."""

from __future__ import annotations

from rdkit import Chem
from rdkit.Chem import AllChem

from pharmpipe.features.extract import FeaturePoint, FeatureTable, build_table, feature_factory
from pharmpipe.features.load import het_from_filename


def _embed(smiles: str):
    mol = Chem.AddHs(Chem.MolFromSmiles(smiles))
    AllChem.EmbedMolecule(mol, randomSeed=0)
    return mol


def test_featurize_phenol_families():
    factory = feature_factory("base")
    table = build_table([("phenol", _embed("c1ccccc1O"))], factory,
                        ["Donor", "Acceptor", "Aromatic", "Hydrophobe"])
    families = set(table.families())
    assert "Aromatic" in families          # the ring
    assert "Donor" in families             # the -OH
    assert "Acceptor" in families          # the -OH oxygen
    assert table.n_ligands == 1


def test_feature_table_coords_shape():
    p = [FeaturePoint("Donor", 1.0, 2.0, 3.0, "L1"),
         FeaturePoint("Donor", 4.0, 5.0, 6.0, "L2"),
         FeaturePoint("Acceptor", 7.0, 8.0, 9.0, "L1")]
    table = FeatureTable(points=p, ligand_ids=["L1", "L2"])
    assert table.coords("Donor").shape == (2, 3)
    assert table.coords("Acceptor").shape == (1, 3)
    assert table.coords("Hydrophobe").shape == (0, 3)
    assert table.families() == ["Donor", "Acceptor"]


def test_het_from_filename():
    from pathlib import Path
    assert het_from_filename(Path("1M2Z_DEX_A301.mol2")) == "DEX"
    assert het_from_filename(Path("8VKZ_A1ACE_A901.mol2")) == "A1ACE"
    assert het_from_filename(Path("weird.mol2")) is None
