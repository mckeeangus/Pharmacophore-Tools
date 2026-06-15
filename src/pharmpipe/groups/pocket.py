"""Contact-based pocket identity for bound-ligand poses.

Pure geometry, no scientific assumptions and no network. A pose's *contact
fingerprint* is the set of protein residues it touches **in its own native
structure** — not in the Stage-2 aligned frame. This matters: Stage-2 superposes
every kept pose onto a single canonical pocket, which collapses pseudo-symmetric
sites (e.g. the GABA-A benzodiazepine site onto the orthosteric site) on top of
each other. Fingerprinting natively keeps genuinely distinct pockets distinct.

Residue keys are chain-agnostic (``RESNAME + author_seqnum``) so that the same
pocket is comparable across structures that use different chain identifiers; the
subunit copies that line one ligand instance carry distinct sequence numbering,
so distinct functional sites stay distinct while symmetric copies merge.
"""

from __future__ import annotations

import logging
from collections import Counter
from dataclasses import dataclass

import gemmi

log = logging.getLogger("pharmpipe.groups.pocket")

# A protein residue is "in contact" if any of its atoms lies within this distance
# of any ligand heavy atom.
DEFAULT_CONTACT_ANGSTROM = 4.5


# --- robust neighbour search -------------------------------------------------

def _orthogonalised(st: gemmi.Structure) -> gemmi.Structure:
    """Return a copy in a plain orthogonal P1 box.

    ``gemmi.NeighborSearch`` requires a standard crystal-frame orientation; some
    deposited cells (skewed SCALE records) violate that. We only need cartesian
    contacts, so we drop the crystal frame and wrap the model in an orthogonal
    box large enough to hold it.
    """
    model = st[0]
    xs = [a.pos for ch in model for r in ch for a in r]
    if not xs:
        return st
    pad = 5.0
    lo = gemmi.Position(min(p.x for p in xs), min(p.y for p in xs), min(p.z for p in xs))
    span = (max(p.x for p in xs) - lo.x, max(p.y for p in xs) - lo.y,
            max(p.z for p in xs) - lo.z)
    for ch in model:
        for r in ch:
            for a in r:
                a.pos = gemmi.Position(a.pos.x - lo.x + pad,
                                       a.pos.y - lo.y + pad,
                                       a.pos.z - lo.z + pad)
    st.cell = gemmi.UnitCell(span[0] + 2 * pad, span[1] + 2 * pad,
                             span[2] + 2 * pad, 90, 90, 90)
    st.spacegroup_hm = "P 1"
    return st


@dataclass
class ContactIndex:
    """A structure wrapped with a neighbour-search index for fast contacts."""
    model: gemmi.Model
    search: gemmi.NeighborSearch

    @classmethod
    def from_structure(cls, st: gemmi.Structure,
                       max_radius: float = DEFAULT_CONTACT_ANGSTROM) -> ContactIndex:
        try:
            ns = gemmi.NeighborSearch(st[0], st.cell, max_radius).populate()
        except RuntimeError:
            st = _orthogonalised(st)
            ns = gemmi.NeighborSearch(st[0], st.cell, max_radius).populate()
        return cls(model=st[0], search=ns)

    def fingerprint(self, ligand: gemmi.Residue,
                    cutoff: float = DEFAULT_CONTACT_ANGSTROM) -> frozenset[str]:
        """Protein residues (``het_flag == 'A'``) within ``cutoff`` of the ligand."""
        keys: set[str] = set()
        for atom in ligand:
            if atom.is_hydrogen():
                continue
            for mark in self.search.find_atoms(atom.pos, "\0", radius=cutoff):
                cra = mark.to_cra(self.model)
                if cra.residue.het_flag == "A":
                    keys.add(f"{cra.residue.name}{cra.residue.seqid.num}")
        return frozenset(keys)


def find_ligand(model: gemmi.Model, comp_id: str, chain_id: str,
                seqid: str) -> gemmi.Residue | None:
    """Locate a ligand instance by comp id + author seq id (chain id if it helps)."""
    matches = [r for ch in model for r in ch
               if r.name == comp_id and str(r.seqid.num) == str(seqid)]
    if not matches:
        return None
    for ch in model:
        if ch.name != chain_id:
            continue
        for r in ch:
            if r.name == comp_id and str(r.seqid.num) == str(seqid):
                return r
    return matches[0]


# --- overlap metrics & clustering -------------------------------------------

def jaccard(a: frozenset[str], b: frozenset[str]) -> float:
    if not a and not b:
        return 0.0
    return len(a & b) / len(a | b)


def overlap_coefficient(a: frozenset[str], b: frozenset[str]) -> float:
    """Intersection over the smaller set — forgiving of ligand-size differences."""
    denom = min(len(a), len(b))
    return len(a & b) / denom if denom else 0.0


class _UnionFind:
    def __init__(self, n: int):
        self.parent = list(range(n))

    def find(self, i: int) -> int:
        while self.parent[i] != i:
            self.parent[i] = self.parent[self.parent[i]]
            i = self.parent[i]
        return i

    def union(self, i: int, j: int) -> None:
        self.parent[self.find(i)] = self.find(j)


def cluster_fingerprints(fingerprints: list[frozenset[str]], *,
                         jaccard_min: float = 0.30,
                         overlap_min: float = 0.60,
                         min_shared: int = 5) -> list[int]:
    """Group poses into pockets by fingerprint overlap (connected components).

    Two poses join the same pocket when their contact sets are similar enough by
    *either* Jaccard or overlap-coefficient (the latter rescues a small fragment
    nested inside a larger inhibitor's contact set), provided they share at least
    ``min_shared`` residues. Returns a cluster id per pose, densely numbered with
    id 0 = largest cluster.
    """
    n = len(fingerprints)
    uf = _UnionFind(n)
    for i in range(n):
        for j in range(i + 1, n):
            if len(fingerprints[i] & fingerprints[j]) < min_shared:
                continue
            if (jaccard(fingerprints[i], fingerprints[j]) >= jaccard_min
                    or overlap_coefficient(fingerprints[i], fingerprints[j]) >= overlap_min):
                uf.union(i, j)

    roots = [uf.find(i) for i in range(n)]
    order = {root: rank for rank, (root, _) in enumerate(Counter(roots).most_common())}
    return [order[r] for r in roots]


def consensus_residues(fingerprints: list[frozenset[str]], indices: list[int],
                       frac: float = 0.5) -> set[str]:
    """Residues contacted by at least ``frac`` of the poses in a cluster."""
    if not indices:
        return set()
    counts: Counter = Counter()
    for i in indices:
        counts.update(fingerprints[i])
    threshold = max(1, round(frac * len(indices)))
    return {res for res, c in counts.items() if c >= threshold}
