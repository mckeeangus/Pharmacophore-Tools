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


@dataclass
class FeatureTable:
    """All feature points from a set of ligands, plus the ligand roster.

    ``ligand_ids`` is every ligand that was *loaded* (even if it contributed no
    feature of a given family) — support fractions are taken against this total.
    """

    points: list[FeaturePoint]
    ligand_ids: list[str]

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


def featurize(mol, factory, families: list[str], ligand_id: str) -> list[FeaturePoint]:
    """Extract the requested feature families from one molecule (pure)."""
    wanted = set(families)
    out: list[FeaturePoint] = []
    for feat in factory.GetFeaturesForMol(mol):
        fam = feat.GetFamily()
        if fam not in wanted:
            continue
        pos = feat.GetPos()
        out.append(FeaturePoint(fam, pos.x, pos.y, pos.z, ligand_id))
    return out


def build_table(molecules: list[tuple[str, object]], factory,
                families: list[str]) -> FeatureTable:
    """Featurize an ordered list of (ligand_id, mol) into a FeatureTable."""
    points: list[FeaturePoint] = []
    ligand_ids: list[str] = []
    for ligand_id, mol in molecules:
        ligand_ids.append(ligand_id)
        points.extend(featurize(mol, factory, families, ligand_id))
    return FeatureTable(points=points, ligand_ids=ligand_ids)
