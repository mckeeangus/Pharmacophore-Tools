"""mmCIF download (cached) and parsing via gemmi."""

from __future__ import annotations

import logging
from pathlib import Path

import gemmi
import numpy as np

from ..util import http
from ..util.paths import ensure_dir, target_structures_dir

log = logging.getLogger("pharmpipe.structures")

MMCIF_URL = "https://files.rcsb.org/download/{pdb_id}.cif"


def download_mmcif(pdb_id: str, slug: str, cfg: http.HttpConfig) -> Path | None:
    """Download (or reuse cached) mmCIF into data/targets/<slug>/structures/."""
    pdb_id = pdb_id.upper()
    out = ensure_dir(target_structures_dir(slug)) / f"{pdb_id}.cif"
    if out.exists() and out.stat().st_size > 0:
        return out
    text = http.get_text(MMCIF_URL.format(pdb_id=pdb_id), cfg,
                         category="mmcif", cache_key=f"cif:{pdb_id}", allow_404=True)
    if text is None:
        log.warning("mmCIF for %s not available (404)", pdb_id)
        return None
    out.write_text(text, encoding="utf-8")
    return out


def read_structure(path: Path) -> gemmi.Structure:
    st = gemmi.read_structure(str(path))
    st.setup_entities()
    return st


def read_protein_atom_coords(path: Path) -> np.ndarray:
    """Heavy-atom coordinates of the polymer (protein) chains, shape ``(n, 3)``.

    Used as the source of receptor atoms for excluded-volume spheres. The reference
    PDB is already in the binding-site-local frame the aligned ligands share, so its
    polymer atoms need no further transform. Waters, ligands/HETATM, and hydrogens
    are dropped; only the first model is read.
    """
    st = read_structure(path)
    if not len(st):
        return np.empty((0, 3), dtype=float)
    coords: list[tuple[float, float, float]] = []
    for chain in st[0]:
        polymer = chain.get_polymer()
        if not len(polymer):                       # skip non-polymer (water/ligand) chains
            continue
        for residue in polymer:
            for atom in residue:
                if atom.is_hydrogen():
                    continue
                p = atom.pos
                coords.append((p.x, p.y, p.z))
    return np.array(coords, dtype=float) if coords else np.empty((0, 3), dtype=float)
