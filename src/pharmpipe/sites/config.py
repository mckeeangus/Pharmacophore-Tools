"""Load config/sites.yaml into typed site definitions."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import yaml

from ..util.paths import CONFIG_DIR


@dataclass
class SiteDefaults:
    pocket_shell_angstrom: float = 10.0
    cutoff_angstrom: float = 8.0
    match_distance_angstrom: float = 2.5
    max_pocket_rmsd_angstrom: float = 3.0
    min_pocket_atoms: int = 8


@dataclass
class SiteDef:
    slug: str
    reference_pdb: str
    anchor_het: str
    notes: str = ""
    # Per-site overrides (fall back to defaults when None).
    pocket_shell_angstrom: float | None = None
    cutoff_angstrom: float | None = None
    match_distance_angstrom: float | None = None
    max_pocket_rmsd_angstrom: float | None = None
    min_pocket_atoms: int | None = None

    def resolved(self, d: SiteDefaults) -> SiteDef:
        return SiteDef(
            slug=self.slug,
            reference_pdb=self.reference_pdb.upper(),
            anchor_het=self.anchor_het.upper(),
            notes=self.notes,
            pocket_shell_angstrom=self.pocket_shell_angstrom or d.pocket_shell_angstrom,
            cutoff_angstrom=self.cutoff_angstrom or d.cutoff_angstrom,
            match_distance_angstrom=self.match_distance_angstrom or d.match_distance_angstrom,
            max_pocket_rmsd_angstrom=self.max_pocket_rmsd_angstrom or d.max_pocket_rmsd_angstrom,
            min_pocket_atoms=self.min_pocket_atoms or d.min_pocket_atoms,
        )


@dataclass
class SitesConfig:
    defaults: SiteDefaults
    sites: dict[str, SiteDef]

    def get(self, slug: str) -> SiteDef | None:
        s = self.sites.get(slug)
        return s.resolved(self.defaults) if s is not None else None


def load_sites(path: str | Path | None = None) -> SitesConfig:
    path = Path(path) if path else CONFIG_DIR / "sites.yaml"
    raw = yaml.safe_load(Path(path).read_text(encoding="utf-8")) or {}
    defaults = SiteDefaults(**(raw.get("defaults") or {}))
    sites: dict[str, SiteDef] = {}
    for slug, body in (raw.get("sites") or {}).items():
        body = dict(body or {})
        sites[slug] = SiteDef(
            slug=slug,
            reference_pdb=str(body.pop("reference_pdb")),
            anchor_het=str(body.pop("anchor_het")),
            notes=str(body.pop("notes", "") or ""),
            **{k: v for k, v in body.items()},
        )
    return SitesConfig(defaults=defaults, sites=sites)
