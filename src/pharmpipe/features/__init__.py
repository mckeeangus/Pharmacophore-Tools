"""Stage 4: RDKit pharmacophore-feature extraction from grouped poses.

``extract`` is the pure core (molecules -> feature points); ``load`` is the IO edge
(mol2 files -> RDKit molecules).
"""

from .extract import FeaturePoint, FeatureTable, build_table, feature_factory, featurize
from .load import LoadReport, load_directory, load_pose, read_smiles_map

__all__ = [
    "FeaturePoint", "FeatureTable", "build_table", "featurize", "feature_factory",
    "LoadReport", "load_directory", "load_pose", "read_smiles_map",
]
