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
    # Co-atom feature hierarchy: when one atom is perceived as several families, keep
    # only the highest-priority family in each group (higher subsumes lower on a shared
    # atom). Each inner list is ordered highest-priority first. Resolution fires ONLY
    # for co-incident (shared-atom) dual classifications; genuine dual roles (a hydroxyl
    # as Donor+Acceptor, a ring heteroatom as Aromatic+Acceptor/Donor) are absent from
    # the groups and so preserved. See config/pharmacophore.yaml `feature_hierarchy`.
    feature_hierarchy: list[list[str]] = field(default_factory=list)


@dataclass
class ClusteringConfig:
    method: str = "kmeans_silhouette"
    params: dict = field(default_factory=dict)


@dataclass
class DensityConfig:
    """Knobs for the density-based consensus strategy (see pharmacophore/density.py).

    By design there are only two scientific knobs — a single length scale
    (``voxel`` / ``bandwidth``) and the ``occupancy_floor`` — plus a self-contained
    excluded-volume sub-block. Everything is deterministic (fixed grid, no seeding).
    """

    voxel: float = 1.0              # grid spacing (A) = spatial resolution
    bandwidth: float = 1.5          # Gaussian smoothing sigma (A) ~ feature tolerance
    peak_separation: float = 1.5    # min centre-to-centre distance (A) between two kept
    #                                 peaks of one family (own knob; set = bandwidth)
    occupancy_floor: float = 2.0    # min summed distinct-molecule weight to keep a peak
    scaffold_weighting: bool = False  # also weight by inverse scaffold frequency
    # Collapse overlapping features across families so a region of space yields one
    # feature (same rule as the k-means path); excluded-volume spheres are exempt.
    merge_overlapping: bool = True
    merge_radius: float | None = None
    # Excluded-volume spheres from receptor atoms in pocket regions no ligand occupies.
    excluded_volume: bool = True
    ev_shell: float = 5.0           # consider protein atoms within this of the ligand cloud
    ev_clearance: float = 2.0       # ...but not within this of any ligand atom (occupied)
    ev_voxel: float = 2.0           # coarsen protein atoms onto this grid -> one sphere each
    ev_radius: float = 1.0          # excluded-volume sphere radius (A)
    ev_max: int = 40                # cap the number of excluded-volume spheres


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
    # "density_quantile": radius enclosing `quantile` of the feature's (density-weighted)
    # mass from the centre — robust to the far points still assigned to the cluster.
    # "rmsd": root-mean-square point-to-centre distance (the tail-sensitive alternative).
    method: str = "density_quantile"
    quantile: float = 0.75
    min: float = 1.0
    max: float = 3.0


@dataclass
class PharmacophoreConfig:
    features: FeatureConfig
    clustering: ClusteringConfig
    selection: SelectionConfig
    tolerance: ToleranceConfig
    density: DensityConfig
    # Which consensus strategy turns per-molecule feature points into consensus
    # features: "kmeans" (silhouette k-means, the default) or "density" (Gaussian
    # occupancy field). Both honour the same in/out contract.
    consensus_method: str = "kmeans"


def load_pharmacophore_config(path: str | Path | None = None) -> PharmacophoreConfig:
    path = Path(path) if path else CONFIG_DIR / "pharmacophore.yaml"
    raw = yaml.safe_load(Path(path).read_text(encoding="utf-8")) or {}
    return PharmacophoreConfig(
        features=FeatureConfig(**(raw.get("features") or {})),
        clustering=ClusteringConfig(**(raw.get("clustering") or {})),
        selection=SelectionConfig(**(raw.get("selection") or {})),
        tolerance=ToleranceConfig(**(raw.get("tolerance") or {})),
        density=DensityConfig(**(raw.get("density") or {})),
        consensus_method=raw.get("consensus_method", "kmeans"),
    )
