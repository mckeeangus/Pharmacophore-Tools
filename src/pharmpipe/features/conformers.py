"""Conformer-ensemble generation for the docked-seed feature-alignment build (Stage 4).

The alignment build has no protein frame, so it must superpose ligands by their features.
For that to find the right overlay, each ligand's ensemble must *contain* a near-bioactive
conformer — the single biggest source of silent failure. So we sample generously (ETKDG v3),
minimise with MMFF, keep only a low-energy window, prune near-duplicates, and cap the result.

Pure-ish RDKit (no file IO); deterministic (fixed embed seed). Knobs come from
``AlignmentConfig`` (config/pharmacophore.yaml ``alignment:``), never hardcoded here.
"""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from rdkit import Chem
from rdkit.Chem import AllChem

if TYPE_CHECKING:  # import only for typing — avoids a features<->pharmacophore import cycle
    from ..pharmacophore.config import AlignmentConfig

log = logging.getLogger("pharmpipe.features.conformers")

_EMBED_SEED = 0xC0FFEE  # fixed so the ensemble is reproducible run-to-run


def _mol_from_template(pose: Chem.Mol) -> Chem.Mol | None:
    """A protonation- and stereo-specified molecule read off a docked 3D pose.

    ``AssignStereochemistryFrom3D`` fixes every stereocentre from the coordinates — including
    the **protonated-amine invertomer** (which face the proton sits on), a locked stereocentre
    the neutral index SMILES cannot express. Round-tripping through canonical SMILES carries the
    pose's formal charges (its pH-7.4 protonation) too, so the re-embedded ensemble keeps both
    the docked ionisation and chirality instead of sampling a random invertomer mixture.
    """
    try:
        m = Chem.Mol(pose)
        Chem.AssignStereochemistryFrom3D(m)
        return Chem.MolFromSmiles(Chem.MolToSmiles(Chem.RemoveHs(m)))
    except Exception:  # noqa: BLE001 — any perception failure falls back to the plain SMILES
        return None


def generate_conformers(
    smiles: str, cfg: AlignmentConfig, *, template_pose: Chem.Mol | None = None,
) -> tuple[Chem.Mol, list[int], dict[int, float]] | None:
    """Embed a low-energy conformer ensemble for ``smiles``.

    Returns ``(mol_with_Hs, conformer_ids, rel_energies)`` where the ids are **energy-sorted**
    (lowest first), restricted to within ``cfg.energy_window`` kcal/mol of the minimum — the
    **high-energy discard**, since a ligand is very unlikely to bind in a strained conformation —
    then capped at ``cfg.max_confs``. ``rel_energies`` maps each kept conformer id to its MMFF
    energy relative to the ensemble minimum (kcal/mol). Returns ``None`` when the SMILES is
    unparseable or embedding fails.

    ``template_pose`` (a docked 3D structure) takes precedence over ``smiles``: its protonation
    **and** stereochemistry (incl. the protonated-amine invertomer) are read off the coordinates
    and enforced during embedding, so the ensemble is one diastereomer, not a mixture. Embedding
    uses ETKDG v3 with ``enforceChirality`` (default on), so a specified invertomer is held fixed
    while ring/torsion flexibility is still sampled. Falls back to ``smiles`` if the template
    cannot be perceived.
    """
    mol = _mol_from_template(template_pose) if template_pose is not None else None
    if mol is None:
        mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None
    mol = Chem.AddHs(mol)
    params = AllChem.ETKDGv3()
    params.randomSeed = _EMBED_SEED
    params.pruneRmsThresh = cfg.rmsd_prune
    cids = list(AllChem.EmbedMultipleConfs(mol, numConfs=cfg.n_conformers, params=params))
    if not cids:
        return None
    energies: dict[int, float] = {}
    for cid, (_converged, energy) in zip(cids, AllChem.MMFFOptimizeMoleculeConfs(mol),
                                         strict=False):
        energies[cid] = energy
    if not energies:
        return None
    emin = min(energies.values())
    kept = sorted((c for c in cids if energies[c] - emin <= cfg.energy_window),
                  key=lambda c: energies[c])[:cfg.max_confs]
    return mol, kept, {c: energies[c] - emin for c in kept}
