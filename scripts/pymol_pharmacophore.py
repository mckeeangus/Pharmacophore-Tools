#!/usr/bin/env python
"""Visualise a pharmacophore + its compounds in PyMOL.

Standalone: depends only on the Python standard library and PyMOL's ``cmd`` — it
parses the ``pharmacophore.json`` itself, so it runs anywhere the files are copied.

Run (needs the viz environment):

    pixi run -e viz pymol -cq scripts/pymol_pharmacophore.py -- \
        --pharmacophore catalogue/<slug>/pharmacophores/<cell>/pharmacophore.json \
        --compounds     catalogue/<slug>/groups/<cell> \
        --out           <cell>.pse

Kept pharmacophore features are drawn as **fixed-radius mesh (wireframe) spheres**
(``PH4_SPHERE_RADIUS``) each with an opaque centre pseudoatom marking its position,
coloured by family (HBD/donor pink, HBA/acceptor green, hydrophobic cyan, aromatic
yellow, positive-ionisable red). The feature's true tolerance radius lives in the JSON,
not the sphere size. **Excluded-Volume markers are receptor steric markers and are NOT
drawn.** ``--features features.csv`` additionally overlays the raw extracted points
(small opaque dots). Omit ``--out`` to stay in an interactive PyMOL window; ``--image
PATH`` additionally writes a ray-traced PNG snapshot.

``--sweep-out PATH`` writes a **second, separate** visualisation: an occupancy-cutoff
sweep across PyMOL states. Reading ``features.csv`` (all raw clusters, no overlap merge
and no support floor), each state raises an occupancy cutoff by 0.05 (occupancy = points
÷ contributing ligands, uncapped), showing every cluster at or above it — so scrubbing
states reveals which clusters survive as the threshold rises. ``--sweep-image PATH``
snapshots state 1 (all clusters).

By default the clean ``representative_ligand.sdf`` written beside the JSON is shown
(correct bond orders). Pass ``--compounds DIR`` to overlay the full raw mol2 set
instead (heavy-atom only — bonds may render imperfectly).
"""

import argparse
import csv
import glob
import json
import math
import os
import sys
from collections import defaultdict

try:
    from pymol import cmd
except ImportError:  # pure helpers (e.g. _read_clusters) stay importable without PyMOL
    cmd = None

# Family -> RGB (0–1). Matches config/pharmacophore.yaml so colours are consistent.
COLORS = {
    "Donor": (1.00, 0.40, 0.70),            # pink   — HBD
    "Acceptor": (0.00, 0.80, 0.00),         # green  — HBA
    "LumpedHydrophobe": (0.00, 0.90, 0.90),  # cyan   — hydrophobic
    "Aromatic": (1.00, 0.85, 0.00),         # yellow
    "PosIonizable": (1.00, 0.00, 0.00),     # red
    "NegIonizable": (1.00, 0.45, 0.00),     # orange
    "ExcludedVolume": (0.55, 0.55, 0.55),   # grey — receptor excluded-volume (density)
}
_GREY = (0.5, 0.5, 0.5)

# Ligand feature spheres are drawn at a FIXED radius (not the tolerance radius, which is
# up to 3 A and swamps the scene). The true tolerance stays in pharmacophore.json. This
# is a RADIUS, so 0.5 A draws a 1.0 A-diameter ball -- and two such spheres just touch
# when their centres are ~1 A apart, mirroring the overlap-merge rule (features within
# ~1 A collapse to one).
PH4_SPHERE_RADIUS = 0.5


def _args(argv):
    ap = argparse.ArgumentParser()
    ap.add_argument("--pharmacophore", required=True)
    ap.add_argument("--compounds", help="optional directory of aligned *.mol2 to overlay")
    ap.add_argument("--ligand", help="representative ligand to show "
                    "(default: representative_ligand.sdf beside the JSON)")
    ap.add_argument("--features", help="optional features.csv to overlay raw points "
                    "(also the source for --sweep-out; defaults to features.csv beside the JSON)")
    ap.add_argument("--out", help="write the kept-model .pse here (else interactive)")
    ap.add_argument("--image", help="write a ray-traced .png of the kept-model view here")
    ap.add_argument("--sweep-out", dest="sweep_out",
                    help="write the occupancy-cutoff sweep .pse (20+ states) here")
    ap.add_argument("--sweep-image", dest="sweep_image",
                    help="write a .png snapshot of the sweep (state 1 = all clusters) here")
    ap.add_argument("--min-cluster-size", dest="min_cluster_size", type=int, default=2,
                    help="drop sweep clusters with fewer points than this (matches config)")
    return ap.parse_args(argv)


