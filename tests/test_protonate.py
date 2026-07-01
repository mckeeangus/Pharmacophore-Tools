"""Unit tests for the pure protonation-state selection (Stage 4 prep) — offline.

These exercise the pKa-ladder walk without pkasolver: ``States`` are faked with RDKit
mols, matching the duck-typed interface ``dominant_microstate_at_ph`` reads.
"""

from __future__ import annotations

from dataclasses import dataclass

import pytest
from rdkit import Chem

from pharmpipe.prep.protonate import (
    PhenolRule,
    apply_phenol_correction,
    dominant_microstate_at_ph,
    largest_fragment,
    neutralize_unactivated_phenolates,
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


# --- phenol pKa correction (config/protonation.yaml) -----------------------------------

def _phenol_rule() -> PhenolRule:
    o = "[$([OX2H1]),$([OX1-])]"
    return PhenolRule(
        phenol=Chem.MolFromSmarts(f"{o}-c1ccccc1"),
        reference_pka=10.0,
        activating=(
            Chem.MolFromSmarts(f"{o}c1ccccc1[$([NX3](=O)=O),$([NX3+]([O-])=O)]"),
            Chem.MolFromSmarts(f"{o}c1ccc([$([NX3](=O)=O),$([NX3+]([O-])=O)])cc1"),
        ),
    )


def _phenol_oxygen(smiles: str) -> tuple[Chem.Mol, int]:
    """A mol and the index of its (first) phenolic -OH oxygen."""
    mol = Chem.MolFromSmiles(smiles)
    for atom in mol.GetAtoms():
        if (atom.GetSymbol() == "O" and atom.GetTotalNumHs() >= 1
                and any(n.GetIsAromatic() for n in atom.GetNeighbors())):
            return mol, atom.GetIdx()
    raise AssertionError("no phenolic oxygen")


def test_unactivated_phenol_pka_is_lifted_to_reference():
    # salicylate phenol: pkasolver's 4.71 -> reference 10.0, so it stays protonated.
    prot, idx = _phenol_oxygen("O=C([O-])c1ccccc1O")
    deprot = Chem.MolFromSmiles("O=C([O-])c1ccccc1[O-]")
    state = FakeState(4.71, prot, deprot, reaction_center_idx=idx)
    corrected, overrides = apply_phenol_correction([state], _phenol_rule())
    assert overrides == [(idx, 4.71, 10.0)]
    assert corrected[0].pka == 10.0
    # ...and at pH 7.4 the phenol is now kept protonated.
    assert to_smiles(dominant_microstate_at_ph(corrected, 7.4)) == "O=C([O-])c1ccccc1O"


def test_activated_phenol_keeps_ml_pka():
    # p-nitrophenol matches the activating list -> pkasolver's value is untouched.
    prot, idx = _phenol_oxygen("O=[N+]([O-])c1ccc(O)cc1")
    deprot = Chem.MolFromSmiles("O=[N+]([O-])c1ccc([O-])cc1")
    state = FakeState(7.15, prot, deprot, reaction_center_idx=idx)
    corrected, overrides = apply_phenol_correction([state], _phenol_rule())
    assert overrides == []
    assert corrected[0].pka == 7.15


def test_non_phenol_site_untouched():
    # a carboxyl reaction centre is not a phenol -> never corrected.
    mol = Chem.MolFromSmiles("O=C(O)c1ccccc1O")
    carboxyl_o = next(a.GetIdx() for a in mol.GetAtoms()
                      if a.GetSymbol() == "O" and a.GetTotalNumHs() == 1
                      and not any(n.GetIsAromatic() for n in a.GetNeighbors()))
    state = FakeState(3.42, mol, Chem.MolFromSmiles("O=C([O-])c1ccccc1O"),
                      reaction_center_idx=carboxyl_o)
    corrected, overrides = apply_phenol_correction([state], _phenol_rule())
    assert overrides == []
    assert corrected[0].pka == 3.42


def test_backstop_neutralizes_unactivated_phenolate():
    # a bare tyrosine-type phenolate (no re-protonation rung available) is protonated…
    mol = Chem.MolFromSmiles("Cc1ccc([O-])cc1")
    out, neutralized = neutralize_unactivated_phenolates(mol, _phenol_rule())
    assert len(neutralized) == 1
    assert to_smiles(out) == to_smiles(Chem.MolFromSmiles("Cc1ccc(O)cc1"))


def test_backstop_leaves_activated_and_nonbenzene_phenolates():
    # picric acid (2,4,6-trinitrophenolate) is genuinely acidic -> untouched…
    picric = Chem.MolFromSmiles("O=[N+]([O-])c1cc([N+](=O)[O-])c([O-])c([N+](=O)[O-])c1")
    out, neutralized = neutralize_unactivated_phenolates(picric, _phenol_rule())
    assert neutralized == []
    # …and a non-benzene enolate (tropolone-thione) is left to pkasolver.
    trop = Chem.MolFromSmiles("[O-]c1cccccc1=S")
    out2, neutralized2 = neutralize_unactivated_phenolates(trop, _phenol_rule())
    assert neutralized2 == []
