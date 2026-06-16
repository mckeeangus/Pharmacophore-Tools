"""Stage 3 — faithful, pocket-aware re-alignment for multi-pocket targets.

Stage 2 superposes every kept pose onto ONE local pocket frame. That is tight for
comparing poses *within* a pocket, but it collapses pseudo-symmetric sites: a
GABA-A benzodiazepine-site ligand ends up stacked on top of the orthosteric
ligand. For a faithful cross-pocket overlay we instead rigid-body superpose each
pose's *whole native assembly* onto the target reference structure and move the
native ligand by that transform. Every ligand then sits at its true subunit
interface on the shared reference, so distinct pockets are spatially distinct.

The hard part is pseudo-symmetry: a homo-pentamer-like receptor (GABA-A) has near-
identical subunits, so a naive single-chain fit can map a native subunit onto the
*wrong* reference copy and rotate the whole assembly by one position. We avoid that
by (1) anchoring the rough fit on the most *discriminating* chain — the one whose
best sequence match is far ahead of its second-best, i.e. a unique subunit such as
GABA-A's gamma — then (2) assigning the remaining chains by spatial proximity in
that rough frame and (3) refining on all matched Calpha at once. Used only where
``realign_global: true`` in config/pockets.yaml.
"""

from __future__ import annotations

import logging

import gemmi

log = logging.getLogger("pharmpipe.groups.realign")

_CHAIN_CENTROID_TOL = 15.0     # max chain-centroid gap to accept a subunit pairing


def _apply(t: gemmi.Transform, p: gemmi.Position) -> gemmi.Position:
    q = t.apply(p)
    return gemmi.Position(q.x, q.y, q.z)


def _centroid(positions: list[gemmi.Position]) -> gemmi.Position:
    n = len(positions)
    return gemmi.Position(sum(p.x for p in positions) / n,
                          sum(p.y for p in positions) / n,
                          sum(p.z for p in positions) / n)


def _polymers(model: gemmi.Model, min_len: int = 20):
    return [c.get_polymer() for c in model if len(c.get_polymer()) >= min_len]


def _ca_by_seqnum(poly: gemmi.ResidueSpan) -> dict[int, gemmi.Position]:
    out: dict[int, gemmi.Position] = {}
    for res in poly:
        ca = res.get_ca()
        if ca is not None:
            out[res.seqid.num] = ca.pos
    return out


def global_transform(ref_model: gemmi.Model, mov_model: gemmi.Model,
                     min_count: int = 30, min_pairs: int = 60) -> gemmi.Transform | None:
    """Symmetry-robust rigid-body transform putting ``mov_model`` into the
    reference frame (see module docstring). Returns ``None`` if nothing aligns."""
    refs = _polymers(ref_model)
    movs = _polymers(mov_model)
    if not refs or not movs:
        return None

    # 1) all reference-chain x native-chain sequence-aware superposition scores.
    score: dict[tuple[int, int], gemmi.SupResult] = {}
    for ri, rp in enumerate(refs):
        for mi, mp in enumerate(movs):
            try:
                sup = gemmi.calculate_superposition(
                    rp, mp, gemmi.PolymerType.PeptideL, gemmi.SupSelect.CaP)
            except RuntimeError:
                continue
            if sup.count >= min_count:
                score[(ri, mi)] = sup
    if not score:
        return None

    # 2) anchor on the most discriminating reference chain (unique subunit).
    anchor = _discriminating_anchor(refs, movs, score)
    if anchor is None:
        return None
    t0 = score[anchor].transform

    # 3) assign remaining native chains to reference chains by proximity in t0 frame.
    ref_ca = [_ca_by_seqnum(rp) for rp in refs]
    mov_ca = [_ca_by_seqnum(mp) for mp in movs]
    pairs = _assign_chains(ref_ca, mov_ca, score, anchor, t0)

    # 4) refine on all matched Calpha (paired by seq number within each chain pair).
    fixed: list[gemmi.Position] = []
    moving: list[gemmi.Position] = []
    for ri, mi in pairs:
        for num in ref_ca[ri].keys() & mov_ca[mi].keys():
            fixed.append(ref_ca[ri][num])
            moving.append(mov_ca[mi][num])
    if len(fixed) < min_pairs:
        return t0
    return gemmi.superpose_positions(fixed, moving).transform


def _discriminating_anchor(refs, movs, score) -> tuple[int, int] | None:
    """Reference chain whose best native match most exceeds its second-best."""
    best: tuple[int, int] | None = None
    best_disc = -1.0
    for ri in range(len(refs)):
        counts = sorted((score[(ri, mi)].count, mi)
                        for mi in range(len(movs)) if (ri, mi) in score)
        if not counts:
            continue
        top = counts[-1]
        second = counts[-2][0] if len(counts) > 1 else 0
        disc = top[0] - second
        if disc > best_disc:
            best_disc, best = disc, (ri, top[1])
    return best


def _assign_chains(ref_ca, mov_ca, score, anchor, t0) -> list[tuple[int, int]]:
    ref_cent = [_centroid(list(d.values())) for d in ref_ca]
    mov_cent = [_centroid([_apply(t0, p) for p in d.values()]) for d in mov_ca]
    used_ref: set[int] = set()
    pairs: list[tuple[int, int]] = []
    order = sorted(range(len(mov_ca)), key=lambda mi: 0 if mi == anchor[1] else 1)
    for mi in order:
        cands = [(ref_cent[ri].dist(mov_cent[mi]), ri)
                 for ri in range(len(ref_ca))
                 if ri not in used_ref and (ri, mi) in score]
        if not cands:
            continue
        dist, ri = min(cands)
        if dist <= _CHAIN_CENTROID_TOL:
            used_ref.add(ri)
            pairs.append((ri, mi))
    return pairs


def apply_transform(res: gemmi.Residue, t: gemmi.Transform) -> None:
    """Move a residue's atoms into the reference frame (in place)."""
    for atom in res:
        atom.pos = _apply(t, atom.pos)
