"""Unit tests for the pure protonation-state selection (Stage 4 prep) — offline.

These exercise the pKa-ladder walk without pkasolver: ``States`` are faked with RDKit
mols, matching the duck-typed interface ``dominant_microstate_at_ph`` reads.
"""

from __future__ import annotations

from dataclasses import dataclass

import pytest
from rdkit import Chem

from pharmpipe.prep.protonate import (
    dominant_microstate_at_ph,
    largest_fragment,
    protonated_mol,
    to_smiles,
)


@dataclass
class FakeState:
    pka: float
    protonated_mol: Chem.Mol
    deprotonated_mol: Chem.Mol


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
