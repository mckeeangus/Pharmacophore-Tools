"""Protonate ligand SMILES to their dominant microstate at a target pH (Stage 4 prep).

The catalogue SMILES are drawn neutral, but H-bond donor/acceptor and ±ionizable
perception depends on the *protonation state* the ligand actually adopts in the binding
site. This module reduces a molecule to its single most-populated microstate at a given
pH from a predicted **pKa ladder** — the dominant species a ligand-based pharmacophore
should be built from.

It is **pure / dependency-light** (RDKit only): it does not import pkasolver. The pKa
ladder is supplied by the caller as a sequence of conjugate acid/base *states* — each a
duck-typed object with ``pka: float``, ``protonated_mol`` and ``deprotonated_mol``
(RDKit mols) — so the model that produced them (pkasolver in
``scripts/protonate_ligands.py``) stays at the IO/heavy-dependency edge and the
state-selection logic here is unit-testable offline.

Selection follows the Henderson–Hasselbalch ordering: walking the ladder from the fully
protonated species, each site whose pKa is below the target pH is deprotonated; the
species reached once every remaining site has pKa above the pH is the dominant one.
"""

from __future__ import annotations

from typing import Protocol

from rdkit import Chem

PHYSIOLOGICAL_PH = 7.4


class ProtonationState(Protocol):
    """The subset of a pkasolver ``States`` this module reads (duck-typed)."""

    pka: float
    protonated_mol: Chem.Mol
    deprotonated_mol: Chem.Mol


def largest_fragment(mol: Chem.Mol) -> Chem.Mol:
    """Return the largest covalent fragment (drops salts/counter-ions)."""
    frags = Chem.GetMolFrags(mol, asMols=True, sanitizeFrags=False)
    if len(frags) <= 1:
        return mol
    return max(frags, key=lambda m: m.GetNumHeavyAtoms())


def dominant_microstate_at_ph(states: list[ProtonationState], ph: float) -> Chem.Mol:
    """The most-populated microstate at ``ph`` from a pKa ladder.

    ``states`` are conjugate acid/base pairs forming a single titration chain (the
    deprotonated mol of one site is the protonated mol of the next). Starting fully
    protonated, every site with ``pka <= ph`` is deprotonated; the species reached when
    a site's ``pka`` first exceeds ``ph`` is returned. Requires a non-empty ladder.
    """
    if not states:
        raise ValueError("no protonation states supplied")
    ordered = sorted(states, key=lambda s: s.pka)
    mol = ordered[0].protonated_mol
    for state in ordered:
        if ph >= state.pka:
            mol = state.deprotonated_mol
        else:
            break
    return mol


def protonated_mol(mol: Chem.Mol, states: list[ProtonationState],
                   ph: float = PHYSIOLOGICAL_PH) -> Chem.Mol:
    """Dominant microstate at ``ph``; the input mol unchanged if it has no ionizable site."""
    if not states:
        return mol
    return dominant_microstate_at_ph(states, ph)


def to_smiles(mol: Chem.Mol) -> str:
    """Canonical SMILES carrying the formal charges of the protonation state."""
    return Chem.MolToSmiles(mol)
