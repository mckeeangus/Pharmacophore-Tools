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
    """One consensus feature: a tolerance sphere of a single family.

    The output contract is method-agnostic: a feature carries a (family, position,
    tolerance, optional direction) regardless of which consensus strategy produced
    it (k-means or density), so downstream stages never branch on the method.
    ``direction`` is a unit vector for projected families (HBD/HBA) when the upstream
    feature perception supplies per-point directions; ``None`` otherwise.
    """

    family: str
    x: float
    y: float
    z: float
    radius: float          # tolerance radius, Angstrom
    n_points: int          # feature points in the cluster / basin
    n_ligands: int         # distinct ligands contributing
    support: float         # n_ligands / n_ligands_in_set
    direction: tuple[float, float, float] | None = None
    # Concentration of the pooled per-point directions behind ``direction`` (resultant length of
    # the unit vectors, in [0,1]): 1 = tightly agreed, ~0 = scattered. ``None`` when no direction is
    # set. A direction is only reported above a threshold; the viz scales arrow length by this.
    direction_r: float | None = None
    label: str = ""        # per-family ordinal, e.g. "Donor 1" (report/viz identity)

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
        feats = [PharmacophoreFeature(**_normalise_feature(f))
                 for f in data.get("features", [])]
        return cls(name=data["name"], features=feats, metadata=data.get("metadata", {}))


def _normalise_feature(f: dict) -> dict:
    """JSON stores direction as a list; restore the tuple the dataclass expects."""
    d = dict(f)
    if d.get("direction") is not None:
        d["direction"] = tuple(d["direction"])
    return d
