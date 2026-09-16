"""Density-based consensus strategy for ensemble pharmacophores (Stage 4, pure core).

The sole consensus strategy: it turns per-molecule, binding-site-aligned feature points
into consensus features by estimating, per feature type, a **Gaussian-smoothed occupancy
field** (a KDE) over a fixed voxel grid, then reading consensus features off the field's
local maxima. Each conserved sub-site is its own peak, so multiple features of one type
fall out natively with no *k* to pick, and the whole procedure is deterministic (fixed
grid, bandwidth and threshold; no random seeding).

The unit of evidence is the **distinct molecule**, not the raw point: every point is
weighted by ``1 / (points that molecule contributes to this feature type)`` so a
molecule that happens to place many points of one type cannot dominate the field
(optionally also by inverse scaffold frequency). A peak is kept only if the summed
distinct-molecule weight in its basin clears an occupancy floor **and** its
membership-radius support clears the support floor.

Precedent: dynophore cloud -> super-feature with occurrence frequency (Wolber lab);
field-maximum extraction (GBPM; Baroni et al. FLAPpharm); Gaussian feature-density
molecular representation (Tanrikulu & Schneider); occupancy/frequency thresholding
across complexes (REPHARMBLE; SARS-CoV-2 Mpro consensus pharmacophores).
"""

from __future__ import annotations

from dataclasses import asdict, replace

import numpy as np
from scipy.ndimage import gaussian_filter, maximum_filter

from ..features.extract import FeatureTable
from .build import (
    BuildResult,
    ClusterAssignment,
    _merge_overlapping,
    _merge_records,
    feature_radius,
    finalize_features,
)
from .config import DensityConfig, ToleranceConfig
from .model import Pharmacophore, PharmacophoreFeature

# --- molecule weighting ------------------------------------------------------

def _molecule_weights(ligands: list[str],
                      scaffold_freq: dict[str, int] | None) -> np.ndarray:
    """Per-point weight so each *molecule* contributes one unit of evidence.

    ``w_i = 1 / (points molecule m(i) contributes to this family)``; optionally also
    divided by the molecule's scaffold frequency so over-represented scaffolds do not
    bias the field. The weights of one molecule's points therefore sum to 1 (or to
    ``1 / scaffold_freq``), making the field a map of distinct-molecule occurrence.
    """
    counts: dict[str, int] = {}
    for lig in ligands:
        counts[lig] = counts.get(lig, 0) + 1
    w = np.array([1.0 / counts[lig] for lig in ligands], dtype=float)
    if scaffold_freq:
        w = w * np.array([1.0 / max(scaffold_freq.get(lig, 1), 1) for lig in ligands])
    return w


# --- occupancy field ---------------------------------------------------------

def _occupancy_field(coords: np.ndarray, weights: np.ndarray, dcfg: DensityConfig
                     ) -> tuple[np.ndarray, np.ndarray]:
    """Accumulate molecule-weighted points into a grid and Gaussian-smooth it.

    Returns the field array and the grid origin (corner of voxel ``[0,0,0]``).
    Smoothing a weighted histogram with ``sigma = bandwidth / voxel`` is an
    equivalent, deterministic kernel-density estimate on the grid.
    """
    pad = dcfg.bandwidth * 3.0 + dcfg.voxel
    origin = coords.min(axis=0) - pad
    extent = (coords.max(axis=0) + pad) - origin
    shape = np.maximum(np.ceil(extent / dcfg.voxel).astype(int) + 1, 1)
    grid = np.zeros(tuple(shape), dtype=float)
    idx = np.clip(np.floor((coords - origin) / dcfg.voxel).astype(int), 0, shape - 1)
    np.add.at(grid, (idx[:, 0], idx[:, 1], idx[:, 2]), weights)
    field = gaussian_filter(grid, sigma=dcfg.bandwidth / dcfg.voxel, mode="constant")
    return field, origin


def _voxel_centers(idx: np.ndarray, origin: np.ndarray, voxel: float) -> np.ndarray:
    return origin + (idx + 0.5) * voxel


