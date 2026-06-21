"""The clustering strategy interface (Stage 4).

A clusterer maps a set of 3D feature points to integer cluster labels. That is the
*only* contract the pharmacophore builder depends on, so any method (k-means now,
density-based or hierarchical later) is a drop-in replacement that yields the same
output file format. Register implementations in ``registry.py``.
"""

from __future__ import annotations

from typing import Protocol, runtime_checkable

import numpy as np


@runtime_checkable
class Clusterer(Protocol):
    """Assign each row of ``coords`` (n, 3) to a cluster label in ``[0, k)``."""

    name: str

    def fit_predict(self, coords: np.ndarray) -> np.ndarray:
        """Return an integer label array of shape ``(n,)``."""
        ...

    def describe(self) -> dict:
        """Method name + parameters, for the output's ``method`` provenance block."""
        ...
