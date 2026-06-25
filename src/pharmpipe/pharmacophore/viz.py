"""Raw-data visualisation of extracted features (Stage 4, IO edge).

For every model we render the *individual* extracted feature points (before they
collapse into the pharmacophore), coloured by cluster, with kept-cluster centres
marked. This is how the data's shape is inspected by eye — to judge whether k-means
suits it or a different clustering method would do better. Matplotlib only (offline,
headless Agg backend); no PyMOL needed.
"""

from __future__ import annotations

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402

from .build import BuildResult  # noqa: E402

# Distinct cluster colours (cycled); kept-cluster centres are drawn black.
_CLUSTER_CMAP = "tab10"


def _scatter_axes(ax, coords: np.ndarray, labels: np.ndarray, centers: dict,
                  kept: set[int]) -> None:
    if len(coords):
        ax.scatter(coords[:, 0], coords[:, 1], coords[:, 2], c=labels,
                   cmap=_CLUSTER_CMAP, s=25, alpha=0.7, depthshade=True)
    # Centre marker AREA scales with the cluster's point count (its population /
    # local density): a bigger marker = more feature points collapsed into that
    # centre. Kept clusters are drawn as a filled "X", dropped ones a thin "x".
    counts = {int(lbl): int((labels == lbl).sum()) for lbl in centers}
    for label, center in centers.items():
        is_kept = label in kept
        marker = "X" if is_kept else "x"
        size = 40 + counts[label] * (24 if is_kept else 8)
        ax.scatter(*center, c="black", marker=marker, s=size)
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_zlabel("z")


def plot_raw_features(result: BuildResult, out_dir: Path) -> list[Path]:
    """One 3D scatter PNG per family + a combined-by-family overview."""
    written: list[Path] = []
    for a in result.assignments:
        fig = plt.figure(figsize=(6, 5))
        ax = fig.add_subplot(111, projection="3d")
        _scatter_axes(ax, a.coords, a.labels, a.centers, a.kept_labels)
        n_kept = len(a.kept_labels)
        n_clusters = len(set(a.labels.tolist())) if len(a.labels) else 0
        ax.set_title(f"{result.pharmacophore.name}\n{a.family}: "
                     f"{len(a.coords)} points, {n_clusters} clusters, {n_kept} kept")
        fig.tight_layout()
        path = out_dir / f"raw_features_{a.family}.png"
        fig.savefig(path, dpi=120)
        plt.close(fig)
        written.append(path)
    return written
