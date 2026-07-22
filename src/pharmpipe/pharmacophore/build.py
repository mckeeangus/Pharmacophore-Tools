"""Shared assembly primitives for the density consensus strategy (Stage 4, pure core).

The pure building blocks the density builder reuses: tolerance-radius / feature-radius
maths, the cross-family overlap merge and its "merged away" bookkeeping, per-family
ordinal labelling, and the representative-ligand pick. No IO lives here, so this is the
unit-tested heart of the stage.
"""

from __future__ import annotations

from dataclasses import dataclass, field, replace
from typing import TypeVar

import numpy as np

from ..features.extract import FeatureTable
from .config import ToleranceConfig
from .model import Pharmacophore, PharmacophoreFeature

_P = TypeVar("_P")  # opaque payload carried alongside a feature through merging


@dataclass
class ClusterAssignment:
    """A family's clustering, kept for the raw-data visualisation."""

    family: str
    coords: np.ndarray          # (n, 3) all points of this family
    labels: np.ndarray          # (n,) cluster label per point
    ligand_ids: list[str]       # (n,) source ligand per point
    centers: dict[int, tuple[float, float, float]]  # label -> centre
    kept_labels: set[int]       # labels that became pharmacophore features
    # kept cluster label -> (feature label, support) for the raw-feature plots
    feature_labels: dict[int, tuple[str, float]] = field(default_factory=dict)


@dataclass
class MergeRecord:
    """One overlap-merge removal: a candidate that passed the support/size floor but was
    displaced by a stronger, already-kept feature within ``merge_radius``. Recorded so the
    report can say *why* an above-floor feature is absent and *in favour of* which one.
    ``winner_label`` is filled after ``finalize_features`` numbers the kept features."""

    dropped_family: str
    dropped_points: int
    dropped_ligands: int
    dropped_support: float
    dropped_cluster_label: int
    winner_family: str
    winner_cluster_label: int
    winner_label: str = ""


@dataclass
class BuildResult:
    pharmacophore: Pharmacophore
    assignments: list[ClusterAssignment] = field(default_factory=list)
    merged_away: list[MergeRecord] = field(default_factory=list)


def _weighted_quantile(values: np.ndarray, weights: np.ndarray, q: float) -> float:
    """Smallest ``value`` at or below which a fraction ``q`` of the weight lies."""
    if len(values) == 0:
        return 0.0
    order = np.argsort(values)
    v, w = values[order], weights[order]
    cum = np.cumsum(w)
    if cum[-1] <= 0:
        return float(v[-1])
    idx = int(np.searchsorted(cum, q * cum[-1]))
    return float(v[min(idx, len(v) - 1)])


def feature_radius(distances: np.ndarray, weights: np.ndarray | None,
                   tol: ToleranceConfig) -> float:
    """Tolerance radius from point-to-centre ``distances``, clamped to ``[min, max]``.

    ``density_quantile`` (default) returns the radius enclosing ``tol.quantile`` of the
    (optionally density-weighted) mass — the far points still assigned to the cluster no
    longer set the size. ``rmsd`` returns the (weighted) root-mean-square distance. Shared
    by both consensus paths so the sphere means the same thing in each.
    """
    if len(distances) == 0:
        return tol.min
    w = np.ones(len(distances)) if weights is None else np.asarray(weights, dtype=float)
    if tol.method == "rmsd":
        r = float(np.sqrt(np.average(distances ** 2, weights=w)))
    elif tol.method == "density_quantile":
        r = _weighted_quantile(distances, w, tol.quantile)
    else:
        raise ValueError(f"unknown tolerance method {tol.method!r}")
    return float(min(max(r, tol.min), tol.max))


def _overlaps(a: PharmacophoreFeature, b: PharmacophoreFeature,
              merge_radius: float | None) -> bool:
    """True if two features sit in the same region of space (family-agnostic).

    With an explicit ``merge_radius`` the test is a fixed centre-to-centre cutoff.
    Otherwise it is geometric: the centres are closer than the larger of the two
    tolerance radii, i.e. one centre lies inside the other's sphere — a threshold
    that scales with each cluster's own spread rather than a hand-picked number.
    """
    dist = float(np.linalg.norm(np.array(a.position) - np.array(b.position)))
    thresh = merge_radius if merge_radius is not None else max(a.radius, b.radius)
    return dist < thresh


