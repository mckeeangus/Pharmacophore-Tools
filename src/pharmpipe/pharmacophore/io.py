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

# Feature spheres render at a small FIXED radius (the tolerance radius, up to 3 A,
# swamps the scene); the true tolerance is preserved in pharmacophore.json.
PH4_SPHERE_RADIUS = 0.5


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


def write_representative_sdf(mol, ligand_id: str, path: Path) -> Path:
    """Write one representative ligand to SDF (bond orders + 3D coords intact).

    The catalogue mol2 are heavy-atom-only and render with spurious bonds in PyMOL;
    this is the RDKit molecule the loader already perceived (correct bond orders via
    the SMILES template), so the SDF displays cleanly. ``ligand_id`` becomes the
    molecule title.
    """
    from rdkit import Chem  # local import keeps RDKit at this IO edge

    m = Chem.Mol(mol)
    m.SetProp("_Name", ligand_id)
    with Chem.SDWriter(str(path)) as w:
        w.write(m)
    return path


def write_pml(ph: Pharmacophore, path: Path, colors: dict[str, list[float]],
              ligand_file: Path | None = None) -> Path:
    """Portable PyMOL script: load the representative ligand + feature spheres.

    Self-contained (no pharmpipe import needed to run it). The ligand path is
    written relative to the script, so the session is reproducible wherever the
    files are copied. The richer ``scripts/pymol_pharmacophore.py`` reads the JSON
    directly and adds a raw-feature overlay; this ``.pml`` is the lightweight,
    always-written companion.
    """
    lines = [
        f"# {ph.name} — ensemble pharmacophore ({len(ph.features)} features)",
        f"# run from this file's directory:  pymol {path.name}",
        "reinitialize", "bg_color white", "set valence, 1", "",
    ]
    if ligand_file is not None:
        rel = os.path.relpath(ligand_file, path.parent).replace(os.sep, "/")
        lines += [f"load {rel}, ligand",
                  "hide everything, ligand", "show sticks, ligand",
                  "color grey70, ligand and elem C", ""]
    for fam, col in colors.items():
        lines.append(f"set_color ph4_{fam}, [{col[0]}, {col[1]}, {col[2]}]")
    lines.append("")
    for i, feat in enumerate(ph.features):
        obj = (feat.label or f"{feat.family} {i}").replace(" ", "_")
        pos = f"pos=[{feat.x:.3f}, {feat.y:.3f}, {feat.z:.3f}]"
        # small fixed-radius translucent sphere ...
        lines.append(f"pseudoatom {obj}, {pos}, vdw={PH4_SPHERE_RADIUS:.3f}")
        lines.append(f"color ph4_{feat.family}, {obj}")
        lines.append(f"group ph4_{feat.family}, {obj}")
        # ... plus an opaque point marker (pseudoatom) at the exact centre.
        ctr = f"{obj}_ctr"
        lines.append(f"pseudoatom {ctr}, {pos}, "
                     f"label=\"{feat.label or feat.family} ({feat.support:.2f})\"")
        lines.append(f"color ph4_{feat.family}, {ctr}")
        lines.append(f"group ph4_centers, {ctr}")
    lines += ["show spheres, ph4_*", "set sphere_transparency, 0.4, ph4_*",
              "hide spheres, ph4_centers", "show nb_spheres, ph4_centers",
              "orient", ""]
    path.write_text("\n".join(lines), encoding="utf-8")
    return path
