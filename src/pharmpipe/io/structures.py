"""mmCIF download (cached) and parsing via gemmi."""

from __future__ import annotations

import logging
from pathlib import Path

import gemmi

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
