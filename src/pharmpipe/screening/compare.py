"""Compare two pharmacophore models by feature composition + internal geometry (pure).

The screening models and the known-actives models live in different coordinate frames (each
docked set in its PDB crystal frame; the catalogue models in the Stage-2 aligned frame), so
positions are not directly comparable — only **which families are present** and the **internal
pairwise distances** between features are. This module reduces a model to one dominant feature
per family and compares two such reductions (or a model against a literature family set).
"""

from __future__ import annotations

from dataclasses import dataclass, field
from itertools import combinations

import numpy as np

EXCLUDED = "ExcludedVolume"


def _pos(feat: dict) -> np.ndarray:
    p = feat.get("position")
    if p is None:
        p = [feat.get("x"), feat.get("y"), feat.get("z")]
    return np.asarray(p, dtype=float)


@dataclass
class ModelSummary:
    """One model reduced to its dominant (highest-support) feature per family."""

    # family -> (dominant-feature position, support); family -> number of features of that type
    dominant: dict[str, tuple[np.ndarray, float]] = field(default_factory=dict)
    counts: dict[str, int] = field(default_factory=dict)

    @property
    def families(self) -> set[str]:
        return set(self.dominant)

    def distances(self) -> dict[frozenset, float]:
        """Internal pairwise distance between the dominant feature of each family pair."""
        out: dict[frozenset, float] = {}
        for a, b in combinations(sorted(self.dominant), 2):
            out[frozenset((a, b))] = float(np.linalg.norm(
                self.dominant[a][0] - self.dominant[b][0]))
        return out


def summarise(features: list[dict]) -> ModelSummary:
    """Reduce a list of pharmacophore_model.json features to a ModelSummary (EV dropped)."""
    s = ModelSummary()
    for f in features:
        fam = f.get("family")
        if fam == EXCLUDED or fam is None:
            continue
        s.counts[fam] = s.counts.get(fam, 0) + 1
        support = float(f.get("support") or 0.0)
        if fam not in s.dominant or support > s.dominant[fam][1]:
            s.dominant[fam] = (_pos(f), support)
    return s


@dataclass
class Comparison:
    shared: list[str]
    only_a: list[str]      # in the screening model, not the reference
    only_b: list[str]      # in the reference, not the screening model
    geom: dict[str, float]  # "cation-aromatic" -> |d_a - d_b| over shared family pairs
    family_recall: float   # |shared| / |reference families|
    mean_geom_delta: float | None
    verdict: str           # MATCH | PARTIAL | MISMATCH


def _label(pair: frozenset) -> str:
    short = {"PosIonizable": "cation", "NegIonizable": "anion", "Aromatic": "aromatic",
             "Acceptor": "acceptor", "Donor": "donor", "LumpedHydrophobe": "hydrophobe"}
    a, b = sorted(pair)
    return f"{short.get(a, a)}-{short.get(b, b)}"


def compare_models(a: ModelSummary, b: ModelSummary, geom_tol: float = 1.5) -> Comparison:
    """Compare screening model ``a`` to reference model ``b`` (known-actives).

    ``verdict``: MATCH when every reference family is recovered and the shared internal
    distances agree within ``geom_tol``; PARTIAL when most families are recovered (>=0.5) or
    geometry is off; MISMATCH otherwise.
    """
    shared = sorted(a.families & b.families)
    da, db = a.distances(), b.distances()
    geom = {_label(k): abs(da[k] - db[k]) for k in (set(da) & set(db))}
    recall = len(shared) / len(b.families) if b.families else 0.0
    mean_delta = float(np.mean(list(geom.values()))) if geom else None
    if recall >= 0.999 and (mean_delta is None or mean_delta <= geom_tol):
        verdict = "MATCH"
    elif recall >= 0.5:
        verdict = "PARTIAL"
    else:
        verdict = "MISMATCH"
    return Comparison(shared, sorted(a.families - b.families), sorted(b.families - a.families),
                      geom, recall, mean_delta, verdict)


@dataclass
class LiteratureComparison:
    recovered: list[str]
    missing: list[str]
    extra: list[str]
    recall: float
    verdict: str


def compare_to_literature(a: ModelSummary, lit_families: list[str]) -> LiteratureComparison:
    """Family-composition comparison of a screening model against a literature family set."""
    lit = set(lit_families)
    recovered = sorted(a.families & lit)
    missing = sorted(lit - a.families)
    extra = sorted(a.families - lit)
    recall = len(recovered) / len(lit) if lit else 0.0
    verdict = "MATCH" if recall >= 0.999 else ("PARTIAL" if recall >= 0.5 else "MISMATCH")
    return LiteratureComparison(recovered, missing, extra, recall, verdict)
