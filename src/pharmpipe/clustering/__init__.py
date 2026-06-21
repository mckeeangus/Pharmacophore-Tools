"""Stage 4: swappable clustering of feature points within a (pocket x efficacy) cell.

``get_clusterer`` resolves a method name from config to a strategy implementing the
``Clusterer`` protocol; the pharmacophore builder depends only on that protocol.
"""

from .base import Clusterer
from .kmeans import KMeansSilhouette
from .registry import available, get_clusterer

__all__ = ["Clusterer", "KMeansSilhouette", "available", "get_clusterer"]
