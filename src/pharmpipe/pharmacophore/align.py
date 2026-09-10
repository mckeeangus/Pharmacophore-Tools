"""Feature-clique alignment for the docked-seed minimum-docking build (Stage 4, pure core).

With no protein frame, ligands are superposed by their *features*. Two molecules' feature
point clouds are matched with a correspondence-graph clique search (à la DISCO/Phase): a node
pairs two same-family features, an edge joins two nodes whose intra-molecular distances agree,
and a maximal clique (Bron-Kerbosch) is a mutually-consistent set of feature matches. Each
clique yields a rigid transform in closed form (Kabsch); the best-scoring clique wins.

The multiple alignment uses a **seed/reference scheme**: start from a consensus model built
from a few docked poses (the bioactive frame), then align each further ligand's best conformer
onto the running model and fold its matched features back in (running mean), so the model
sharpens as it grows. Pure numpy — no RDKit, no IO — so it is unit-testable in isolation.
"""

from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np

# A feature point is (family, xyz, direction) — direction is a unit orientation vector for
# directional families (Donor/Acceptor/Aromatic) or None. A point cloud is a list of them. The
# aligner is generic over families: it matches on family + intra-molecular distances, and (when
# directions are used) fits orientation via projected points (see `align_features`).
FeatureCloud = list[tuple[str, np.ndarray, np.ndarray | None]]

# Directional families whose orientation is fit in the superposition via a projected point. The
# aromatic ring-normal is perceived but excluded here: it is sign-ambiguous, so it is not used as
# a Kabsch target (the H-bond donor/acceptor orientation is what resolves the ring-flip).
PROJECTED_FAMILIES = frozenset({"Donor", "Acceptor"})


@dataclass(frozen=True)
class AlignResult:
    """A rigid transform mapping a probe cloud onto the reference (x' = R·x + t)."""

    rotation: np.ndarray     # (3,3)
    translation: np.ndarray  # (3,)
    n_matched: int
    rmsd: float

    def apply(self, xyz: np.ndarray) -> np.ndarray:
        return xyz @ self.rotation.T + self.translation


@dataclass(frozen=True)
class AlignRecord:
    """Per-ligand provenance for one row of ``alignment_manifest.csv``."""

    ligand_id: str
    source: str          # "seed" | "aligned"
    n_conformers: int    # conformers considered (0 for seed poses)
    conformer: int       # index of the chosen conformer (-1 for seed / unaligned)
    n_matched: int       # feature correspondences in the winning clique (0 if unaligned)
    rmsd: float          # clique superposition RMSD (nan if unaligned)
    aligned: bool


@dataclass
class SeedAlignResult:
    points: list[tuple[str, np.ndarray, str]] = field(default_factory=list)  # (family, xyz, lig)
    transforms: dict[str, tuple[np.ndarray, np.ndarray, int]] = field(default_factory=dict)
    manifest: list[AlignRecord] = field(default_factory=list)
    # EM convergence trace: (iteration, max consensus feature-centre shift in A, n aligned).
    convergence: list[tuple[int, float, int]] = field(default_factory=list)


def _kabsch(P: np.ndarray, Q: np.ndarray) -> tuple[np.ndarray, np.ndarray, float]:
    """Rigid transform (proper rotation R, translation t) best mapping P onto Q, and RMSD."""
    Pc, Qc = P - P.mean(0), Q - Q.mean(0)
    U, _, Vt = np.linalg.svd(Pc.T @ Qc)
    d = np.sign(np.linalg.det(Vt.T @ U.T))
    R = Vt.T @ np.diag([1.0, 1.0, d]) @ U.T
    t = Q.mean(0) - R @ P.mean(0)
    rmsd = float(np.sqrt((((P @ R.T + t) - Q) ** 2).sum(1).mean()))
    return R, t, rmsd


def _maximal_cliques(adj: list[set[int]]):
    """All maximal cliques of an undirected graph (Bron-Kerbosch with pivoting)."""
    out: list[set[int]] = []

    def expand(R: set[int], P: set[int], X: set[int]) -> None:
        if not P and not X:
            out.append(R)
            return
        pivot = max(P | X, key=lambda u: len(adj[u] & P))
        for v in list(P - adj[pivot]):
            expand(R | {v}, P & adj[v], X & adj[v])
            P = P - {v}
            X = X | {v}

    expand(set(), set(range(len(adj))), set())
    return out


