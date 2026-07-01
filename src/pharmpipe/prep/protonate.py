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

from dataclasses import dataclass
from typing import Protocol

from rdkit import Chem

PHYSIOLOGICAL_PH = 7.4


class ProtonationState(Protocol):
    """The subset of a pkasolver ``States`` this module reads (duck-typed)."""

    pka: float
    protonated_mol: Chem.Mol
    deprotonated_mol: Chem.Mol


@dataclass(frozen=True)
class _CorrectedState:
    """Immutable stand-in for a pkasolver ``States`` with a substituted ``pka``.

    The phenol correction rewrites a site's pKa without mutating pkasolver's object;
    it carries just the fields ``dominant_microstate_at_ph`` reads plus the reaction
    centre so a chain of corrections stays inspectable.
    """

    pka: float
    protonated_mol: Chem.Mol
    deprotonated_mol: Chem.Mol
    reaction_center_idx: int = -1


@dataclass(frozen=True)
class PhenolRule:
    """Compiled phenol pKa correction (from ``config/protonation.yaml``).

    ``phenol`` and each pattern in ``activating`` are SMARTS whose **first atom is the
    phenolic oxygen**, so a match anchors the rule to one specific ionization site.
    """

    phenol: Chem.Mol
    reference_pka: float
    activating: tuple[Chem.Mol, ...] = ()


def _anchor_oxygens(mol: Chem.Mol, pattern: Chem.Mol) -> set[int]:
    """Atom indices matched by ``pattern``'s first (anchor) atom."""
    if pattern is None:
        return set()
    return {match[0] for match in mol.GetSubstructMatches(pattern)}


def phenolic_oxygens(mol: Chem.Mol, rule: PhenolRule) -> set[int]:
    """Indices of phenolic-hydroxyl oxygens in ``mol`` under ``rule``."""
    return _anchor_oxygens(mol, rule.phenol)


def activated_oxygens(mol: Chem.Mol, rule: PhenolRule) -> set[int]:
    """Phenolic oxygens whose ring bears an activating EWG (keep the ML pKa)."""
    out: set[int] = set()
    for pattern in rule.activating:
        out |= _anchor_oxygens(mol, pattern)
    return out


def apply_phenol_correction(
    states: list[ProtonationState], rule: PhenolRule,
) -> tuple[list[ProtonationState], list[tuple[int, float, float]]]:
    """Reassign the reference pKa to every *unactivated* phenol site in ``states``.

    A state whose ``reaction_center_idx`` is a phenolic oxygen that is **not** in an
    activating environment gets ``rule.reference_pka`` (so the Henderson–Hasselbalch
    walk keeps the phenol protonated at physiological pH); activated phenols (nitro-,
    cyano-, polyhalo-substituted) and all non-phenol sites are left untouched. Returns
    the corrected states and a list of ``(atom_idx, old_pka, new_pka)`` overrides for
    provenance. Pure: pkasolver's objects are not mutated.
    """
    corrected: list[ProtonationState] = []
    overrides: list[tuple[int, float, float]] = []
    for state in states:
        idx = getattr(state, "reaction_center_idx", -1)
        mol = state.protonated_mol
        is_phenol = (
            mol is not None
            and 0 <= idx < mol.GetNumAtoms()
            and idx in phenolic_oxygens(mol, rule)
            and idx not in activated_oxygens(mol, rule)
        )
        if is_phenol and abs(state.pka - rule.reference_pka) > 1e-9:
            overrides.append((idx, state.pka, rule.reference_pka))
            corrected.append(_CorrectedState(
                pka=rule.reference_pka,
                protonated_mol=mol,
                deprotonated_mol=state.deprotonated_mol,
                reaction_center_idx=idx,
            ))
        else:
            corrected.append(state)
    return corrected, overrides


def neutralize_unactivated_phenolates(
    mol: Chem.Mol, rule: PhenolRule,
) -> tuple[Chem.Mol, list[int]]:
    """Protonate every unactivated benzene-phenolate oxygen in ``mol``.

    A backstop to the rung correction: pkasolver (via dimorphite) sometimes deprotonates
    a phenol in its baseline pH-7 microstate without emitting a re-protonation rung, so
    the pKa edit in :func:`apply_phenol_correction` has nothing to act on and the
    phenolate survives the ladder walk. This operates on the *final* microstate instead —
    any ``[O-]`` on a benzene ring that is not in an activating environment is set back to
    the neutral hydroxyl. Activated phenolates (nitro-, cyano-, polyhalo-) are left as
    predicted. Returns the (possibly new) mol and the indices neutralized.
    """
    targets = sorted(
        idx for idx in phenolic_oxygens(mol, rule) - activated_oxygens(mol, rule)
        if mol.GetAtomWithIdx(idx).GetFormalCharge() == -1
    )
    if not targets:
        return mol, []
    rw = Chem.RWMol(mol)
    for idx in targets:
        atom = rw.GetAtomWithIdx(idx)
        atom.SetFormalCharge(0)
        atom.SetNumExplicitHs(atom.GetNumExplicitHs() + 1)
    out = rw.GetMol()
    Chem.SanitizeMol(out)
    return out, targets


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