def _merge_overlapping(candidates: list[tuple[PharmacophoreFeature, _P]],
                       merge_radius: float | None,
                       ) -> tuple[list[tuple[PharmacophoreFeature, _P]],
                                  list[tuple[PharmacophoreFeature, _P,
                                             PharmacophoreFeature, _P]]]:
    """Greedily drop overlapping features, keeping the largest in each region.

    ``candidates`` must already be sorted strongest-first (more points, then more
    support), so the first feature accepted for a region is the one we keep. The
    payload travelling with each feature is opaque, so this serves both the
    cross-family merge (payload = ``(family, label)``) and any same-family use.
    Overlap ignores family on purpose: two features of *different* families that
    occupy the same spot (e.g. a donor and an acceptor) cannot both describe one
    binding position, so the dominant one displaces the other.

    Returns ``(accepted, dropped)`` where each ``dropped`` entry is
    ``(dropped_feat, dropped_payload, winner_feat, winner_payload)`` — the first
    already-accepted feature that displaced it — for the "Merged away" report.
    """
    accepted: list[tuple[PharmacophoreFeature, _P]] = []
    dropped: list[tuple[PharmacophoreFeature, _P,
                        PharmacophoreFeature, _P]] = []
    for feat, payload in candidates:
        winner = next(((kfeat, kpay) for kfeat, kpay in accepted
                       if _overlaps(feat, kfeat, merge_radius)), None)
        if winner is None:
            accepted.append((feat, payload))
        else:
            dropped.append((feat, payload, winner[0], winner[1]))
    return accepted, dropped


def _merge_records(
    dropped: list[tuple[PharmacophoreFeature, tuple[str, int],
                        PharmacophoreFeature, tuple[str, int]]],
    label_index: dict[str, dict[int, tuple[str, float]]],
) -> list[MergeRecord]:
    """Turn raw merge drops into ``MergeRecord``s, resolving the winner's final label."""
    records: list[MergeRecord] = []
    for dfeat, (_dfam, dlabel), _wfeat, (wfam, wlabel) in dropped:
        winner_label = label_index.get(wfam, {}).get(wlabel, (wfam, 0.0))[0]
        records.append(MergeRecord(
            dropped_family=dfeat.family, dropped_points=dfeat.n_points,
            dropped_ligands=dfeat.n_ligands, dropped_support=dfeat.support,
            dropped_cluster_label=dlabel, winner_family=wfam,
            winner_cluster_label=wlabel, winner_label=winner_label))
    return records


def finalize_features(
    pooled: list[tuple[PharmacophoreFeature, tuple[str, int]]],
) -> tuple[list[PharmacophoreFeature], dict[str, set[int]],
           dict[str, dict[int, tuple[str, float]]]]:
    """Assign per-family ordinal labels and index the kept clusters for viz/report.

    ``pooled`` is the final (post-merge/cap) feature list, strongest-first. Each family's
    features are numbered ``1..n`` in that order, so ``Donor 1`` is the dominant donor.
    Returns the labelled features, ``family -> kept cluster-labels``, and
    ``family -> {cluster_label: (feature_label, support)}`` for the plots. Shared by
    both consensus paths so labelling is identical.
    """
    counts: dict[str, int] = {}
    features: list[PharmacophoreFeature] = []
    kept_by_family: dict[str, set[int]] = {}
    label_index: dict[str, dict[int, tuple[str, float]]] = {}
    for feat, (family, cluster_label) in pooled:
        counts[family] = counts.get(family, 0) + 1
        labelled = replace(feat, label=f"{family} {counts[family]}")
        features.append(labelled)
        kept_by_family.setdefault(family, set()).add(cluster_label)
        label_index.setdefault(family, {})[cluster_label] = (
            labelled.label, labelled.support)
    return features, kept_by_family, label_index


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
