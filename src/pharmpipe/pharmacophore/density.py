"""Density-based consensus strategy for ensemble pharmacophores (Stage 4, pure core).

An alternative to the k-means feature-clustering path (``build.py``) that turns the
same per-molecule, binding-site-aligned feature points into the same consensus-feature
output — so it is a drop-in behind the ``consensus_method`` flag and downstream code
never branches on which ran.

Instead of choosing *k* and partitioning points, it estimates, per feature type, a
**Gaussian-smoothed occupancy field** over a fixed voxel grid, then reads consensus
features off the field's local maxima. Each conserved sub-site is its own peak, so
multiple features of one type fall out natively with no *k* to pick, and the whole
procedure is deterministic (fixed grid, bandwidth and threshold; no random seeding).

The unit of evidence is the **distinct molecule**, not the raw point: every point is
weighted by ``1 / (points that molecule contributes to this feature type)`` so a
molecule that happens to place many points of one type cannot dominate the field
(optionally also by inverse scaffold frequency). A peak is kept only if the summed
distinct-molecule weight in its basin clears an occupancy floor.

Precedent: dynophore cloud -> super-feature with occurrence frequency (Wolber lab);
field-maximum extraction (GBPM; Baroni et al. FLAPpharm); Gaussian feature-density
molecular representation (Tanrikulu & Schneider); occupancy/frequency thresholding
across complexes (REPHARMBLE; SARS-CoV-2 Mpro consensus pharmacophores). Excluded-volume
spheres from receptor atoms in unoccupied pocket regions follow the GBPM idea of reading
the *complement* of the ligand envelope off the receptor.
"""

from __future__ import annotations

from dataclasses import asdict

import numpy as np
from scipy.ndimage import gaussian_filter, maximum_filter
from scipy.spatial import cKDTree

from ..features.extract import FeatureTable
from .build import BuildResult, ClusterAssignment, _merge_overlapping
from .config import DensityConfig, ToleranceConfig
from .model import Pharmacophore, PharmacophoreFeature

EV_FAMILY = "ExcludedVolume"


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
                    tol: ToleranceConfig
                    ) -> tuple[np.ndarray, dict[int, tuple],
                               list[tuple[int, PharmacophoreFeature]]]:
    """One feature type -> (point labels, basin centres, kept (basin_label, feature)s).

    Features keep their basin label so a later cross-family merge can update which
    basins remain "kept" for the diagnostic plots.
    """
    n = len(coords)
    if n == 0:
        return np.empty(0, dtype=int), {}, []

    field, origin = _occupancy_field(coords, weights, dcfg)
    peaks = _local_maxima(field, origin, dcfg)
    if len(peaks) == 0:                              # degenerate: one basin at the mean
        peaks = coords.mean(axis=0, keepdims=True)

    labels = _nearest(coords, peaks)

    # Field voxels (where the field is non-trivial) -> nearest peak, for the
    # density-weighted centroid and the field-spread tolerance.
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
        # density-weighted centroid + field-spread tolerance from the basin's voxels
        if vox_mask.any():
            w = vox_val[vox_mask]
            xyz = vox_xyz[vox_mask]
            centroid = (w[:, None] * xyz).sum(axis=0) / w.sum()
            spread = float(np.sqrt((w * ((xyz - centroid) ** 2).sum(axis=1)).sum() / w.sum()))
        else:                                        # peak with no field mass (rare)
            centroid = peaks[p]
            spread = tol.min
        centers[p] = tuple(float(c) for c in centroid)
        mol_weight = float(weights[pts_mask].sum())
        if mol_weight < dcfg.occupancy_floor:
            continue
        n_lig = len({lig for lig, m in zip(ligands, pts_mask, strict=True) if m})
        kept.append((p, PharmacophoreFeature(
            family=family, x=centers[p][0], y=centers[p][1], z=centers[p][2],
            radius=float(min(max(spread, tol.min), tol.max)),
            n_points=int(pts_mask.sum()), n_ligands=n_lig,
            support=round(n_lig / n_ligands if n_ligands else 0.0, 4),
            direction=None,   # set when upstream perception supplies per-point vectors
        )))
    return labels, centers, kept


# --- excluded volume ---------------------------------------------------------

