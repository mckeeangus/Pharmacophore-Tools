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
class DensityConfig:
    """Knobs for the density-based consensus strategy (see pharmacophore/density.py).

    The scientific knobs are the length scale (``voxel`` / ``bandwidth``), the
    ``occupancy_floor``, and the ``membership_radius`` that defines feature support,
    plus a self-contained excluded-volume sub-block. Everything is deterministic
    (fixed grid, no seeding).
    """

    voxel: float = 1.0              # grid spacing (A) = spatial resolution
    bandwidth: float = 1.5          # Gaussian smoothing sigma (A) ~ feature tolerance;
    #                                 sets feature positions/tolerances (the smooth field)
    # Peak-detection length scale (A): the sigma of the SEPARATE field the peaks are read
    # off, and the min spacing between two kept peaks. Decoupled from `bandwidth` so genuine
    # multi-lobe sub-sites resolve as distinct peaks without also sharpening the position/
    # tolerance field. None => fall back to `bandwidth` (the old coupled behaviour).
    peak_bandwidth: float | None = None
    occupancy_floor: float = 2.0    # min summed distinct-molecule weight to keep a peak
    # A ligand SUPPORTS a feature only if it has a feature point within this radius (A)
    # of the peak centre — support = distinct supporting ligands / total ligands. This
    # makes support a hard-membership count robust to far basin outliers.
    membership_radius: float = 1.5
    scaffold_weighting: bool = False  # also weight by inverse scaffold frequency
    # Collapse overlapping features across families so a region of space yields one
    # feature (same rule as the k-means path); excluded-volume spheres are exempt.
    merge_overlapping: bool = True
    merge_radius: float | None = None
    # Compatible co-located family pairs that are NEVER merged into each other (each an
    # unordered pair). A hydroxyl genuinely is both Donor and Acceptor, and an aromatic
    # ring is both Aromatic and a hydrophobe; literature models keep these distinct, so
    # exempting them stops the merge from deleting the weaker half (e.g. an OH acceptor
    # collapsing into its donor). Same-family and non-listed cross-family overlaps still merge.
    merge_exempt_pairs: list[list[str]] = field(default_factory=list)
    # Excluded-volume spheres from receptor atoms in pocket regions no ligand occupies.
    excluded_volume: bool = True
    ev_shell: float = 5.0           # consider protein atoms within this of the ligand cloud
    ev_clearance: float = 2.0       # ...but not within this of any ligand atom (occupied)
    ev_voxel: float = 2.0           # coarsen protein atoms onto this grid -> one sphere each
    ev_radius: float = 1.0          # excluded-volume sphere radius (A)
    ev_max: int = 40                # cap the number of excluded-volume spheres

    @property
    def peak_sigma(self) -> float:
        """Length scale for peak detection: ``peak_bandwidth`` or ``bandwidth`` if unset."""
        return self.peak_bandwidth if self.peak_bandwidth is not None else self.bandwidth


@dataclass
class SelectionConfig:
    min_ligands: int = 3
    min_support_fraction: float = 0.5
    min_cluster_size: int = 2


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
    selection: SelectionConfig
    tolerance: ToleranceConfig
    density: DensityConfig


def load_pharmacophore_config(path: str | Path | None = None) -> PharmacophoreConfig:
    path = Path(path) if path else CONFIG_DIR / "pharmacophore.yaml"
    raw = yaml.safe_load(Path(path).read_text(encoding="utf-8")) or {}
    return PharmacophoreConfig(
        features=FeatureConfig(**(raw.get("features") or {})),
        selection=SelectionConfig(**(raw.get("selection") or {})),
        tolerance=ToleranceConfig(**(raw.get("tolerance") or {})),
        density=DensityConfig(**(raw.get("density") or {})),
    )
