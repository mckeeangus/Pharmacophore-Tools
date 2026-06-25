"""Assemble an ensemble pharmacophore from feature points (Stage 4, pure core).

Per feature family: cluster the points (any ``Clusterer``), reduce each cluster to a
centre + tolerance radius + support statistics, then keep the clusters that recur
across enough ligands. No IO and no clustering algorithm live here — the clusterer
is injected — so this is the unit-tested heart of the stage.
"""

from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np

from ..clustering.base import Clusterer
from ..features.extract import FeatureTable
from .config import SelectionConfig, ToleranceConfig
from .model import Pharmacophore, PharmacophoreFeature


@dataclass
class ClusterAssignment:
    """A family's clustering, kept for the raw-data visualisation."""

    family: str
    coords: np.ndarray          # (n, 3) all points of this family
    labels: np.ndarray          # (n,) cluster label per point
    ligand_ids: list[str]       # (n,) source ligand per point
    centers: dict[int, tuple[float, float, float]]  # label -> centre
    kept_labels: set[int]       # labels that became pharmacophore features


@dataclass
class BuildResult:
    pharmacophore: Pharmacophore
    assignments: list[ClusterAssignment] = field(default_factory=list)


def _radius(coords: np.ndarray, center: np.ndarray, tol: ToleranceConfig) -> float:
    if tol.method != "rmsd":
        raise ValueError(f"unknown tolerance method {tol.method!r}")
    rms = float(np.sqrt(np.mean(np.sum((coords - center) ** 2, axis=1))))
    return float(min(max(rms, tol.min), tol.max))


def _overlaps(a: PharmacophoreFeature, b: PharmacophoreFeature,
              merge_radius: float | None) -> bool:
    """True if two same-family features sit in the same region of space.

    With an explicit ``merge_radius`` the test is a fixed centre-to-centre cutoff.
    Otherwise it is geometric: the centres are closer than the larger of the two
    tolerance radii, i.e. one centre lies inside the other's sphere — a threshold
    that scales with each cluster's own spread rather than a hand-picked number.
    """
    dist = float(np.linalg.norm(np.array(a.position) - np.array(b.position)))
    thresh = merge_radius if merge_radius is not None else max(a.radius, b.radius)
    return dist < thresh


def _merge_overlapping(candidates: list[tuple[PharmacophoreFeature, int]],
                       merge_radius: float | None,
                       ) -> list[tuple[PharmacophoreFeature, int]]:
    """Greedily drop overlapping features, keeping the largest in each region.

    ``candidates`` must already be sorted strongest-first (more points, then more
    support), so the first feature accepted for a region is the one we keep.
    """
    accepted: list[tuple[PharmacophoreFeature, int]] = []
    for feat, label in candidates:
        if any(_overlaps(feat, kept, merge_radius) for kept, _ in accepted):
            continue
        accepted.append((feat, label))
    return accepted


def _family_features(family: str, coords: np.ndarray, labels: np.ndarray,
                     ligands: list[str], n_ligands: int, sel: SelectionConfig,
                     tol: ToleranceConfig) -> tuple[list[PharmacophoreFeature], set[int]]:
    """Reduce one family's clusters to kept features (+ the kept label set)."""
    candidates: list[tuple[PharmacophoreFeature, int]] = []
    for label in sorted(set(labels.tolist())):
        mask = labels == label
        pts = coords[mask]
        center = pts.mean(axis=0)
        n_points = int(mask.sum())
        n_lig = len({lig for lig, m in zip(ligands, mask, strict=True) if m})
        support = n_lig / n_ligands if n_ligands else 0.0
        if n_points < sel.min_cluster_size or support < sel.min_support_fraction:
            continue
        feat = PharmacophoreFeature(
            family=family, x=float(center[0]), y=float(center[1]), z=float(center[2]),
            radius=_radius(pts, center, tol), n_points=n_points,
            n_ligands=n_lig, support=round(support, 4),
        )
        candidates.append((feat, label))
    # Largest first (more points, then more support): the head of each overlap
    # region is the one kept, and this also drives the optional top-N cap.
    candidates.sort(key=lambda fl: (fl[0].n_points, fl[0].support), reverse=True)
    if sel.merge_overlapping:
        candidates = _merge_overlapping(candidates, sel.merge_radius)
    if sel.top_n_per_family is not None:
        candidates = candidates[: sel.top_n_per_family]
    return [f for f, _ in candidates], {lbl for _, lbl in candidates}


def build_pharmacophore(table: FeatureTable, clusterer: Clusterer, sel: SelectionConfig,
                        tol: ToleranceConfig, name: str,
                        metadata: dict | None = None) -> BuildResult:
    features: list[PharmacophoreFeature] = []
    assignments: list[ClusterAssignment] = []
    for family in table.families():
        pts = table.of_family(family)
        coords = np.array([p.position for p in pts], dtype=float)
        ligands = [p.ligand_id for p in pts]
        labels = np.asarray(clusterer.fit_predict(coords), dtype=int)
        fam_feats, kept = _family_features(
            family, coords, labels, ligands, table.n_ligands, sel, tol)
        features.extend(fam_feats)
        centers = {
            int(lbl): tuple(coords[labels == lbl].mean(axis=0))
            for lbl in set(labels.tolist())
        }
        assignments.append(ClusterAssignment(
            family=family, coords=coords, labels=labels, ligand_ids=ligands,
            centers=centers, kept_labels=kept))
    meta = dict(metadata or {})
    meta.setdefault("clustering", clusterer.describe())
    meta["n_features"] = len(features)
    ph = Pharmacophore(name=name, features=features, metadata=meta)
    return BuildResult(pharmacophore=ph, assignments=assignments)


def best_representative(table: FeatureTable, ph: Pharmacophore) -> str | None:
    """Pick the ligand that best fits the model, for the visualisation overlay.

    Score = fraction of kept features for which the ligand has a feature point of
    the same family inside that feature's tolerance sphere. Ties break toward the
    richer ligand (more feature points). Returns the ligand_id, or ``None`` for an
    empty set. With no kept features (no model) the first loaded ligand is returned.
    """
    if not table.ligand_ids:
        return None
    if not ph.features:
        return table.ligand_ids[0]
    by_lig: dict[str, list] = {}
    for p in table.points:
        by_lig.setdefault(p.ligand_id, []).append(p)
    best_id: str | None = None
    best_key = (-1.0, -1)
    for lig in table.ligand_ids:
        pts = by_lig.get(lig, [])
        matched = 0
        for f in ph.features:
            c = np.array(f.position)
            if any(p.family == f.family
                   and float(np.linalg.norm(np.array(p.position) - c)) <= f.radius
                   for p in pts):
                matched += 1
        key = (matched / len(ph.features), len(pts))
        if key > best_key:
            best_key, best_id = key, lig
    return best_id
