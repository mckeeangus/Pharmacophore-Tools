"""Load the literature pharmacophore references (config/literature_pharmacophores.yaml)."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

import yaml

from ..util.paths import CONFIG_DIR


@dataclass(frozen=True)
class LiteratureModel:
    key: str
    citation: str
    families: list[str]
    key_distances: dict[str, float] = field(default_factory=dict)
    notes: str = ""


def load_literature(path: str | Path | None = None) -> dict[str, LiteratureModel]:
    path = Path(path) if path else CONFIG_DIR / "literature_pharmacophores.yaml"
    raw = yaml.safe_load(Path(path).read_text(encoding="utf-8")) or {}
    return {k: LiteratureModel(key=k, citation=v.get("citation", ""),
                               families=list(v.get("families", [])),
                               key_distances=dict(v.get("key_distances", {}) or {}),
                               notes=v.get("notes", ""))
            for k, v in raw.items()}