def _local_maxima(field: np.ndarray, origin: np.ndarray, dcfg: DensityConfig
                  ) -> np.ndarray:
    """All local maxima of the field, as world coordinates, deduped by bandwidth.

    Peaks closer than the smoothing bandwidth cannot be resolved, so near-coincident
    maxima are collapsed keeping the taller — the only place the field is post-filtered.
    The min peak spacing is the ``bandwidth`` itself: the Gaussian smoothing (sigma =
    bandwidth) is the field's resolution limit, so two maxima nearer than that are the
    same site and a separate spacing knob would only over-split single lobes.
    """
    if field.max() <= 0:
        return np.empty((0, 3), dtype=float)
    eps = field.max() * 1e-3
    peak_mask = (field == maximum_filter(field, size=3, mode="constant")) & (field > eps)
    peak_idx = np.argwhere(peak_mask)
    heights = field[peak_mask]
    order = np.argsort(heights)[::-1]               # tallest first
    coords = _voxel_centers(peak_idx[order], origin, dcfg.voxel)
    kept: list[np.ndarray] = []
    for c in coords:
        if all(np.linalg.norm(c - k) >= dcfg.bandwidth for k in kept):
            kept.append(c)
    return np.array(kept, dtype=float) if kept else np.empty((0, 3), dtype=float)


def _nearest(coords: np.ndarray, peaks: np.ndarray) -> np.ndarray:
    """Index of the nearest peak for each row of ``coords`` (watershed-by-proximity)."""
    d2 = ((coords[:, None, :] - peaks[None, :, :]) ** 2).sum(axis=2)
    return d2.argmin(axis=1)


# --- per-family consensus ----------------------------------------------------

def _family_density(family: str, coords: np.ndarray, ligands: list[str],
                    weights: np.ndarray, n_ligands: int, dcfg: DensityConfig,
                    tol: ToleranceConfig, min_support: float
                    ) -> tuple[np.ndarray, dict[int, tuple],
                               list[tuple[int, PharmacophoreFeature]]]:
    """One feature type -> (point labels, basin centres, kept (basin_label, feature)s).

    Features keep their basin label so a later cross-family merge can update which
    basins remain "kept" for the diagnostic plots.
    """
    n = len(coords)
    if n == 0:
        return np.empty(0, dtype=int), {}, []

    # Peaks are read off a SEPARATE field smoothed at `peak_sigma` (<= bandwidth), so
    # genuine multi-lobe sub-sites resolve as distinct peaks; positions/tolerances below
    # still come from the `bandwidth`-smoothed field. When peak_bandwidth is unset the two
    # fields coincide (old coupled behaviour).
    pk_cfg = replace(dcfg, bandwidth=dcfg.peak_sigma)
    pk_field, pk_origin = _occupancy_field(coords, weights, pk_cfg)
    peaks = _local_maxima(pk_field, pk_origin, pk_cfg)
    if len(peaks) == 0:                              # degenerate: one basin at the mean
        peaks = coords.mean(axis=0, keepdims=True)

    labels = _nearest(coords, peaks)

    # Field voxels (where the field is non-trivial) -> nearest peak, for the
    # density-weighted centroid and the field-spread tolerance.
    field, origin = _occupancy_field(coords, weights, dcfg)
    eps = field.max() * 1e-3
    vox_idx = np.argwhere(field > eps)
    vox_xyz = _voxel_centers(vox_idx, origin, dcfg.voxel)
    vox_val = field[field > eps]
    vox_basin = _nearest(vox_xyz, peaks)

    centers: dict[int, tuple] = {}
    kept: list[tuple[int, PharmacophoreFeature]] = []
    for p in range(len(peaks)):
        pts_mask = labels == p
        vox_mask = vox_basin == p
        # POSITION = density-weighted centroid of the basin voxels *within
        # membership_radius of the peak* — a peak-local window, so a diffuse tail (or a
        # neighbouring lobe spilling into the basin) cannot drag the centre off the true
        # density maximum. TOLERANCE is still taken over the whole basin (density_quantile
        # already down-weights the diffuse tail), so the sphere can still express real spread.
        local_mask = vox_mask & (
            np.linalg.norm(vox_xyz - peaks[p], axis=1) <= dcfg.membership_radius)
        if not local_mask.any():
            local_mask = vox_mask                    # rare: no voxel within the window
        if local_mask.any():
            wl = vox_val[local_mask]
            centroid = (wl[:, None] * vox_xyz[local_mask]).sum(axis=0) / wl.sum()
        else:                                        # peak with no field mass (rare)
            centroid = peaks[p]
        if vox_mask.any():
            wb = vox_val[vox_mask]
            radius = feature_radius(
                np.linalg.norm(vox_xyz[vox_mask] - centroid, axis=1), wb, tol)
        else:
            radius = tol.min
        centers[p] = tuple(float(c) for c in centroid)
        # Support is a HARD-MEMBERSHIP count: a ligand supports this peak only if it has a
        # feature point within `membership_radius` of the centre (over all family points,
        # not just the basin), so a far basin outlier no longer inflates support. Point
        # count and occupancy derive from that member set; the occupancy floor still gates
        # on the basin's field prominence (`mol_weight`).
        member = np.linalg.norm(coords - centroid, axis=1) <= dcfg.membership_radius
        mol_weight = float(weights[pts_mask].sum())
        n_points = int(member.sum())
        n_lig = len({lig for lig, m in zip(ligands, member, strict=True) if m})
        support = n_lig / n_ligands if n_ligands else 0.0
        # A peak must clear both the distinct-molecule occupancy floor and the support
        # floor (present in >= this fraction of the cell's ligands, within the radius).
        if mol_weight < dcfg.occupancy_floor or support < min_support:
            continue
        kept.append((p, PharmacophoreFeature(
            family=family, x=centers[p][0], y=centers[p][1], z=centers[p][2],
            radius=radius,
            n_points=n_points, n_ligands=n_lig,
            support=round(support, 4),
            direction=None,   # set when upstream perception supplies per-point vectors
        )))
    return labels, centers, kept


