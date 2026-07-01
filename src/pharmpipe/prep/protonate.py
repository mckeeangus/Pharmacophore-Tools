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

**Weak-acid guard.** pkasolver systematically *over-deprotonates* weak acids (O–H, N–H)
that sit on complex, poly-ionizable scaffolds — phenols, aliphatic/sugar alcohols,
amides, primary sulfonamides, amino-heteroaromatics — because adjacent-charge, H-bond,
and second/third-ionization (macrostate) effects are invisible to a molecular-graph GNN.
These classes have aqueous pKa well above 7.4, so :func:`neutralize_weak_acids`
re-protonates any that survive the walk as their conjugate base, unless they match a
genuinely-acidic structural exception. It is purely *additive* (only ever adds a proton),
so it cannot disturb carboxylates, phosphates, protonated amines, or anything pkasolver
handles correctly. The class definitions live in ``config/protonation.yaml`` — a general
structural prior, never a per-compound pKa value.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Protocol

from rdkit import Chem

PHYSIOLOGICAL_PH = 7.4


class ProtonationState(Protocol):
    """The subset of a pkasolver ``States`` this module reads (duck-typed)."""

    pka: float
    protonated_mol: Chem.Mol
    deprotonated_mol: Chem.Mol


@dataclass(frozen=True)
class WeakAcidClass:
    """One weak-acid class the guard re-protonates (from ``config/protonation.yaml``).

    ``anion`` is a SMARTS whose **first atom is the conjugate-base heteroatom** to
    re-protonate; ``exceptions`` are SMARTS (same anchor) for genuinely-acidic members
    that keep their deprotonation.
    """

    name: str
    anion: Chem.Mol
    exceptions: tuple[Chem.Mol, ...] = field(default_factory=tuple)


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


def _anchor_atoms(mol: Chem.Mol, pattern: Chem.Mol) -> set[int]:
    """Indices matched by ``pattern``'s first (anchor) atom."""
    if pattern is None:
        return set()
    return {match[0] for match in mol.GetSubstructMatches(pattern)}


def neutralize_weak_acids(
    mol: Chem.Mol, classes: list[WeakAcidClass],
) -> tuple[Chem.Mol, list[tuple[str, int]]]:
    """Re-protonate every unactivated weak-acid conjugate base in ``mol``.

    For each class, the anchor atom of every ``anion`` match that is not covered by an
    ``exceptions`` match and still carries a −1 formal charge is neutralized (charge → 0,
    one H added). Purely additive — no proton is ever removed. Returns the (possibly new)
    mol and the ``(class_name, atom_idx)`` list neutralized. On the rare sanitize failure
    the input mol is returned untouched.
    """
    to_fix: dict[int, str] = {}
    for cls in classes:
        excepted: set[int] = set()
        for exc in cls.exceptions:
            excepted |= _anchor_atoms(mol, exc)
        for idx in _anchor_atoms(mol, cls.anion) - excepted:
            if mol.GetAtomWithIdx(idx).GetFormalCharge() == -1:
                to_fix.setdefault(idx, cls.name)
    if not to_fix:
        return mol, []
    rw = Chem.RWMol(mol)
    for idx in to_fix:
        atom = rw.GetAtomWithIdx(idx)
        atom.SetFormalCharge(0)
        atom.SetNumExplicitHs(atom.GetNumExplicitHs() + 1)
    out = rw.GetMol()
    try:
        Chem.SanitizeMol(out)
    except (Chem.AtomValenceException, Chem.KekulizeException, ValueError):
        return mol, []
    return out, sorted((name, idx) for idx, name in to_fix.items())


def to_smiles(mol: Chem.Mol) -> str:
    """Canonical SMILES carrying the formal charges of the protonation state."""
    return Chem.MolToSmiles(mol)
