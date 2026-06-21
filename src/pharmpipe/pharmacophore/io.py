"""Read/write pharmacophore artifacts (Stage 4, IO edge).

The JSON model is canonical; the rest are conveniences for inspection and PyMOL.
"""

from __future__ import annotations

import csv
import json
import os
from pathlib import Path

from .build import BuildResult
from .model import Pharmacophore


def write_json(ph: Pharmacophore, path: Path) -> Path:
    path.write_text(json.dumps(ph.to_dict(), indent=2), encoding="utf-8")
    return path


def read_json(path: Path) -> Pharmacophore:
    return Pharmacophore.from_dict(json.loads(Path(path).read_text(encoding="utf-8")))


def write_features_csv(result: BuildResult, path: Path) -> Path:
    """Every raw feature point with its family, cluster id, and kept flag.

    This is the data the user inspects to judge clustering quality and to prototype
    alternative methods.
    """
    with path.open("w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["family", "ligand_id", "x", "y", "z", "cluster", "kept"])
        for a in result.assignments:
            for (x, y, z), lbl, lig in zip(a.coords.tolist(), a.labels.tolist(),
                                           a.ligand_ids, strict=True):
                w.writerow([a.family, lig, round(x, 3), round(y, 3), round(z, 3),
                            int(lbl), int(lbl in a.kept_labels)])
    return path


def write_pml(ph: Pharmacophore, compounds_dir: Path, path: Path,
              colors: dict[str, list[float]]) -> Path:
    """Portable PyMOL script: load the cell's compounds + feature spheres.

    Self-contained (no pharmpipe import needed to run it). Compound paths are
    written relative to the script, so the session is reproducible wherever the
    files are copied. The richer ``scripts/pymol_pharmacophore.py`` reads the JSON
    directly and adds a raw-feature overlay; this ``.pml`` is the lightweight,
    always-written companion.
    """
    rel_dir = os.path.relpath(compounds_dir, path.parent)
    lines = [
        f"# {ph.name} — ensemble pharmacophore ({len(ph.features)} features)",
        f"# run from this file's directory:  pymol {path.name}",
        "reinitialize", "bg_color white", "set valence, 1", "",
    ]
    for mol2 in sorted(compounds_dir.glob("*.mol2")):
        rel = Path(rel_dir, mol2.name).as_posix()
        lines.append(f"load {rel}, compounds")
    lines += ["hide everything, compounds", "show lines, compounds",
              "color grey70, compounds and elem C", ""]
    for fam, col in colors.items():
        lines.append(f"set_color ph4_{fam}, [{col[0]}, {col[1]}, {col[2]}]")
    lines.append("")
    for i, feat in enumerate(ph.features):
        obj = f"{feat.family}_{i}"
        lines.append(f"pseudoatom {obj}, pos=[{feat.x:.3f}, {feat.y:.3f}, {feat.z:.3f}], "
                     f"vdw={feat.radius:.3f}")
        lines.append(f"color ph4_{feat.family}, {obj}")
        lines.append(f"group ph4_{feat.family}, {obj}")
    lines += ["show spheres, ph4_*", "set sphere_transparency, 0.4, ph4_*",
              "orient", ""]
    path.write_text("\n".join(lines), encoding="utf-8")
    return path
