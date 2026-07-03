"""Stage 4: RDKit pharmacophore-feature extraction from grouped poses.

``extract`` is the pure core (molecules -> feature points); ``load`` is the IO edge
(mol2 files -> RDKit molecules).
"""

from .extract import (
    FeaturePoint,
    FeatureResolution,
    FeatureTable,
    build_table,
    feature_factory,
    featurize,
    hierarchy_pairs,
)
from .load import LoadReport, load_directory, load_pose, read_smiles_map

__all__ = [
    "FeaturePoint", "FeatureResolution", "FeatureTable", "build_table", "featurize",
    "feature_factory", "hierarchy_pairs", "LoadReport", "load_directory", "load_pose",
    "read_smiles_map",
]