def _set_colors():
    for family, rgb in COLORS.items():
        cmd.set_color(f"ph4_{family}", list(rgb))


def load_ligand(ligand_path):
    cmd.load(ligand_path, "ligand")
    cmd.hide("everything", "ligand")
    cmd.show("sticks", "ligand")
    cmd.color("grey70", "ligand and elem C")


def load_compounds(compounds_dir):
    files = sorted(glob.glob(os.path.join(compounds_dir, "*.mol2")))
    for path in files:
        cmd.load(path, "compounds")
    cmd.hide("everything", "compounds")
    cmd.show("lines", "compounds")
    cmd.color("grey70", "compounds and elem C")
    return len(files)


def load_features(json_path):
    with open(json_path, encoding="utf-8") as fh:
        model = json.load(fh)
    for i, feat in enumerate(model.get("features", [])):
        family = feat["family"]
        # Excluded-volume markers are receptor steric markers, not ligand chemistry —
        # part of the JSON model but never drawn in the visualisation.
        if family == "ExcludedVolume":
            continue
        pos = [feat["x"], feat["y"], feat["z"]]
        # fixed-radius mesh (wireframe) sphere ...
        sphere = f"{family}_{i}"
        cmd.pseudoatom(sphere, pos=pos, vdw=PH4_SPHERE_RADIUS)
        cmd.color(f"ph4_{family}", sphere)
        cmd.group(f"ph4_{family}", sphere)
        # ... plus an opaque point marker (pseudoatom) at the exact centre.
        centre = f"{family}_ctr_{i}"
        cmd.pseudoatom(centre, pos=pos)
        cmd.color(f"ph4_{family}", centre)
        cmd.group("ph4_centers", centre)
    _show_mesh_spheres()
    # centres are opaque nonbonded-sphere points, not mesh
    cmd.hide("mesh", "ph4_centers")
    cmd.show("nb_spheres", "ph4_centers")
    return model.get("name", os.path.basename(json_path))


def _show_mesh_spheres():
    """Render the ph4_* feature pseudoatoms as mesh (wireframe) spheres.

    Pseudoatoms are excluded from surfaces by default, so their ``ignore`` flag is
    cleared before ``show mesh`` renders each vdw sphere as a wireframe. A raised
    ``surface_quality`` smooths the small (0.5 Å) spheres from a coarse polyhedron."""
    cmd.set("surface_quality", 1)
    cmd.set("mesh_width", 0.6)
    cmd.flag("ignore", "ph4_*", "clear")
    cmd.show("mesh", "ph4_*")


def _read_clusters(features_csv, min_cluster_size):
    """Per (family, cluster) centroid + occupancy from a features.csv (EV-free by
    construction). ``occupancy = n_points / distinct ligands`` (uncapped)."""
    pts = defaultdict(list)
    with open(features_csv, encoding="utf-8") as fh:
        for row in csv.DictReader(fh):
            pts[(row["family"], row["cluster"])].append(
                (float(row["x"]), float(row["y"]), float(row["z"]), row["ligand_id"]))
    clusters = []
    for (family, _cl), rows in pts.items():
        n = len(rows)
        if n < min_cluster_size:
            continue
        n_lig = len({r[3] for r in rows})
        clusters.append({
            "family": family,
            "x": sum(r[0] for r in rows) / n,
            "y": sum(r[1] for r in rows) / n,
            "z": sum(r[2] for r in rows) / n,
            "occ": n / n_lig if n_lig else 0.0,
        })
    return clusters