def _greedy_cliques(adj: list[set[int]], starts: int = 8):
    """A few large cliques, grown greedily — an O(n^2) fallback when exact enumeration would
    blow up (feature-rich molecules give a big correspondence graph, and Bron-Kerbosch is
    exponential). From each of the ``starts`` highest-degree seed nodes, repeatedly add the
    candidate adjacent to all current members with the most onward connections. Not guaranteed
    maximum, but bounded and deterministic; the best of the returned cliques is used."""
    order = sorted(range(len(adj)), key=lambda u: len(adj[u]), reverse=True)
    out: list[set[int]] = []
    for seed in order[:starts]:
        clique = {seed}
        cand = set(adj[seed])
        while cand:
            v = max(cand, key=lambda u: len(adj[u] & cand))
            clique.add(v)
            cand &= adj[v]
        out.append(clique)
    return out


def _cliques(adj: list[set[int]], max_nodes: int):
    """Exact maximal cliques when the graph is small enough, else a greedy bounded set."""
    return _maximal_cliques(adj) if len(adj) <= max_nodes else _greedy_cliques(adj)


def _clique_points(probe: FeatureCloud, ref: FeatureCloud, nodes, idx,
                   use_directions: bool, projected_length: float):
    """Correspondence point sets (P from probe, Q from ref) for one clique.

    Each matched pair contributes its centre; when ``use_directions`` and both members of a
    ``PROJECTED_FAMILIES`` pair carry a direction, it *also* contributes a **projected point**
    (centre + ``projected_length`` · direction). Fitting those jointly bakes H-bond orientation
    into the superposition, so a ring-flipped acceptor (right position, wrong direction) no longer
    superposes and is penalised by RMSD."""
    P, Q = [], []
    for k in idx:
        i, j = nodes[k]
        P.append(probe[i][1])
        Q.append(ref[j][1])
        if use_directions and probe[i][0] in PROJECTED_FAMILIES:
            dp, dq = probe[i][2], ref[j][2]
            if dp is not None and dq is not None:
                P.append(probe[i][1] + projected_length * dp)
                Q.append(ref[j][1] + projected_length * dq)
    return np.array(P), np.array(Q)


def align_features(probe: FeatureCloud, ref: FeatureCloud,
                   dist_tol: float, min_clique: int, max_nodes: int = 40,
                   use_directions: bool = False,
                   projected_length: float = 1.5) -> AlignResult | None:
    """Best rigid transform mapping ``probe`` feature points onto ``ref`` (or ``None``).

    A correspondence node is a same-family pair ``(i in probe, j in ref)``; two nodes are
    adjacent when their intra-molecular distances agree within ``dist_tol`` (and they share
    no probe/ref index). The largest clique with the smallest RMSD, of size >= ``min_clique``,
    gives the returned transform. When ``use_directions``, the superposition also fits H-bond
    donor/acceptor **projected points** (see ``_clique_points``), so orientation — not just
    position — is matched. ``None`` when no clique exists. Exact enumeration is used while the
    graph has <= ``max_nodes`` nodes; above that a bounded greedy search keeps runtime polynomial.
    """
    nodes = [(i, j) for i, pf in enumerate(probe) for j, rf in enumerate(ref) if pf[0] == rf[0]]
    if len(nodes) < min_clique:
        return None
    adj: list[set[int]] = [set() for _ in nodes]
    for a in range(len(nodes)):
        ia, ja = nodes[a]
        for b in range(a + 1, len(nodes)):
            ib, jb = nodes[b]
            if ia == ib or ja == jb:
                continue
            dp = float(np.linalg.norm(probe[ia][1] - probe[ib][1]))
            dr = float(np.linalg.norm(ref[ja][1] - ref[jb][1]))
            if abs(dp - dr) <= dist_tol:
                adj[a].add(b)
                adj[b].add(a)
    best: AlignResult | None = None
    for clique in _cliques(adj, max_nodes):
        if len(clique) < min_clique:
            continue
        idx = sorted(clique)
        P, Q = _clique_points(probe, ref, nodes, idx, use_directions, projected_length)
        R, t, rmsd = _kabsch(P, Q)
        if best is None or (len(clique), -rmsd) > (best.n_matched, -best.rmsd):
            best = AlignResult(R, t, len(clique), rmsd)
    return best


def _mean_direction(dirs: list) -> np.ndarray | None:
    """Unit mean of the non-None direction vectors (or ``None`` if there are none/degenerate)."""
    vs = [d for d in dirs if d is not None]
    if not vs:
        return None
    m = np.mean(vs, axis=0)
    n = float(np.linalg.norm(m))
    return m / n if n > 1e-6 else None


