"""Unit tests for the pure protonation-state selection (Stage 4 prep) — offline.

These exercise the pKa-ladder walk without pkasolver: ``States`` are faked with RDKit
mols, matching the duck-typed interface ``dominant_microstate_at_ph`` reads.
"""

from __future__ import annotations

from dataclasses import dataclass

import pytest
from rdkit import Chem

from pharmpipe.prep.protonate import (
    WeakAcidClass,
    dominant_microstate_at_ph,
    largest_fragment,
    neutralize_weak_acids,
    protonated_mol,
    to_smiles,
)


@dataclass
class FakeState:
    pka: float
    protonated_mol: Chem.Mol
    deprotonated_mol: Chem.Mol
    reaction_center_idx: int = -1


def _state(pka: float, prot: str, deprot: str) -> FakeState:
    return FakeState(pka, Chem.MolFromSmiles(prot), Chem.MolFromSmiles(deprot))


def test_acid_deprotonates_above_its_pka():
    # acetic acid, pKa 4.19 -> acetate at pH 7.4
    states = [_state(4.19, "CC(=O)O", "CC(=O)[O-]")]
    assert to_smiles(dominant_microstate_at_ph(states, 7.4)) == "CC(=O)[O-]"


def test_base_stays_protonated_below_its_pka():
    # methylamine, pKa 10.6 -> methylammonium at pH 7.4
    states = [_state(10.6, "C[NH3+]", "CN")]
    assert to_smiles(dominant_microstate_at_ph(states, 7.4)) == "C[NH3+]"


def test_multi_site_ladder_picks_the_right_rung():
    # imidazole ladder; at pH 7.4 the neutral form dominates (between 6.98 and 11.45)
    states = [
        _state(3.55, "c1c[nH2+]c[nH+]1", "c1c[nH+]c[nH]1"),
        _state(6.98, "c1c[nH+]c[nH]1", "c1c[nH]cn1"),
        _state(11.45, "c1c[nH]cn1", "c1c[n-]cn1"),
    ]
    assert to_smiles(dominant_microstate_at_ph(states, 7.4)) == \
        to_smiles(Chem.MolFromSmiles("c1c[nH]cn1"))


def test_low_ph_keeps_everything_protonated():
    states = [_state(4.19, "CC(=O)O", "CC(=O)[O-]")]
    assert to_smiles(dominant_microstate_at_ph(states, 1.0)) == "CC(=O)O"


def test_no_states_returns_input_unchanged():
    mol = Chem.MolFromSmiles("c1ccccc1")
    assert to_smiles(protonated_mol(mol, [], 7.4)) == to_smiles(mol)
    with pytest.raises(ValueError):
        dominant_microstate_at_ph([], 7.4)


def test_largest_fragment_strips_salt():
    mol = Chem.MolFromSmiles("CC(=O)[O-].[Na+]")
    assert to_smiles(largest_fragment(mol)) == "CC(=O)[O-]"


# --- weak-acid guard (config/protonation.yaml) -----------------------------------------

def _guard() -> list[WeakAcidClass]:
    """The production guard classes, compiled from the same SMARTS as the config."""
    return [
        WeakAcidClass("phenol", Chem.MolFromSmarts("[OX1-]-c1ccccc1"), (
            Chem.MolFromSmarts("[OX1-]c1ccccc1[$([NX3](=O)=O),$([NX3+]([O-])=O)]"),
            Chem.MolFromSmarts("[OX1-]c1ccc([$([NX3](=O)=O),$([NX3+]([O-])=O)])cc1"),
            Chem.MolFromSmarts("[OX1-]c1c([F,Cl,Br,I])cc([F,Cl,Br,I])cc1[F,Cl,Br,I]"),
        )),
        WeakAcidClass("alcohol", Chem.MolFromSmarts("[OX1-][CX4]")),
        WeakAcidClass("amide", Chem.MolFromSmarts(
            "[$([NX2-][CX3]=[OX1]);!$([NX2-]([CX3]=O)[CX3]=O);"
            "!$([NX2-]([CX3]=O)[SX4](=O)=O)]")),
        WeakAcidClass("sulfonamide", Chem.MolFromSmarts(
            "[$([NX2-][SX4](=O)=O);!$([NX2-]([SX4](=O)=O)[CX3]=O)]")),
        WeakAcidClass("aryl_amine", Chem.MolFromSmarts(
            "[$([NX2-]a);!$([NX2-][CX3]=O);!$([NX2-][SX4](=O)=O)]")),
    ]


def _canon(smiles: str) -> str:
    return to_smiles(Chem.MolFromSmiles(smiles))


def test_guard_neutralizes_weak_acids():
    # salicylate phenol, tyrosine phenol, sugar alkoxide, amide, primary sulfonamide,
    # and an amino-pyrimidine are all re-protonated at pH 7.4.
    cases = {
        "O=C([O-])c1ccccc1[O-]": "O=C([O-])c1ccccc1O",          # salicylate: COO- kept, PhO- fixed
        "Cc1ccc([O-])cc1": "Cc1ccc(O)cc1",                       # tyrosine-type phenol
        "OC[C@@H]([O-])CO": "OCC(O)CO",                          # sugar/aliphatic alkoxide
        "CC(=O)[N-]c1ccccc1": "CC(=O)Nc1ccccc1",                 # amide
        "[NH-]S(=O)(=O)c1ccccc1": "NS(=O)(=O)c1ccccc1",          # primary sulfonamide
        "[NH-]c1ncccn1": "Nc1ncccn1",                            # amino-pyrimidine
    }
    guard = _guard()
    for anion, expected in cases.items():
        out, neutralized = neutralize_weak_acids(Chem.MolFromSmiles(anion), guard)
        assert neutralized, f"expected a neutralization for {anion}"
        assert to_smiles(out) == _canon(expected), anion


def test_guard_leaves_genuinely_acidic_and_strong_bases_alone():
    keep = [
        "CC(=O)[O-]",                                            # carboxylate
        "O=P([O-])([O-])OC",                                     # phosphate ester
        "O=[N+]([O-])c1ccc([O-])cc1",                           # p-nitrophenolate (activated)
        "O=[N+]([O-])c1cc([N+](=O)[O-])c([O-])c([N+](=O)[O-])c1",  # picric acid
        "O=C1[N-]S(=O)(=O)c2ccccc21",                            # saccharin (acylsulfonamide)
        "O=C1CCC(=O)[N-]1",                                      # succinimide (imide)
        "[O-]c1cccccc1=S",                                       # tropolone-thione (non-benzene)
        "C[NH3+]",                                               # ammonium (a base, never touched)
    ]
    guard = _guard()
    for smi in keep:
        out, neutralized = neutralize_weak_acids(Chem.MolFromSmiles(smi), guard)
        assert neutralized == [], smi
        assert to_smiles(out) == _canon(smi)


def test_guard_reports_class_and_index_and_is_idempotent():
    mol = Chem.MolFromSmiles("Cc1ccc([O-])cc1")
    out, neutralized = neutralize_weak_acids(mol, _guard())
    assert [n for n, _ in neutralized] == ["phenol"]
    # a second pass finds nothing left to do (idempotent).
    out2, again = neutralize_weak_acids(out, _guard())
    assert again == []
    assert to_smiles(out2) == to_smiles(out)