# --- public builder ----------------------------------------------------------

def build_density(table: FeatureTable, dcfg: DensityConfig, tol: ToleranceConfig,
                  name: str, metadata: dict | None = None, *,
                  min_support: float = 0.5,
                  scaffold_freq: dict[str, int] | None = None) -> BuildResult:
    """The density consensus builder: feature points in -> ``BuildResult`` out.

    ``min_support`` is the selection floor: a peak becomes a feature only if at least this
    fraction of the cell's ligands have a point within ``dcfg.membership_radius`` of its centre.
    """
    assignments: list[ClusterAssignment] = []
    pooled: list[tuple[PharmacophoreFeature, tuple[str, int]]] = []
    for family in table.families():
        pts = table.of_family(family)
        coords = np.array([p.position for p in pts], dtype=float)
        ligands = [p.ligand_id for p in pts]
        weights = _molecule_weights(ligands, scaffold_freq)
        labels, centers, kept = _family_density(
            family, coords, ligands, weights, table.n_ligands, dcfg, tol, min_support)
        pooled.extend((feat, (family, lbl)) for lbl, feat in kept)
        assignments.append(ClusterAssignment(
            family=family, coords=coords, labels=labels, ligand_ids=ligands,
            centers=centers, kept_labels=set()))

    # Cross-family merge: one feature per region of space (a donor and an acceptor that
    # land on the same atoms cannot both be true), keeping the dominant peak.
    dropped: list = []
    if dcfg.merge_overlapping:
        exempt = frozenset(frozenset(pair) for pair in dcfg.merge_exempt_pairs)
        pooled.sort(key=lambda fl: (fl[0].n_points, fl[0].support), reverse=True)
        pooled, dropped = _merge_overlapping(pooled, dcfg.merge_radius, exempt,
                                             cross_family=dcfg.merge_cross_family)
    features, kept_by_family, label_index = finalize_features(pooled)
    for assignment in assignments:
        assignment.kept_labels = kept_by_family.get(assignment.family, set())
        assignment.feature_labels = label_index.get(assignment.family, {})

    meta = dict(metadata or {})
    meta.setdefault("consensus", {"method": "density", "params": asdict(dcfg)})
    meta["n_features"] = len(features)
    ph = Pharmacophore(name=name, features=features, metadata=meta)
    return BuildResult(pharmacophore=ph, assignments=assignments,
                       merged_away=_merge_records(dropped, label_index))