def consolidate(points: FeatureCloud, radius: float) -> FeatureCloud:
    """Greedily merge same-family points within ``radius`` into one reference slot each.

    Turns the seed poses' overlapping feature clouds into a compact one-point-per-site model
    (``(family, centroid, mean_direction)``) for the clique search to align against.
    """
    ref: FeatureCloud = []
    for fam in sorted({f for f, _, _ in points}):
        pts = [(p, d) for f, p, d in points if f == fam]
        used = [False] * len(pts)
        for i, (pi, _) in enumerate(pts):
            if used[i]:
                continue
            group = [i]
            used[i] = True
            for j in range(i + 1, len(pts)):
                if not used[j] and np.linalg.norm(pts[j][0] - pi) <= radius:
                    used[j] = True
                    group.append(j)
            centroid = np.mean([pts[g][0] for g in group], axis=0)
            ref.append((fam, centroid, _mean_direction([pts[g][1] for g in group])))
    return ref


def _best_alignment(conformers: list[FeatureCloud], ref: FeatureCloud, *, dist_tol: float,
                    min_clique: int, max_clique_nodes: int, max_align_rmsd: float | None,
                    use_directions: bool, projected_length: float,
                    ) -> tuple[AlignResult, int, FeatureCloud] | None:
    """Best (most-matched, lowest-RMSD) conformer alignment of one compound onto ``ref``.

    Trying every conformer and keeping the best is the **conformer re-selection**: as ``ref``
    improves across EM iterations, a compound can pick a different, better-fitting conformer than
    it did against the initial seed. ``None`` if no conformer clears ``min_clique`` / the RMSD gate.
    """
    best: tuple[AlignResult, int, FeatureCloud] | None = None
    for ci, cloud in enumerate(conformers):
        res = align_features(cloud, ref, dist_tol, min_clique, max_clique_nodes,
                             use_directions, projected_length)
        if res is None or (max_align_rmsd is not None and res.rmsd > max_align_rmsd):
            continue
        if best is None or (res.n_matched, -res.rmsd) > (best[0].n_matched, -best[0].rmsd):
            best = (res, ci, cloud)
    return best


def _assign(fam: str, xyz: np.ndarray, ref: FeatureCloud, radius: float) -> int | None:
    """Index of the nearest same-family ref slot within ``radius`` of ``xyz`` (or ``None``)."""
    same = [(k, float(np.linalg.norm(xyz - rf[1]))) for k, rf in enumerate(ref) if rf[0] == fam]
    if not same:
        return None
    k, d = min(same, key=lambda t: t[1])
    return k if d <= radius else None


def _rotate(direction, rot: np.ndarray):
    """Apply a rotation to a direction vector (no translation); ``None`` passes through."""
    return None if direction is None else direction @ rot.T


