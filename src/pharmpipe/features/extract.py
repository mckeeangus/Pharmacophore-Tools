"""Pharmacophore-feature extraction from 3D molecules (Stage 4, pure core).

Given RDKit molecules with 3D coordinates, pull out pharmacophore feature points
(family + position) using an RDKit feature factory. No file IO lives here — the
caller supplies already-parsed molecules (see ``load.py``) so this stays unit
testable offline.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import numpy as np
from rdkit import RDConfig
from rdkit.Chem import AllChem


@dataclass(frozen=True)
class FeaturePoint:
    """One pharmacophore feature extracted from one ligand."""

    family: str
    x: float
    y: float
    z: float
    ligand_id: str

    @property
    def position(self) -> tuple[float, float, float]:
        return (self.x, self.y, self.z)


@dataclass(frozen=True)
class FeatureResolution:
    """One co-atom hierarchy decision: ``dropped_family`` removed in favour of
    ``kept_family`` on a shared atom of ``ligand_id`` (``n_atoms`` atoms shared)."""

    ligand_id: str
    kept_family: str
    dropped_family: str
    n_atoms: int


@dataclass
class FeatureTable:
    """All feature points from a set of ligands, plus the ligand roster.

    ``ligand_ids`` is every ligand that was *loaded* (even if it contributed no
    feature of a given family) — support fractions are taken against this total.
    ``resolutions`` records every co-atom dual classification collapsed by the
    feature hierarchy (see ``_resolve_hierarchy``).
    """

    points: list[FeaturePoint]
    ligand_ids: list[str]
    resolutions: list[FeatureResolution] = None  # type: ignore[assignment]

    def __post_init__(self) -> None:
        if self.resolutions is None:
            self.resolutions = []

    @property
    def n_ligands(self) -> int:
        return len(self.ligand_ids)

    def families(self) -> list[str]:
        # Preserve first-seen order for stable, reproducible output.
        seen: dict[str, None] = {}
        for p in self.points:
            seen.setdefault(p.family, None)
        return list(seen)

    def of_family(self, family: str) -> list[FeaturePoint]:
        return [p for p in self.points if p.family == family]

    def coords(self, family: str) -> np.ndarray:
        pts = self.of_family(family)
        if not pts:
            return np.empty((0, 3), dtype=float)
        return np.array([p.position for p in pts], dtype=float)


def feature_factory(fdef: str = "base"):
    """Build an RDKit feature factory. ``base`` -> RDKit's BaseFeatures.fdef."""
    path = (Path(RDConfig.RDDataDir) / "BaseFeatures.fdef") if fdef == "base" else Path(fdef)
    return AllChem.BuildFeatureFactory(str(path))


def hierarchy_pairs(hierarchy: list[list[str]]) -> frozenset[tuple[str, str]]:
    """Expand each ordered group into ``(higher, lower)`` subsumes-pairs.

    A group ``[A, B, C]`` (highest-priority first) yields ``(A,B), (A,C), (B,C)``. Using
    a set of pairs — rather than a single rank per family — is essential because a family
    can be the *higher* member of several groups (``PosIonizable`` subsumes both ``Donor``
    and ``LumpedHydrophobe``); a per-family rank would collapse those to one group.
    """
    pairs: set[tuple[str, str]] = set()
    for group in hierarchy:
        for hi in range(len(group)):
            for lo in range(hi + 1, len(group)):
                pairs.add((group[hi], group[lo]))
    return frozenset(pairs)


def _resolve_hierarchy(
    raw: list[tuple[str, object, frozenset[int]]],
    hierarchy: list[list[str]],
    ligand_id: str,
) -> tuple[list[tuple[str, object]], list[FeatureResolution]]:
    """Collapse co-atom dual classifications by the feature hierarchy (pure).

    ``raw`` is one molecule's features as ``(family, pos, atom_ids)``. A lower-priority
    feature is dropped when it shares >=1 atom with a higher-priority feature it is
    subsumed by (per ``hierarchy_pairs``) — so a protonated amine's Donor is subsumed by
    its PosIonizable, while a hydroxyl (Donor+Acceptor, not grouped) or a lone hydrophobe
    (no overlap) is untouched. Returns the surviving ``(family, pos)`` features and the
    resolutions recorded.
    """
    pairs = hierarchy_pairs(hierarchy)
    dropped = [False] * len(raw)
    resolutions: list[FeatureResolution] = []
    for i, (fam_i, _, atoms_i) in enumerate(raw):
        for j, (fam_j, _, atoms_j) in enumerate(raw):
            if i == j:
                continue
            # fam_j subsumes fam_i and they touch the same atom -> drop fam_i
            if (fam_j, fam_i) in pairs and (shared := atoms_i & atoms_j):
                dropped[i] = True
                resolutions.append(
                    FeatureResolution(ligand_id, fam_j, fam_i, len(shared)))
                break
    kept = [(fam, pos, atoms) for k, (fam, pos, atoms) in enumerate(raw) if not dropped[k]]
    return kept, resolutions


