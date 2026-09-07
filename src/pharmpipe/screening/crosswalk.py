"""Load + validate the DrugCLIP screening crosswalk (config/screening.yaml).

The crosswalk maps each docked PDB directory to its catalogue slug, site, DrugCLIP index, and
the known-actives cell / literature key. It is curated config; this module only reads it and
*validates* each ``pdb -> index`` pairing by mol_id overlap, so a mis-entered pairing is caught
rather than silently used. IO at the edges (reads csv/yaml); no build logic here.
"""

from __future__ import annotations

import csv
from dataclasses import dataclass
from pathlib import Path

import yaml

from ..util.paths import CONFIG_DIR, REPO_ROOT

RAW_DOCKED_DIR = REPO_ROOT / "out"
RAW_INDEX_DIR = REPO_ROOT / "website_output"
SCREENING_DIR = REPO_ROOT / "data" / "screening"


@dataclass(frozen=True)
class ScreeningTarget:
    """One screening set: a docked PDB dir paired with its DrugCLIP index + comparison refs."""

    key: str            # organised set name -> data/screening/<key>/
    pdb: str            # source dir under out/
    index: str          # DrugCLIP index filename under website_output/
    slug: str           # catalogue target slug (for the known-actives comparison)
    cell: str | None    # built known-actives cell, or None if none exists
    literature: str | None  # key into config/literature_pharmacophores.yaml, or None


def load_crosswalk(path: str | Path | None = None) -> tuple[int, list[ScreeningTarget]]:
    """Return ``(alignment_depth, targets)`` from config/screening.yaml."""
    path = Path(path) if path else CONFIG_DIR / "screening.yaml"
    raw = yaml.safe_load(Path(path).read_text(encoding="utf-8")) or {}
    depth = int(raw.get("alignment_depth", 100))
    targets = [ScreeningTarget(key=t["key"], pdb=t["pdb"], index=t["index"], slug=t["slug"],
                               cell=t.get("cell"), literature=t.get("literature"))
               for t in raw.get("targets", [])]
    return depth, targets


def _index_mol_ids(index_path: Path) -> set[str]:
    """mol_id column of a DrugCLIP index CSV."""
    ids: set[str] = set()
    if not index_path.exists():
        return ids
    with index_path.open(encoding="utf-8") as fh:
        for row in csv.DictReader(fh):
            mid = row.get("mol_id")
            if mid:
                ids.add(mid)
    return ids


def docked_mol_ids(docked_dir: Path) -> set[str]:
    """mol_ids = the ``<mol_id>_docked.sdf`` stems in a docked directory."""
    return {p.name[: -len("_docked.sdf")] for p in docked_dir.glob("*_docked.sdf")}


def validate_overlap(target: ScreeningTarget, docked_dir: Path, index_dir: Path) -> float:
    """Fraction of a target's docked mol_ids present in its paired index (1.0 = all).

    A low value means the crosswalk paired the wrong dir/index — the organiser refuses to
    proceed on such a pairing.
    """
    docked = docked_mol_ids(docked_dir)
    if not docked:
        return 0.0
    idx = _index_mol_ids(index_dir / target.index)
    return len(docked & idx) / len(docked)
