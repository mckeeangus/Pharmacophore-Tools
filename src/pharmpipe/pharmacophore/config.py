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
    # Collapse overlapping features so a region of space is not double-counted; excluded-volume
    # spheres are exempt.
    merge_overlapping: bool = True
    merge_radius: float | None = None
    # Whether the overlap merge acts ACROSS families. False (default) = merge only features of the
    # SAME family (de-duplicate co-located same-type peaks); different families at one spot are ALL
    # kept, because a single atom/region genuinely can be several pharmacophore types at once (a
    # pyridine N is both Aromatic and Acceptor; a hydroxyl both Donor and Acceptor) and literature
    # models keep them distinct. True restores the old "one feature per region" cross-family merge
    # (dominant family wins), honouring `merge_exempt_pairs`.
    merge_cross_family: bool = False
    # Only used when `merge_cross_family` is True: cross-family pairs never merged into each other.
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
class AlignmentConfig:
    """Knobs for the docked-seed feature-alignment build (see pharmacophore/align.py).

    Consumed ONLY by the ``--seed-docked`` minimum-docking mode; it does not touch the
    density/selection/tolerance knobs the catalogue and other modes use, so the two paths
    stay orthogonal. ``conformers`` covers the per-ligand ensemble; ``clique`` covers the
    feature-clique correspondence search.
    """

    # Conformer ensemble (RDKit ETKDG v3 + MMFF): the bioactive conformer must be present,
    # so sample generously, keep only a low-energy window, prune near-duplicates, then cap.
    n_conformers: int = 64          # embeds attempted per ligand
    energy_window: float = 10.0     # keep conformers within this (kcal/mol) of the minimum
    rmsd_prune: float = 0.5         # ETKDG pruneRmsThresh (A) — drop near-duplicate embeds
    max_confs: int = 40             # cap the kept ensemble (energy-sorted)
    # Feature-clique alignment: two features correspond only if same-family and their
    # intra-molecular distances agree within `dist_tol`; a rigid alignment needs at least
    # `min_clique` mutually-consistent correspondences (3 => a determined 3-D transform).
    dist_tol: float = 1.5           # correspondence distance tolerance (A)
    min_clique: int = 3             # minimum mutually-consistent feature matches to align
    # Families used to drive the alignment (a subset of features.families). None => all of
    # features.families. Restricting to the pharmacophorically-defining families keeps the
    # correspondence graph small and the cliques meaningful.
    align_families: list[str] | None = None
    seed_k: int = 5                 # docked poses used to seed the model (bioactive frame)
    # A compound is only folded into the growing model if its best clique superposition RMSD is
    # <= this (A); poorer fits are dropped (recorded aligned=False), so a bad alignment cannot
    # corrupt the running consensus. None disables the gate (accept any >= min_clique clique).
    max_align_rmsd: float | None = 1.5
    # Correspondence-graph size above which the clique search switches from exact (Bron-Kerbosch,
    # exponential) to a bounded greedy search — keeps alignment tractable for feature-rich ligands
    # (many H-bond/aromatic features give a large graph). Small molecules stay under it (exact).
    max_clique_nodes: int = 40
    # EM refinement: after the initial rank-order growing pass, re-align every compound's ensemble
    # to the CURRENT consensus (re-selecting its best conformer) and rebuild, up to `em_iterations`
    # times, stopping early when the largest consensus feature-centre shift is below `em_tol` (A).
    # This removes the effect of a sub-optimal discrete conformer chosen early and reduces the
    # dependence on the seed/order. 0 disables EM (single growing pass only).
    em_iterations: int = 5
    em_tol: float = 0.1
    # Orientation-aware matching: when true, the superposition also fits H-bond donor/acceptor
    # **projected points** (feature centre + `projected_length` A along its lone-pair / D-H vector),
    # so a directional feature must agree in ORIENTATION, not just position — this resolves the
    # ring-flipped acceptor that positional matching averages away. Perceived directions come from
    # features/extract.py. False = positional matching only (the pre-directional behaviour).
    use_directions: bool = True
    projected_length: float = 1.5


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