def featurize(mol, factory, families: list[str], ligand_id: str,
              hierarchy: list[list[str]] | None = None,
              ) -> tuple[list[FeaturePoint], list[FeatureResolution]]:
    """Extract the requested feature families from one molecule (pure).

    Returns the surviving feature points and any co-atom hierarchy resolutions. A
    ``None``/empty ``hierarchy`` disables the collapse (every perceived feature is kept).
    """
    wanted = set(families)
    raw: list[tuple[str, object, frozenset[int]]] = []
    for feat in factory.GetFeaturesForMol(mol):
        fam = feat.GetFamily()
        if fam not in wanted:
            continue
        raw.append((fam, feat.GetPos(), frozenset(feat.GetAtomIds())))
    kept, resolutions = _resolve_hierarchy(raw, hierarchy or [], ligand_id)
    points = [FeaturePoint(fam, pos.x, pos.y, pos.z, ligand_id) for fam, pos, _ in kept]
    return points, resolutions


# Families whose H-bond / ring geometry gives a meaningful orientation for directional matching.
DIRECTIONAL_FAMILIES = frozenset({"Donor", "Acceptor", "Aromatic"})


def _feature_direction(mol, conf, family: str, atom_ids: frozenset[int]) -> np.ndarray | None:
    """Unit orientation vector for a directional feature on one conformer, or ``None``.

    * Donor    — mean(H − D) over the donor heavy atom's attached hydrogens (points the H-bond
                 the way it is donated); ``None`` if the pose is heavy-atom-only (no explicit H).
    * Acceptor — from the heavy neighbours toward the acceptor atom (acceptor − mean(neighbours)),
                 i.e. the lone-pair / donor-approach direction; this is what distinguishes a
                 correctly-oriented ring nitrogen from a ring-flipped one.
    * Aromatic — the ring-plane normal (via SVD of the ring atom coordinates); sign-ambiguous, so it
                 is matched unsigned downstream.
    Returns a unit vector or ``None`` when the geometry is unavailable/degenerate.
    """
    def pos(idx: int) -> np.ndarray:
        p = conf.GetAtomPosition(idx)
        return np.array([p.x, p.y, p.z], dtype=float)

    def unit(v: np.ndarray) -> np.ndarray | None:
        n = float(np.linalg.norm(v))
        return v / n if n > 1e-6 else None

    if family == "Aromatic":
        ring = np.array([pos(i) for i in atom_ids])
        if len(ring) < 3:
            return None
        _, _, vt = np.linalg.svd(ring - ring.mean(axis=0))
        return unit(vt[2])                              # normal = smallest-variance axis
    heavy = [i for i in atom_ids if mol.GetAtomWithIdx(i).GetAtomicNum() > 1]
    if not heavy:
        return None
    atom = mol.GetAtomWithIdx(heavy[0])
    apos = pos(heavy[0])
    if family == "Donor":
        hs = [pos(nb.GetIdx()) for nb in atom.GetNeighbors() if nb.GetAtomicNum() == 1]
        return unit(np.mean(hs, axis=0) - apos) if hs else None
    if family == "Acceptor":
        nbrs = [pos(nb.GetIdx()) for nb in atom.GetNeighbors() if nb.GetAtomicNum() > 1]
        return unit(apos - np.mean(nbrs, axis=0)) if nbrs else None
    return None


def conformer_features(mol, factory, families: list[str],
                       hierarchy: list[list[str]] | None = None,
                       conf_id: int = -1,
                       ) -> list[tuple[str, np.ndarray, np.ndarray | None]]:
    """Resolved ``(family, xyz, direction)`` feature points for one conformer of ``mol`` (pure).

    Like ``featurize`` but returns typed points *with an orientation vector* for a specific
    conformer (``conf_id``, default the first) — used by the feature-alignment build. ``direction``
    is a unit vector for directional families (Donor/Acceptor/Aromatic, see ``_feature_direction``)
    and ``None`` otherwise (or when the geometry is unavailable, e.g. a heavy-atom-only pose has no
    donor H). The co-atom hierarchy is applied exactly as elsewhere.
    """
    wanted = set(families)
    raw = [(f.GetFamily(), f.GetPos(), frozenset(f.GetAtomIds()))
           for f in factory.GetFeaturesForMol(mol, confId=conf_id) if f.GetFamily() in wanted]
    kept, _ = _resolve_hierarchy(raw, hierarchy or [], "")
    conf = mol.GetConformer(conf_id)
    out = []
    for fam, pos, atoms in kept:
        direction = (_feature_direction(mol, conf, fam, atoms)
                     if fam in DIRECTIONAL_FAMILIES else None)
        out.append((fam, np.array([pos.x, pos.y, pos.z], dtype=float), direction))
    return out


def build_table(molecules: list[tuple[str, object]], factory,
                families: list[str],
                hierarchy: list[list[str]] | None = None) -> FeatureTable:
    """Featurize an ordered list of (ligand_id, mol) into a FeatureTable."""
    points: list[FeaturePoint] = []
    ligand_ids: list[str] = []
    resolutions: list[FeatureResolution] = []
    for ligand_id, mol in molecules:
        ligand_ids.append(ligand_id)
        pts, res = featurize(mol, factory, families, ligand_id, hierarchy)
        points.extend(pts)
        resolutions.extend(res)
    return FeatureTable(points=points, ligand_ids=ligand_ids, resolutions=resolutions)
