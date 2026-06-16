"""Load config/pockets.yaml — clustering thresholds + pocket-naming knowledge.

Pocket discovery is geometric (see :mod:`pharmpipe.groups.pocket`); this config
only names the clusters and records what we expect, so departures are visible.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

import yaml

from ..util.paths import CONFIG_DIR


@dataclass
class PocketDefaults:
    contact_angstrom: float = 4.5
    jaccard_min: float = 0.30
    overlap_min: float = 0.60
    min_shared_residues: int = 5
    min_pocket_poses: int = 3


@dataclass
class PocketDef:
    slug: str
    primary_label: str = "active_site"
    collapse_to_primary: bool = False
    # When true, re-superpose each pose's *whole native assembly* onto the
    # reference (instead of the Stage-2 local pocket fit) so distinct pockets land
    # at their true subunit interfaces. Use only for genuine multi-pocket targets;
    # a global fit degrades low-identity cross-species surrogate overlays.
    realign_global: bool = False
    expected_pockets: list[str] = field(default_factory=list)
    # secondary label -> diagnostic HET codes
    markers: dict[str, list[str]] = field(default_factory=dict)
    notes: str = ""

    def label_for_markers(self, het_codes: set[str]) -> str | None:
        """Secondary-pocket label whose markers appear in ``het_codes``, if any."""
        for label, markers in self.markers.items():
            if het_codes & {m.upper() for m in markers}:
                return label
        return None


@dataclass
class PocketsConfig:
    defaults: PocketDefaults
    targets: dict[str, PocketDef]

    def get(self, slug: str) -> PocketDef:
        return self.targets.get(slug, PocketDef(slug=slug))


def load_pockets(path: str | Path | None = None) -> PocketsConfig:
    path = Path(path) if path else CONFIG_DIR / "pockets.yaml"
    raw = yaml.safe_load(Path(path).read_text(encoding="utf-8")) or {}
    defaults = PocketDefaults(**(raw.get("defaults") or {}))
    targets: dict[str, PocketDef] = {}
    for slug, body in (raw.get("targets") or {}).items():
        body = body or {}
        markers = {label: list((spec or {}).get("marker_hets", []))
                   for label, spec in (body.get("pockets") or {}).items()}
        targets[slug] = PocketDef(
            slug=slug,
            primary_label=str(body.get("primary_label", "active_site")),
            collapse_to_primary=bool(body.get("collapse_to_primary", False)),
            realign_global=bool(body.get("realign_global", False)),
            expected_pockets=list(body.get("expected_pockets", [])),
            markers=markers,
            notes=str(body.get("notes", "") or ""),
        )
    return PocketsConfig(defaults=defaults, targets=targets)