def seed_align(seed_points: list[tuple[str, np.ndarray, np.ndarray | None, str]],
               compounds: list[tuple[str, list[FeatureCloud]]],
               *, dist_tol: float, min_clique: int, membership_radius: float,
               max_align_rmsd: float | None = None, max_clique_nodes: int = 40,
               em_iterations: int = 0, em_tol: float = 0.1,
               use_directions: bool = False, projected_length: float = 1.5,
               bootstrap_seed: bool = False) -> SeedAlignResult:
    """Align each ranked compound onto a consensus initialised from ``seed_points``.

    ``seed_points`` are the initial frame's ``(family, xyz, direction, ligand_id)`` — docked poses,
    a crystal ligand, or (seedless) the top compound's lowest-energy conformer. ``compounds`` is
    ``(ligand_id, [conformer_cloud, ...])`` for every ranked ligand to align. Returns the pooled
    aligned feature cloud (with rotated directions), the per-ligand transforms, a manifest, and the
    EM convergence trace. The consensus is built **in the seed's coordinate frame**, so a seed given
    in a protein's coordinates yields a pharmacophore aligned to that binding site.

    A **growing pass** aligns compounds in rank order, updating the reference slots by running mean
    (as the consensus accretes). Then an **EM refinement** (up to ``em_iterations``) re-aligns
    *every* compound to the current full consensus — re-selecting each one's best conformer — and
    recomputes each slot's centre and mean direction, until the largest slot shift falls below
    ``em_tol``. When ``use_directions``, H-bond orientation is fit via projected points (see
    ``align_features``). A compound whose best clique RMSD exceeds ``max_align_rmsd`` is dropped.

    ``bootstrap_seed``: when True the seed is a **scaffold, not a member** — it anchors the
    reference through the whole growing pass (so every compound aligns to the seed's bioactive
    frame), but it is excluded from the pooled consensus and dropped before the EM refinement, so
    the final model reflects the ranked compounds alone (re-settled by EM). The coordinate frame is
    still the seed's, so a seed in a protein's coordinates yields a binding-site-aligned model. This
    is what an external ``--seed`` (a holo co-crystal ligand) uses — it performed best in testing.
    ``False`` (default) keeps the seed in the reference and consensus (the seedless top compound and
    docked seeds are themselves ranked members).
    """
    ba = dict(dist_tol=dist_tol, min_clique=min_clique, max_clique_nodes=max_clique_nodes,
              max_align_rmsd=max_align_rmsd, use_directions=use_directions,
              projected_length=projected_length)
    ref = consolidate([(f, p, d) for f, p, d, _ in seed_points], membership_radius)
    # fixed seed anchors per slot: (position, direction)
    seed_by_slot: list[list[tuple]] = [[] for _ in ref]
    for f, p, d, _ in seed_points:
        k = _assign(f, p, ref, membership_radius)
        if k is not None:
            seed_by_slot[k].append((p, d))

    # --- growing pass: rank order, running-mean update -----------------------------
    result = SeedAlignResult()
    # A bootstrap seed anchors the reference (below) but is kept out of the pooled consensus.
    result.points = [] if bootstrap_seed else list(seed_points)
    accum: list[list[tuple]] = [list(s) for s in seed_by_slot]
    for lig in sorted({lid for _, _, _, lid in seed_points}):
        result.manifest.append(AlignRecord(lig, "seed", 0, -1, 0, float("nan"), True))
    for lig, conformers in compounds:
        best = _best_alignment(conformers, ref, **ba)
        if best is None:
            result.manifest.append(
                AlignRecord(lig, "aligned", len(conformers), -1, 0, float("nan"), False))
            continue
        res, ci, cloud = best
        result.transforms[lig] = (res.rotation, res.translation, ci)
        for fam, xyz, direction in cloud:
            axyz, adir = res.apply(xyz), _rotate(direction, res.rotation)
            result.points.append((fam, axyz, adir, lig))
            k = _assign(fam, axyz, ref, membership_radius)
            if k is not None:
                accum[k].append((axyz, adir))
                ref[k] = (ref[k][0], np.mean([p for p, _ in accum[k]], axis=0),
                          _mean_direction([d for _, d in accum[k]]))
        result.manifest.append(
            AlignRecord(lig, "aligned", len(conformers), ci, res.n_matched, res.rmsd, True))

    # --- EM refinement: re-align all to the consensus, recompute slots -------------
    for it in range(1, em_iterations + 1):
        prev = [c.copy() for _, c, _ in ref]
        # A bootstrap seed is gone by EM: re-align every compound to the seed-free consensus.
        pooled: list[tuple] = [] if bootstrap_seed else list(seed_points)
        transforms: dict[str, tuple[np.ndarray, np.ndarray, int]] = {}
        slot_pts: list[list[tuple]] = [[] if bootstrap_seed else list(s) for s in seed_by_slot]
        manifest: list[AlignRecord] = [m for m in result.manifest if m.source == "seed"]
        for lig, conformers in compounds:
            best = _best_alignment(conformers, ref, **ba)
            if best is None:
                manifest.append(
                    AlignRecord(lig, "aligned", len(conformers), -1, 0, float("nan"), False))
                continue
            res, ci, cloud = best
            transforms[lig] = (res.rotation, res.translation, ci)
            for fam, xyz, direction in cloud:
                axyz, adir = res.apply(xyz), _rotate(direction, res.rotation)
                pooled.append((fam, axyz, adir, lig))
                k = _assign(fam, axyz, ref, membership_radius)
                if k is not None:
                    slot_pts[k].append((axyz, adir))
            manifest.append(
                AlignRecord(lig, "aligned", len(conformers), ci, res.n_matched, res.rmsd, True))
        for k in range(len(ref)):
            if slot_pts[k]:
                ref[k] = (ref[k][0], np.mean([p for p, _ in slot_pts[k]], axis=0),
                          _mean_direction([d for _, d in slot_pts[k]]))
        result.points, result.transforms, result.manifest = pooled, transforms, manifest
        shift = max((float(np.linalg.norm(ref[k][1] - prev[k])) for k in range(len(ref))),
                    default=0.0)
        n_aligned = sum(1 for m in manifest if m.source == "aligned" and m.aligned)
        result.convergence.append((it, shift, n_aligned))
        if shift < em_tol:
            break
    return result


def write_alignment_manifest(manifest: list[AlignRecord], path):
    """Write per-ligand alignment provenance (source, conformer, matches, rmsd) to CSV."""
    import csv
    with open(path, "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["ligand_id", "source", "n_conformers", "conformer", "n_matched",
                    "rmsd", "aligned"])
        for r in manifest:
            rmsd = "" if np.isnan(r.rmsd) else f"{r.rmsd:.3f}"
            w.writerow([r.ligand_id, r.source, r.n_conformers, r.conformer, r.n_matched,
                        rmsd, r.aligned])
    return path
