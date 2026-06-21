"""Stage 4: ensemble pharmacophore assembly from clustered features.

``build_pharmacophore`` is the pure core (FeatureTable + Clusterer -> model);
``build_from_directory`` / ``build_for_cell`` are the IO orchestration entry points;
``Pharmacophore`` is the schema-versioned data model with JSON round-tripping.
"""

from .build import BuildResult, build_pharmacophore
from .config import PharmacophoreConfig, load_pharmacophore_config
from .model import Pharmacophore, PharmacophoreFeature
from .run import ModelOutputs, build_for_cell, build_from_directory

__all__ = [
    "BuildResult", "build_pharmacophore",
    "PharmacophoreConfig", "load_pharmacophore_config",
    "Pharmacophore", "PharmacophoreFeature",
    "ModelOutputs", "build_for_cell", "build_from_directory",
]
