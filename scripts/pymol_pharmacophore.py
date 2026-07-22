#!/usr/bin/env python
"""Visualise a pharmacophore + its compounds in PyMOL.

Standalone: depends only on the Python standard library and PyMOL's ``cmd`` — it
parses the ``pharmacophore.json`` itself, so it runs anywhere the files are copied.

Run (needs the viz environment):

    pixi run -e viz pymol -cq scripts/pymol_pharmacophore.py -- \
        --pharmacophore catalogue/<slug>/pharmacophores/<cell>/pharmacophore.json \
        --compounds     catalogue/<slug>/groups/<cell> \
        --out           <cell>.pse

Kept pharmacophore features are drawn as **small fixed-radius** translucent spheres
(``PH4_SPHERE_RADIUS``) each with an opaque centre pseudoatom marking its position,
coloured by family (HBD/donor pink, HBA/acceptor green, hydrophobic cyan, aromatic
yellow, positive-ionisable red). The feature's true tolerance radius lives in the JSON,
not the sphere size. ``--features features.csv`` additionally overlays the raw extracted
points (small opaque dots) so the cluster centres can be compared to the data. Omit
``--out`` to stay in an interactive PyMOL window; ``--image PATH`` additionally writes a
ray-traced PNG snapshot.

By default the clean ``representative_ligand.sdf`` written beside the JSON is shown
(correct bond orders). Pass ``--compounds DIR`` to overlay the full raw mol2 set
instead (heavy-atom only — bonds may render imperfectly).
"""

import argparse
import csv
import glob
import json
import os
import sys

from pymol import cmd

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
    ap.add_argument("--features", help="optional features.csv to overlay raw points")
    ap.add_argument("--out", help="write a .pse here (else interactive)")
    ap.add_argument("--image", help="write a ray-traced .png snapshot here")
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
        pos = [feat["x"], feat["y"], feat["z"]]
        if family == "ExcludedVolume":
            # excluded-volume markers: their own steric radius, no centre point.
            name = f"{family}_{i}"
            cmd.pseudoatom(name, pos=pos, vdw=feat["radius"])
            cmd.color(f"ph4_{family}", name)
            cmd.group(f"ph4_{family}", name)
            continue
        # fixed-radius translucent sphere ...
        sphere = f"{family}_{i}"
        cmd.pseudoatom(sphere, pos=pos, vdw=PH4_SPHERE_RADIUS)
        cmd.color(f"ph4_{family}", sphere)
        cmd.group(f"ph4_{family}", sphere)
        # ... plus an opaque point marker (pseudoatom) at the exact centre.
        centre = f"{family}_ctr_{i}"
        cmd.pseudoatom(centre, pos=pos)
        cmd.color(f"ph4_{family}", centre)
        cmd.group("ph4_centers", centre)
    cmd.show("spheres", "ph4_*")
    cmd.set("sphere_transparency", 0.4, "ph4_*")
    cmd.hide("spheres", "ph4_centers")
    cmd.show("nb_spheres", "ph4_centers")
    return model.get("name", os.path.basename(json_path))


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


def main(argv):
    args = _args(argv)
    cmd.reinitialize()
    cmd.bg_color("white")
    cmd.set("valence", 1)
    _set_colors()
    # Default: the clean representative SDF beside the model JSON.
    ligand = args.ligand
    if ligand is None and not args.compounds:
        cand = os.path.join(os.path.dirname(args.pharmacophore),
                            "representative_ligand.sdf")
        ligand = cand if os.path.exists(cand) else None
    shown = "0 ligands"
    if args.compounds:
        shown = f"{load_compounds(args.compounds)} raw compounds"
    elif ligand:
        load_ligand(ligand)
        shown = f"representative {os.path.basename(ligand)}"
    name = load_features(args.pharmacophore)
    if args.features:
        overlay_raw(args.features)
    cmd.orient()
    print(f"{name}: {shown} + pharmacophore loaded")
    if args.out:
        cmd.save(args.out)
        print(f"wrote {args.out}")
    if args.image:
        # Ray-traced default-orientation snapshot (opaque white background).
        cmd.set("ray_opaque_background", 1)
        cmd.png(args.image, width=1200, height=900, dpi=150, ray=1)
        print(f"wrote {args.image}")


# PyMOL runs a command-line script with ``__name__ == "pymol"`` (not "__main__")
# and passes the post-"--" args as sys.argv[1:] (the "--" is already stripped).
if __name__ in ("__main__", "pymol"):
    argv = sys.argv[1:]
    if "--" in argv:
        argv = argv[argv.index("--") + 1:]
    main(argv)
