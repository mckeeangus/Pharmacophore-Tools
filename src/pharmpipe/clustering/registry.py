"""Clusterer registry — the single place to add a new clustering method.

``get_clusterer(method, params)`` is what the pipeline calls; adding a strategy is a
one-line entry here plus its implementation module. Everything downstream (feature
assembly, output format) is unchanged, so methods stay directly comparable.
"""

from __future__ import annotations

from collections.abc import Callable

from .base import Clusterer
from .kmeans import KMeansSilhouette

_REGISTRY: dict[str, Callable[..., Clusterer]] = {
    "kmeans_silhouette": KMeansSilhouette,
}


def available() -> list[str]:
    return sorted(_REGISTRY)


def get_clusterer(method: str, params: dict | None = None) -> Clusterer:
    try:
        factory = _REGISTRY[method]
    except KeyError:
        raise ValueError(
            f"unknown clustering method {method!r}; available: {available()}"
        ) from None
    return factory(**(params or {}))
