"""The pharmacophore data model + its generalisable on-disk format (Stage 4).

A pharmacophore is a list of typed feature spheres (family, centre, tolerance
radius) plus support statistics and a provenance block. The JSON form is schema
versioned and method-agnostic: changing the clustering method changes the feature
positions, never the structure — so two methods' outputs are directly comparable.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field

SCHEMA = "pharmpipe.pharmacophore/v1"


@dataclass(frozen=True)
class PharmacophoreFeature:
    """One consensus feature: a tolerance sphere of a single family."""

    family: str
    x: float
    y: float
    z: float
    radius: float          # tolerance radius, Angstrom
    n_points: int          # feature points in the cluster
    n_ligands: int         # distinct ligands contributing
    support: float         # n_ligands / n_ligands_in_set

    @property
    def position(self) -> tuple[float, float, float]:
        return (self.x, self.y, self.z)


@dataclass
class Pharmacophore:
    """A named ensemble pharmacophore with provenance."""

    name: str
    features: list[PharmacophoreFeature] = field(default_factory=list)
    metadata: dict = field(default_factory=dict)

    def to_dict(self) -> dict:
        return {
            "schema": SCHEMA,
            "name": self.name,
            "metadata": self.metadata,
            "features": [asdict(f) for f in self.features],
        }

    @classmethod
    def from_dict(cls, data: dict) -> Pharmacophore:
        schema = data.get("schema")
        if schema != SCHEMA:
            raise ValueError(f"unsupported pharmacophore schema {schema!r}; expected {SCHEMA}")
        feats = [PharmacophoreFeature(**f) for f in data.get("features", [])]
        return cls(name=data["name"], features=feats, metadata=data.get("metadata", {}))
