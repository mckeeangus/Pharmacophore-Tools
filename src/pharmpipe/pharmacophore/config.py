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
    # See config/pharmacophore.yaml `feature_hierarchy` for the co-atom resolution rules.
    feature_hierarchy: list[list[str]] = field(default_factory=list)


@dataclass
class DensityConfig:
    """Knobs for the density-based consensus strategy — see docs/pharmacophore_construction.md
    and config/pharmacophore.yaml `density` for what each one means."""

    voxel: float = 1.0
    bandwidth: float = 1.5
    peak_bandwidth: float | None = None
    occupancy_floor: float = 2.0
    membership_radius: float = 1.5
    direction_min_r: float = 0.5
    scaffold_weighting: bool = False
    merge_radius: float | None = None
    merge_cross_family: bool = False
    merge_exempt_pairs: list[list[str]] = field(default_factory=list)
    resolve_coincident_features: bool = False
    coincidence_radius: float = 2.0
    coincidence_min_support: int = 2

    @property
    def peak_sigma(self) -> float:
        """``peak_bandwidth`` or ``bandwidth`` if unset."""
        return self.peak_bandwidth if self.peak_bandwidth is not None else self.bandwidth


@dataclass
class SelectionConfig:
    min_ligands: int = 3
    min_support_fraction: float = 0.5
    min_cluster_size: int = 2


@dataclass
class ToleranceConfig:
    method: str = "density_quantile"
    quantile: float = 0.75
    min: float = 1.0
    max: float = 3.0


@dataclass
class AlignmentConfig:
    """Knobs for the feature-clique alignment build — see docs/molecule_alignment.md and
    config/pharmacophore.yaml `alignment` for what each one means."""

    n_conformers: int = 64
    energy_window: float = 10.0
    rmsd_prune: float = 0.5
    max_confs: int = 40
    dist_tol: float = 1.5
    min_clique: int = 3
    two_feature_alignment: bool = True
    align_families: list[str] | None = None
    seed_k: int = 5
    max_align_rmsd: float | None = 1.5
    max_clique_nodes: int = 40
    em_iterations: int = 5
    em_tol: float = 0.1
    use_directions: bool = True
    projected_length: float = 1.5
    aromatic_axial: bool = True
    # Seed quality control (align-molecules). When --seed is given, also run the seedless
    # alignment and report which fit the ranked set better (docs/molecule_alignment.md §5).
    compare_seedless: bool = True
    compare_coverage_margin: int = 1     # compounds; a difference this small counts as a tie
    compare_rmsd_margin: float = 0.1     # A; median-RMSD gap this small counts as a tie


@dataclass
class PharmacophoreConfig:
    features: FeatureConfig
    selection: SelectionConfig
    tolerance: ToleranceConfig
    density: DensityConfig
    alignment: AlignmentConfig


def load_pharmacophore_config(path: str | Path | None = None) -> PharmacophoreConfig:
    path = Path(path) if path else CONFIG_DIR / "pharmacophore.yaml"
    raw = yaml.safe_load(Path(path).read_text(encoding="utf-8")) or {}
    return PharmacophoreConfig(
        features=FeatureConfig(**(raw.get("features") or {})),
        selection=SelectionConfig(**(raw.get("selection") or {})),
        tolerance=ToleranceConfig(**(raw.get("tolerance") or {})),
        density=DensityConfig(**(raw.get("density") or {})),
        alignment=AlignmentConfig(**(raw.get("alignment") or {})),
    )
