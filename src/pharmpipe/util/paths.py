"""Canonical filesystem locations for the pipeline.

Resolved relative to the repository root so the same code works locally and on
Gadi. ``data/`` is gitignored (large caches + extracted ligands); ``catalogue/``
is the tracked deliverable.
"""

from __future__ import annotations

from pathlib import Path

# src/pharmpipe/util/paths.py -> repo root is three parents up from this file's dir.
REPO_ROOT = Path(__file__).resolve().parents[3]

CONFIG_DIR = REPO_ROOT / "config"
CATALOGUE_DIR = REPO_ROOT / "catalogue"
DATA_DIR = REPO_ROOT / "data"
TARGETS_DATA_DIR = DATA_DIR / "targets"

# Network/API response cache (entries, chem components, mmCIF, CCD templates).
CACHE_DIR = DATA_DIR / "_cache"


def target_data_dir(slug: str) -> Path:
    """Per-target data directory: data/targets/<slug>/."""
    return TARGETS_DATA_DIR / slug


def target_structures_dir(slug: str) -> Path:
    return target_data_dir(slug) / "structures"


def target_mol2_dir(slug: str) -> Path:
    return target_data_dir(slug) / "ligands" / "mol2"


def target_aligned_mol2_dir(slug: str) -> Path:
    """Site-filtered ligand poses transformed into the reference frame."""
    return target_data_dir(slug) / "ligands" / "aligned_mol2"


def target_reference_pdb(slug: str) -> Path:
    """The site reference protein (scaffold the aligned ligands overlay onto)."""
    return target_data_dir(slug) / "reference.pdb"


def target_session_pml(slug: str) -> Path:
    return target_data_dir(slug) / f"{slug}_aligned.pml"


def target_session_pse(slug: str) -> Path:
    return target_data_dir(slug) / f"{slug}_aligned.pse"


def target_catalogue_dir(slug: str) -> Path:
    return CATALOGUE_DIR / slug


def ensure_dir(path: Path) -> Path:
    path.mkdir(parents=True, exist_ok=True)
    return path