def load_sweep(features_csv, min_cluster_size, step=0.05):
    """Build the occupancy-cutoff sweep across states; returns the number of states.

    Each raw cluster (no overlap merge, no support floor) is a mesh sphere present in
    states ``1..floor(occupancy/step)``; a per-state label shows the cutoff. Scrubbing
    states raises the occupancy threshold from 0.05 to the observed maximum."""
    clusters = _read_clusters(features_csv, min_cluster_size)
    if not clusters:
        return 0
    max_occ = max(c["occ"] for c in clusters)
    n_states = max(20, math.ceil(max_occ / step - 1e-9))
    for idx, c in enumerate(clusters):
        k_max = min(n_states, max(1, math.floor(c["occ"] / step + 1e-9)))
        name = f"{c['family']}_{idx}"
        for k in range(1, k_max + 1):
            cmd.pseudoatom(name, pos=[c["x"], c["y"], c["z"]],
                           vdw=PH4_SPHERE_RADIUS, state=k)
        cmd.color(f"ph4_{c['family']}", name)
        cmd.group(f"ph4_{c['family']}", name)
    # A per-state cutoff label at the cluster centroid.
    cx = sum(c["x"] for c in clusters) / len(clusters)
    cy = sum(c["y"] for c in clusters) / len(clusters)
    cz = sum(c["z"] for c in clusters) / len(clusters)
    for k in range(1, n_states + 1):
        cmd.pseudoatom("sweep_cutoff", pos=[cx, cy, cz], state=k,
                       label=f"occupancy >= {step * k:.2f}")
    _show_mesh_spheres()
    cmd.hide("everything", "sweep_cutoff")
    cmd.show("labels", "sweep_cutoff")
    cmd.set("all_states", 0)
    return n_states


def overlay_raw(features_csv):
    with open(features_csv, encoding="utf-8") as fh:
        for j, row in enumerate(csv.DictReader(fh)):
            family = row["family"]
            name = f"raw_{family}_{j}"
            cmd.pseudoatom(name, pos=[float(row["x"]), float(row["y"]), float(row["z"])],
                           vdw=0.25)
            cmd.color(f"ph4_{family}", name)
            cmd.group(f"raw_{family}", name)
    cmd.show("nb_spheres", "raw_*")


def _new_scene():
    cmd.reinitialize()
    cmd.bg_color("white")
    cmd.set("valence", 1)
    _set_colors()


def _load_ligand_or_compounds(args, ligand):
    if args.compounds:
        return f"{load_compounds(args.compounds)} raw compounds"
    if ligand:
        load_ligand(ligand)
        return f"representative {os.path.basename(ligand)}"
    return "0 ligands"


def _snapshot(path):
    """Ray-traced default-orientation snapshot (opaque white background)."""
    cmd.set("ray_opaque_background", 1)
    cmd.png(path, width=1200, height=900, dpi=150, ray=1)
    print(f"wrote {path}")


def main(argv):
    args = _args(argv)
    # Default: the clean representative SDF beside the model JSON.
    ligand = args.ligand
    if ligand is None and not args.compounds:
        cand = os.path.join(os.path.dirname(args.pharmacophore),
                            "representative_ligand.sdf")
        ligand = cand if os.path.exists(cand) else None

    # --- kept-model view (mesh spheres; excluded volume not drawn) ---
    _new_scene()
    shown = _load_ligand_or_compounds(args, ligand)
    name = load_features(args.pharmacophore)
    if args.features:
        overlay_raw(args.features)
    cmd.orient()
    print(f"{name}: {shown} + pharmacophore loaded")
    if args.out:
        cmd.save(args.out)
        print(f"wrote {args.out}")
    if args.image:
        _snapshot(args.image)

    # --- occupancy-cutoff sweep (separate file, 20+ states) ---
    if args.sweep_out or args.sweep_image:
        features_csv = args.features or os.path.join(
            os.path.dirname(args.pharmacophore), "features.csv")
        if not os.path.exists(features_csv):
            print(f"sweep skipped: no features.csv ({features_csv})")
            return
        _new_scene()
        _load_ligand_or_compounds(args, ligand)
        n_states = load_sweep(features_csv, args.min_cluster_size)
        if n_states == 0:
            print("sweep skipped: no clusters")
            return
        cmd.orient()
        cmd.set("state", 1)
        print(f"{name}: occupancy sweep with {n_states} states")
        if args.sweep_out:
            cmd.save(args.sweep_out)
            print(f"wrote {args.sweep_out}")
        if args.sweep_image:
            _snapshot(args.sweep_image)


# PyMOL runs a command-line script with ``__name__ == "pymol"`` (not "__main__")
# and passes the post-"--" args as sys.argv[1:] (the "--" is already stripped).
if __name__ in ("__main__", "pymol"):
    argv = sys.argv[1:]
    if "--" in argv:
        argv = argv[argv.index("--") + 1:]
    main(argv)
