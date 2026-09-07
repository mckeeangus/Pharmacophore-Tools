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


def generate_conformers(
    smiles: str, cfg: AlignmentConfig,
) -> tuple[Chem.Mol, list[int], dict[int, float]] | None:
    """Embed a low-energy conformer ensemble for ``smiles``.

    Returns ``(mol_with_Hs, conformer_ids, rel_energies)`` where the ids are **energy-sorted**
    (lowest first), restricted to within ``cfg.energy_window`` kcal/mol of the minimum — the
    **high-energy discard**, since a ligand is very unlikely to bind in a strained conformation —
    then capped at ``cfg.max_confs``. ``rel_energies`` maps each kept conformer id to its MMFF
    energy relative to the ensemble minimum (kcal/mol). Returns ``None`` when the SMILES is
    unparseable or embedding fails.
    """
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
