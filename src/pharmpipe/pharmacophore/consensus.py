"""The consensus-strategy seam (Stage 4).

A *consensus strategy* turns per-molecule, binding-site-aligned feature points into a
list of consensus features. Two are available behind one flag, with identical in/out
contracts so downstream code never branches on the method:

  * ``kmeans``  — silhouette-k-means feature clustering (``build.py``);
  * ``density`` — Gaussian occupancy field, peaks -> features (``density.py``).

``build_consensus`` is the single entry the orchestrator calls; add a strategy here and
in ``config`` only. Both return a ``BuildResult`` (a ``Pharmacophore`` plus the
per-family ``ClusterAssignment``s the visualisation/CSV consume), so the artifacts and
their format are method-independent.
"""

from __future__ import annotations

import numpy as np

from ..clustering.registry import get_clusterer
from ..features.extract import FeatureTable
from .build import BuildResult, build_pharmacophore
from .config import PharmacophoreConfig
from .density import build_density

CONSENSUS_METHODS = ("kmeans", "density")


def build_consensus(table: FeatureTable, cfg: PharmacophoreConfig, name: str,
                    metadata: dict | None = None, *,
                    ligand_atoms: np.ndarray | None = None,
                    protein_atoms: np.ndarray | None = None,
                    scaffold_freq: dict[str, int] | None = None) -> BuildResult:
    """Dispatch to the configured consensus strategy; return a uniform BuildResult."""
    method = cfg.consensus_method
    meta = dict(metadata or {})
    meta["consensus_method"] = method
    if method == "kmeans":
        clusterer = get_clusterer(cfg.clustering.method, cfg.clustering.params)
        return build_pharmacophore(table, clusterer, cfg.selection, cfg.tolerance,
                                   name, meta)
    if method == "density":
        return build_density(table, cfg.density, cfg.tolerance, name, meta,
                             min_support=cfg.selection.min_support_fraction,
                             ligand_atoms=ligand_atoms, protein_atoms=protein_atoms,
                             scaffold_freq=scaffold_freq)
    raise ValueError(
        f"unknown consensus_method {method!r}; available: {list(CONSENSUS_METHODS)}")
