"""Unit tests for Stage 4 feature extraction — pure, offline (no file IO)."""

from __future__ import annotations

from rdkit import Chem
from rdkit.Chem import AllChem

from pharmpipe.features.extract import (
    FeaturePoint,
    FeatureTable,
    _resolve_hierarchy,
    build_table,
    feature_factory,
)
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


# The full config hierarchy: PosIonizable and NegIonizable each head TWO groups, so a
# per-family rank would mis-scope them — these tests use the full list on purpose.
_FULL_HIERARCHY = [
    ["PosIonizable", "Donor"], ["PosIonizable", "LumpedHydrophobe"],
    ["NegIonizable", "Acceptor"], ["NegIonizable", "LumpedHydrophobe"],
    ["Aromatic", "LumpedHydrophobe"],
]


def test_hierarchy_cation_subsumes_donor():
    """A protonated amine N (both PosIonizable and Donor on one atom) -> PosIonizable
    only, and the dual classification is tracked. Uses the FULL multi-group hierarchy
    (PosIonizable heads two groups) to guard against per-family rank collapse."""
    factory = feature_factory("base")
    table = build_table([("amine", _embed("CC[NH3+]"))], factory,
                        ["Donor", "PosIonizable"], _FULL_HIERARCHY)
    families = set(table.families())
    assert "PosIonizable" in families
    assert "Donor" not in families
    assert any(r.kept_family == "PosIonizable" and r.dropped_family == "Donor"
               and r.ligand_id == "amine" for r in table.resolutions)


def test_hierarchy_anion_subsumes_acceptor():
    """A carboxylate O (both NegIonizable and Acceptor) -> NegIonizable only, with the
    full multi-group hierarchy (NegIonizable also heads two groups)."""
    factory = feature_factory("base")
    table = build_table([("acid", _embed("CC(=O)[O-]"))], factory,
                        ["Acceptor", "NegIonizable"], _FULL_HIERARCHY)
    families = set(table.families())
    assert "NegIonizable" in families
    assert "Acceptor" not in families
    assert any(r.kept_family == "NegIonizable" and r.dropped_family == "Acceptor"
               for r in table.resolutions)


def test_hierarchy_preserves_nonoverlapping_hydrophobe():
    """Resolution is atom-scoped: a hydrophobe sharing atoms with an aromatic ring is
    subsumed, but a hydrophobe on disjoint atoms survives."""
    raw = [
        ("Aromatic", None, frozenset({0, 1, 2, 3, 4, 5})),          # ring
        ("LumpedHydrophobe", None, frozenset({0, 1, 2, 3, 4, 5})),  # ring face -> dropped
        ("LumpedHydrophobe", None, frozenset({6, 7, 8, 9})),        # chain -> survives
    ]
    kept, res = _resolve_hierarchy(raw, [["Aromatic", "LumpedHydrophobe"]], "L")
    fams = [fam for fam, _, _ in kept]
    assert fams.count("LumpedHydrophobe") == 1     # only the disjoint chain remains
    assert "Aromatic" in fams
    assert len(res) == 1
    assert res[0].kept_family == "Aromatic" and res[0].dropped_family == "LumpedHydrophobe"


def test_hierarchy_preserves_hydroxyl_dual():
    """Donor + Acceptor on one hydroxyl O are in different groups -> both kept."""
    factory = feature_factory("base")
    hierarchy = [["PosIonizable", "Donor"], ["NegIonizable", "Acceptor"],
                 ["Aromatic", "LumpedHydrophobe"]]
    table = build_table([("ethanol", _embed("CCO"))], factory,
                        ["Donor", "Acceptor"], hierarchy)
    families = set(table.families())
    assert "Donor" in families
    assert "Acceptor" in families
    assert table.resolutions == []


def test_no_hierarchy_keeps_all_dual_classifications():
    """With no hierarchy the redundant co-atom features are all retained (old behaviour)."""
    factory = feature_factory("base")
    table = build_table([("amine", _embed("CC[NH3+]"))], factory,
                        ["Donor", "PosIonizable"])
    families = set(table.families())
    assert {"Donor", "PosIonizable"} <= families
    assert table.resolutions == []


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
