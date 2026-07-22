"""Stage 4: ensemble pharmacophore assembly from a Gaussian occupancy field.

``build_density`` is the pure consensus core (FeatureTable -> model);
``build_from_directory`` / ``build_for_cell`` are the IO orchestration entry points;
``Pharmacophore`` is the schema-versioned data model with JSON round-tripping.
"""

from .build import BuildResult
from .config import PharmacophoreConfig, load_pharmacophore_config
from .density import build_density
from .model import Pharmacophore, PharmacophoreFeature
from .run import ModelOutputs, build_for_cell, build_from_directory

__all__ = [
    "BuildResult", "build_density",
    "PharmacophoreConfig", "load_pharmacophore_config",
    "Pharmacophore", "PharmacophoreFeature",
    "ModelOutputs", "build_for_cell", "build_from_directory",
]