def _excluded_volume(protein_atoms: np.ndarray, ligand_atoms: np.ndarray,
                     dcfg: DensityConfig) -> list[PharmacophoreFeature]:
    """Spheres on receptor atoms that border the pocket but no ligand occupies.

    A protein atom qualifies when its nearest ligand atom is within ``ev_shell``
    (it lines the pocket) yet beyond ``ev_clearance`` (the ligand does not reach it).
    Qualifying atoms are coarsened onto an ``ev_voxel`` grid — one sphere per occupied
    cell — and the nearest ``ev_max`` to the ligand cloud are kept.
    """
    if len(protein_atoms) == 0 or len(ligand_atoms) == 0:
        return []
    tree = cKDTree(ligand_atoms)
    dist, _ = tree.query(protein_atoms, k=1)
    keep = (dist > dcfg.ev_clearance) & (dist <= dcfg.ev_shell)
    atoms = protein_atoms[keep]
    if len(atoms) == 0:
        return []
    # one sphere per coarse voxel, at the mean of its atoms
    cell = np.floor(atoms / dcfg.ev_voxel).astype(int)
    buckets: dict[tuple[int, int, int], list[np.ndarray]] = {}
    for key, atom in zip(map(tuple, cell), atoms, strict=True):
        buckets.setdefault(key, []).append(atom)
    spheres = [(np.mean(grp, axis=0), len(grp)) for grp in buckets.values()]
    spheres.sort(key=lambda s: tree.query(s[0], k=1)[0])   # nearest the ligand first
    feats: list[PharmacophoreFeature] = []
    for centre, n_atoms in spheres[: dcfg.ev_max]:
        feats.append(PharmacophoreFeature(
            family=EV_FAMILY, x=float(centre[0]), y=float(centre[1]), z=float(centre[2]),
            radius=dcfg.ev_radius, n_points=int(n_atoms), n_ligands=0, support=0.0,
            direction=None))
    return feats


# --- public builder ----------------------------------------------------------

def build_density(table: FeatureTable, dcfg: DensityConfig, tol: ToleranceConfig,
                  name: str, metadata: dict | None = None, *,
                  ligand_atoms: np.ndarray | None = None,
                  protein_atoms: np.ndarray | None = None,
                  scaffold_freq: dict[str, int] | None = None) -> BuildResult:
    """Density consensus: same contract as ``build_pharmacophore`` (k-means path).

    ``ligand_atoms`` / ``protein_atoms`` (both in the aligned frame) enable the
    excluded-volume spheres; omit them and only ligand-derived features are built.
    """
    assignments: list[ClusterAssignment] = []
    pooled: list[tuple[PharmacophoreFeature, tuple[str, int]]] = []
    for family in table.families():
        pts = table.of_family(family)
        coords = np.array([p.position for p in pts], dtype=float)
        ligands = [p.ligand_id for p in pts]
        weights = _molecule_weights(ligands, scaffold_freq)
        labels, centers, kept = _family_density(
            family, coords, ligands, weights, table.n_ligands, dcfg, tol)
        pooled.extend((feat, (family, lbl)) for lbl, feat in kept)
        assignments.append(ClusterAssignment(
            family=family, coords=coords, labels=labels, ligand_ids=ligands,
            centers=centers, kept_labels=set()))

    # Cross-family merge: one feature per region of space (a donor and an acceptor that
    # land on the same atoms cannot both be true), keeping the dominant peak. Same rule
    # as the k-means path; excluded-volume spheres (added after) are exempt.
    if dcfg.merge_overlapping:
        pooled.sort(key=lambda fl: (fl[0].n_points, fl[0].support), reverse=True)
        pooled = _merge_overlapping(pooled, dcfg.merge_radius)
    features = [feat for feat, _ in pooled]
    kept_by_family: dict[str, set[int]] = {}
    for _, (family, lbl) in pooled:
        kept_by_family.setdefault(family, set()).add(lbl)
    for assignment in assignments:
        assignment.kept_labels = kept_by_family.get(assignment.family, set())

    if dcfg.excluded_volume and protein_atoms is not None and ligand_atoms is not None:
        features.extend(_excluded_volume(protein_atoms, ligand_atoms, dcfg))

    meta = dict(metadata or {})
    meta.setdefault("consensus", {"method": "density", "params": asdict(dcfg)})
    meta["n_features"] = len(features)
    ph = Pharmacophore(name=name, features=features, metadata=meta)
    return BuildResult(pharmacophore=ph, assignments=assignments)
