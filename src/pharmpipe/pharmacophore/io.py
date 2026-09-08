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

# Ligand feature spheres render at a FIXED display radius (the tolerance radius, up to
# 3 A, swamps the scene); the true tolerance is preserved in pharmacophore.json. This is
# a pure display size (a mesh/wireframe sphere), independent of the tolerance and the 1 A
# merge cutoff.
PH4_SPHERE_RADIUS = 1.25
EV_FAMILY = "ExcludedVolume"


def write_json(ph: Pharmacophore, path: Path) -> Path:
    path.write_text(json.dumps(ph.to_dict(), indent=2), encoding="utf-8")
    return path


def read_json(path: Path) -> Pharmacophore:
    return Pharmacophore.from_dict(json.loads(Path(path).read_text(encoding="utf-8")))


# The pharmacophore CSV is the tool-to-tool interchange (construction -> visualisation):
# one row per consensus feature. Feature rows only (the ligand-based tools have no receptor,
# hence no excluded volume). The JSON stays the lossless canonical model.
_MODEL_CSV_COLUMNS = ["family", "label", "x", "y", "z", "radius", "n_points", "n_ligands",
                      "support", "dx", "dy", "dz"]


def write_model_csv(ph: Pharmacophore, path: Path) -> Path:
    """Write the pharmacophore model to a flat CSV (one row per feature).

    ``dx,dy,dz`` carry the optional orientation vector (blank when the feature has none). The
    downstream visualiser reads this with ``read_model_csv``.
    """
    with Path(path).open("w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(_MODEL_CSV_COLUMNS)
        for f in ph.features:
            if f.family == EV_FAMILY:
                continue  # the interchange is purely ligand-based: feature rows only
            d = f.direction if f.direction is not None else ("", "", "")
            w.writerow([f.family, f.label, round(f.x, 4), round(f.y, 4), round(f.z, 4),
                        round(f.radius, 4), f.n_points, f.n_ligands, round(f.support, 4),
                        *(round(c, 4) if c != "" else "" for c in d)])
    return path


def read_model_csv(path: Path) -> Pharmacophore:
    """Reconstruct a ``Pharmacophore`` from a model CSV written by ``write_model_csv``.

    The model name is the file stem. The CSV does not carry the full JSON metadata, but the
    total ligand count (needed by the support sweep) is recovered as the max feature
    ``n_ligands`` and stored under ``metadata.source.n_ligands``.
    """
    from .model import PharmacophoreFeature

    feats: list[PharmacophoreFeature] = []
    with Path(path).open(encoding="utf-8") as fh:
        for row in csv.DictReader(fh):
            dxyz = (row.get("dx"), row.get("dy"), row.get("dz"))
            direction = (tuple(float(c) for c in dxyz)
                         if all(c not in (None, "") for c in dxyz) else None)
            feats.append(PharmacophoreFeature(
                family=row["family"], x=float(row["x"]), y=float(row["y"]), z=float(row["z"]),
                radius=float(row["radius"]), n_points=int(row["n_points"]),
                n_ligands=int(row["n_ligands"]), support=float(row["support"]),
                direction=direction, label=row.get("label", "")))
    n_ligands = max((f.n_ligands for f in feats), default=0)
    metadata = {"source": {"n_ligands": n_ligands}} if n_ligands else {}
    return Pharmacophore(name=Path(path).stem, features=feats, metadata=metadata)


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


def write_aligned_sdf(entries, path: Path) -> Path:
    """Write the feature-aligned compound set to one multi-record SDF.

    ``entries`` is an iterable of ``(mol, conf_id, rotation, translation, tags)`` — one per
    aligned compound. Each molecule's chosen conformer is rigidly transformed (``x' = R·x + t``)
    into the common alignment frame and written with its ``tags`` (mol_id, DrugCLIP rank, chosen
    conformer, alignment RMSD) as SD properties. This is the hand-off deliverable: the existing
    Gaussian-KDE (`build_density`) — or any consensus method — runs on features re-perceived from
    these aligned poses.
    """
    import numpy as np
    from rdkit import Chem
    from rdkit.Geometry import Point3D

    with Chem.SDWriter(str(path)) as w:
        for mol, conf_id, rot, trans, tags in entries:
            m = Chem.Mol(mol)                       # full copy, keeps conformer ids
            conf = m.GetConformer(conf_id)
            pos = conf.GetPositions() @ np.asarray(rot).T + np.asarray(trans)
            for i in range(m.GetNumAtoms()):
                conf.SetAtomPosition(i, Point3D(*(float(c) for c in pos[i])))
            m.SetProp("_Name", str(tags.get("mol_id", "")))
            for k, v in tags.items():
                m.SetProp(str(k), str(v))
            w.write(m, confId=conf_id)
    return path


def write_aligned_points_csv(points, path: Path) -> Path:
    """Write the pooled aligned feature points (family, ligand_id, x, y, z, direction) to CSV.

    The align-only hand-off: consensus extraction (KDE) consumes these directly, so a model can
    be built without re-perceiving features from the SDF. ``points`` are
    ``(family, xyz, direction|None, ligand_id)``; the direction columns are blank when absent."""
    with path.open("w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["family", "ligand_id", "x", "y", "z", "dx", "dy", "dz"])
        for fam, xyz, direction, lig in points:
            d = ["", "", ""] if direction is None else [round(float(c), 3) for c in direction]
            w.writerow([fam, lig, round(float(xyz[0]), 3), round(float(xyz[1]), 3),
                        round(float(xyz[2]), 3), *d])
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
    has_features = False
    for i, feat in enumerate(ph.features):
        # Excluded-volume markers are receptor steric markers, not ligand chemistry —
        # they stay in the JSON model but are never drawn in the visualisation.
        if feat.family == EV_FAMILY:
            continue
        obj = (feat.label or f"{feat.family} {i}").replace(" ", "_")
        pos = f"pos=[{feat.x:.3f}, {feat.y:.3f}, {feat.z:.3f}]"
        # fixed-radius mesh (wireframe) sphere ...
        lines.append(f"pseudoatom {obj}, {pos}, vdw={PH4_SPHERE_RADIUS:.3f}")
        lines.append(f"color ph4_{feat.family}, {obj}")
        lines.append(f"group ph4_{feat.family}, {obj}")
        # ... plus an opaque point marker (pseudoatom) at the exact centre.
        ctr = f"{obj}_ctr"
        lines.append(f"pseudoatom {ctr}, {pos}, "
                     f"label=\"{feat.label or feat.family} ({feat.support:.2f})\"")
        lines.append(f"color ph4_{feat.family}, {ctr}")
        lines.append(f"group ph4_centers, {ctr}")
        has_features = True
    # Some cells keep only excluded volume (no ligand features) — then there are no
    # ph4_* objects to style, so skip the mesh/centre directives (they'd error).
    if has_features:
        lines += ["set surface_quality, 2", "flag ignore, ph4_*, clear",
                  "show mesh, ph4_*", "hide mesh, ph4_centers",
                  "show nb_spheres, ph4_centers"]
    lines += ["orient", ""]
    path.write_text("\n".join(lines), encoding="utf-8")
    return path
