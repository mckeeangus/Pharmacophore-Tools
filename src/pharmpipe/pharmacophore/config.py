"""Load config/pharmacophore.yaml into typed settings (Stage 4)."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

import yaml

from ..util.paths import CONFIG_DIR


@dataclass
class FeatureConfig:
    fdef: str = "base"
    families: list[str] = field(
        default_factory=lambda: ["Donor", "Acceptor", "LumpedHydrophobe"])
    colors: dict[str, list[float]] = field(default_factory=dict)


@dataclass
class ClusteringConfig:
    method: str = "kmeans_silhouette"
    params: dict = field(default_factory=dict)


@dataclass
class SelectionConfig:
    min_ligands: int = 3
    min_support_fraction: float = 0.5
    min_cluster_size: int = 2
    top_n_per_family: int | None = None
    merge_overlapping: bool = True
    merge_radius: float | None = None


@dataclass
class ToleranceConfig:
    method: str = "rmsd"
    min: float = 1.0
    max: float = 3.0


@dataclass
class PharmacophoreConfig:
    features: FeatureConfig
    clustering: ClusteringConfig
    selection: SelectionConfig
    tolerance: ToleranceConfig


def load_pharmacophore_config(path: str | Path | None = None) -> PharmacophoreConfig:
    path = Path(path) if path else CONFIG_DIR / "pharmacophore.yaml"
    raw = yaml.safe_load(Path(path).read_text(encoding="utf-8")) or {}
    return PharmacophoreConfig(
        features=FeatureConfig(**(raw.get("features") or {})),
        clustering=ClusteringConfig(**(raw.get("clustering") or {})),
        selection=SelectionConfig(**(raw.get("selection") or {})),
        tolerance=ToleranceConfig(**(raw.get("tolerance") or {})),
    )
