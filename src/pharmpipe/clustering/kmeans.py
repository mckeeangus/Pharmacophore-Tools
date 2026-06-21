"""k-means clustering with silhouette-based selection of k (Stage 4).

The TeachOpenCADD T009 tutorial fixes ``k = ceil(n_points / kq)`` with a hand-tuned
``kq`` — its own discussion flags this as the obstacle to automation. We instead
choose k automatically by maximising the mean **silhouette score** over a range of
k, so no per-set hand-tuning is needed. This is registered as ``kmeans_silhouette``.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score


@dataclass
class KMeansSilhouette:
    """Pick k in ``[k_min, min(k_max, n-1)]`` by best mean silhouette score.

    Degenerate inputs collapse to a single cluster: 0–2 points, or points that are
    effectively coincident (silhouette is undefined / meaningless there).
    """

    k_min: int = 2
    k_max: int = 8
    n_init: int = 10
    random_state: int = 0
    name: str = "kmeans_silhouette"

    def fit_predict(self, coords: np.ndarray) -> np.ndarray:
        n = len(coords)
        if n <= 2:
            return np.zeros(n, dtype=int)
        k_hi = min(self.k_max, n - 1)
        k_lo = max(2, self.k_min)
        best_labels = np.zeros(n, dtype=int)
        best_score = -1.0
        for k in range(k_lo, k_hi + 1):
            labels = KMeans(n_clusters=k, n_init=self.n_init,
                            random_state=self.random_state).fit_predict(coords)
            if len(set(labels)) < 2:
                continue
            try:
                score = silhouette_score(coords, labels)
            except ValueError:
                continue
            if score > best_score:
                best_score, best_labels = score, labels
        return best_labels

    def describe(self) -> dict:
        return {"method": self.name,
                "params": {"k_min": self.k_min, "k_max": self.k_max,
                           "n_init": self.n_init, "random_state": self.random_state}}
