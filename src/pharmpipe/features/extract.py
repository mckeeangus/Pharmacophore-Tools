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
    kept = [(fam, pos) for k, (fam, pos, _) in enumerate(raw) if not dropped[k]]
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
    points = [FeaturePoint(fam, pos.x, pos.y, pos.z, ligand_id) for fam, pos in kept]
    return points, resolutions


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
