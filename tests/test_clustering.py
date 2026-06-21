"""Unit tests for Stage 4 clustering — pure, offline."""

from __future__ import annotations

import numpy as np

from pharmpipe.clustering import KMeansSilhouette, available, get_clusterer


def test_registry_resolves_method():
    assert "kmeans_silhouette" in available()
    clus = get_clusterer("kmeans_silhouette", {"k_max": 4})
    assert isinstance(clus, KMeansSilhouette)
    assert clus.k_max == 4


def test_unknown_method_raises():
    try:
        get_clusterer("does_not_exist")
    except ValueError as exc:
        assert "unknown clustering method" in str(exc)
    else:  # pragma: no cover
        raise AssertionError("expected ValueError")


def test_silhouette_finds_three_blobs():
    rng = np.random.default_rng(0)
    centers = np.array([[0, 0, 0], [10, 0, 0], [0, 10, 0]], dtype=float)
    coords = np.vstack([c + rng.normal(scale=0.3, size=(15, 3)) for c in centers])
    labels = KMeansSilhouette(k_min=2, k_max=8).fit_predict(coords)
    assert len(set(labels.tolist())) == 3
    # every blob's points share one label
    for i in range(3):
        block = labels[i * 15:(i + 1) * 15]
        assert len(set(block.tolist())) == 1


def test_small_inputs_collapse_to_one_cluster():
    assert KMeansSilhouette().fit_predict(np.empty((0, 3))).tolist() == []
    assert KMeansSilhouette().fit_predict(np.zeros((1, 3))).tolist() == [0]
    assert KMeansSilhouette().fit_predict(np.zeros((2, 3))).tolist() == [0, 0]


def test_coincident_points_do_not_crash():
    coords = np.zeros((6, 3))
    labels = KMeansSilhouette().fit_predict(coords)
    assert len(labels) == 6


def test_describe_carries_params():
    d = KMeansSilhouette(k_min=2, k_max=5).describe()
    assert d["method"] == "kmeans_silhouette"
    assert d["params"]["k_max"] == 5
