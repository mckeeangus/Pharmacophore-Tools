#!/usr/bin/env python
"""Visualise a pharmacophore + its compounds in PyMOL.

Standalone: depends only on the Python standard library and PyMOL's ``cmd`` — it
parses the ``pharmacophore_model.json`` itself, so it runs anywhere the files are copied.

Run (needs the viz environment):

    pixi run -e viz pymol -cq scripts/pymol_pharmacophore.py -- \
        --pharmacophore catalogue/<slug>/pharmacophores/<cell>/pharmacophore_model.json \
        --compounds     catalogue/<slug>/groups/<cell> \
        --out           <cell>.pse

Kept pharmacophore features are drawn as **fixed-radius mesh (wireframe) spheres**
(``PH4_SPHERE_RADIUS``) each with an opaque centre pseudoatom marking its position,
coloured by family (HBD/donor pink, HBA/acceptor green, hydrophobic cyan, aromatic
yellow, positive-ionisable red). The feature's true tolerance radius lives in the JSON,
not the sphere size. Directional features additionally carry an **orientation arrow**
(grouped ``ph4_directions``) drawn from the feature's ``direction`` vector: a single-headed
arrow along the signed lone-pair / donor vector for Donor/Acceptor, and a **double-headed**
arrow along the aromatic ring normal (an undirected axis — either ring face is equivalent).
**Excluded-Volume markers are receptor steric markers and are NOT
drawn.** ``--features features.csv`` additionally overlays the raw extracted points
(small opaque dots). Omit ``--out`` to stay in an interactive PyMOL window; ``--image
PATH`` additionally writes a ray-traced PNG snapshot.

``--sweep-out PATH`` writes a **second, separate** visualisation: a support-cutoff sweep
across 20 PyMOL states. Reading ``features.csv`` (all raw clusters, no overlap merge and
no support floor), each state raises a support cutoff by 0.05 (support = distinct ligands
with a point within ``--membership-radius`` of the cluster centre ÷ total ligands),
showing every cluster at or above it — so scrubbing states 0.05 → 1.00 reveals which
clusters survive as the bar rises. ``--sweep-image PATH`` snapshots state 1 (all clusters).

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

# Ligand feature spheres are drawn at a FIXED display radius (not the tolerance radius,
# which is up to 3 A and swamps the scene). The true tolerance stays in pharmacophore_model.json.
# This is a pure display size (a mesh/wireframe sphere), independent of the tolerance and
# the 1 A merge cutoff.
PH4_SPHERE_RADIUS = 1.25

# Orientation arrows for directional features (drawn from the feature centre along its
# `direction` vector). Donor/Acceptor get a single-headed arrow along the signed lone-pair /
# donor-approach vector; Aromatic gets a DOUBLE-headed arrow along the ring normal, because that
# normal is an undirected axis (either ring face is equivalent) — a single head would imply a
# direction the chemistry does not have.
ARROW_LEN = 2.2       # display length of a direction arrow (A) from the centre
ARROW_SHAFT_R = 0.10  # shaft radius
ARROW_HEAD_R = 0.30   # arrowhead base radius
ARROW_HEAD_FRAC = 0.40  # fraction of the length taken by the head


def _unit(v):
    n = math.sqrt(sum(c * c for c in v))
    return [c / n for c in v] if n > 1e-6 else None


def _arrow_cgo(base, direction, rgb):
    """CGO list for one single-headed arrow: a shaft cylinder + a cone head, from ``base`` along
    the unit ``direction`` for ``ARROW_LEN`` A. Colour ``rgb`` (0-1 triple). Every element is a
    float — PyMOL's CGO parser silently rejects a buffer containing ints."""
    from pymol.cgo import CONE, CYLINDER
    r, g, b = (float(c) for c in rgb)
    base = [float(c) for c in base]
    tip = [base[k] + ARROW_LEN * float(direction[k]) for k in range(3)]
    neck = [base[k] + ARROW_LEN * (1.0 - ARROW_HEAD_FRAC) * float(direction[k]) for k in range(3)]
    return [
        CYLINDER, base[0], base[1], base[2], neck[0], neck[1], neck[2],
        ARROW_SHAFT_R, r, g, b, r, g, b,
        CONE, neck[0], neck[1], neck[2], tip[0], tip[1], tip[2],
        ARROW_HEAD_R, 0.0, r, g, b, r, g, b, 1.0, 1.0,
    ]


def _draw_direction(name, pos, direction, family, rgb):
    """Draw the orientation arrow(s) for one directional feature; returns True if drawn.

    Aromatic is rendered as a symmetric double-headed axis (arrows both ways from the centre);
    Donor/Acceptor as a single arrow along the true (signed) vector."""
    u = _unit(direction)
    if u is None:
        return False
    if family == "Aromatic":                       # undirected axis -> both directions
        cgo = _arrow_cgo(pos, u, rgb) + _arrow_cgo(pos, [-c for c in u], rgb)
    else:                                           # signed lone-pair / D-H vector
        cgo = _arrow_cgo(pos, u, rgb)
    cmd.load_cgo(cgo, name)
    cmd.group("ph4_directions", name)
    return True


def _args(argv):
    ap = argparse.ArgumentParser()
    ap.add_argument("--pharmacophore", required=True)
    ap.add_argument("--compounds", help="optional aligned ligands to overlay: a directory of "
                    "*.mol2, or a single multi-molecule .sdf/.mol2")
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
    ap.add_argument("--membership-radius", dest="membership_radius", type=float, default=1.5,
                    help="sweep support radius (A): a ligand supports a cluster only if it "
                         "has a point within this of the centre (matches config)")
    return ap.parse_args(argv)


def _set_colors():
    for family, rgb in COLORS.items():
        cmd.set_color(f"ph4_{family}", list(rgb))


def load_ligand(ligand_path):
    cmd.load(ligand_path, "ligand")
    cmd.hide("everything", "ligand")
    cmd.show("sticks", "ligand")
    cmd.color("grey70", "ligand and elem C")


def _clean_obj_name(raw, fallback):
    """A PyMOL-safe object name from a molecule title (or a fallback)."""
    nm = "".join(c if (c.isalnum() or c == "_") else "_" for c in (raw or "").strip())
    return nm or fallback


def load_compounds(compounds):
    """Load the raw ligands as **separate, individually-toggleable objects** grouped under
    ``compounds`` — so each molecule can be viewed on its own against the pharmacophore rather
    than as one merged overlay. ``compounds`` is a directory of aligned ``*.mol2`` (one object
    per file, named by its stem) or a single multi-molecule ``.sdf``/``.mol2`` (one object per
    record, named by its title / mol_id). Returns the number of molecule objects created."""
    names = []
    if os.path.isdir(compounds):
        for path in sorted(glob.glob(os.path.join(compounds, "*.mol2"))):
            nm = _clean_obj_name(os.path.splitext(os.path.basename(path))[0], "cmpd")
            cmd.load(path, nm)
            names.append(nm)
    elif os.path.isfile(compounds):
        tmp = "_compounds_tmp"
        cmd.load(compounds, tmp)
        for state in range(1, cmd.count_states(tmp) + 1):
            nm = _clean_obj_name(cmd.get_title(tmp, state), f"cmpd_{state}")
            if nm in names:                       # de-dupe identical titles
                nm = f"{nm}_{state}"
            cmd.create(nm, tmp, source_state=state, target_state=1)
            names.append(nm)
        cmd.delete(tmp)
    if not names:
        return 0
    for nm in names:
        cmd.hide("everything", nm)
        cmd.show("sticks", nm)
        cmd.color("grey70", f"{nm} and elem C")
        cmd.group("compounds", nm)              # collapsible group; each still toggles on its own
    return len(names)


def load_features(json_path):
    with open(json_path, encoding="utf-8") as fh:
        model = json.load(fh)
    has_features = False
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
        # ... plus an orientation arrow for directional features (donor/acceptor lone-pair vector,
        # aromatic ring normal), drawn from the `direction` the model recorded. Grouped so it can
        # be toggled independently of the spheres.
        direction = feat.get("direction")
        if direction:
            _draw_direction(f"{family}_dir_{i}", pos, direction,
                            family, COLORS.get(family, _GREY))
        has_features = True
    if has_features:                       # some cells keep only excluded volume -> no spheres
        _show_mesh_spheres()
        # centres are opaque nonbonded-sphere points, not mesh
        cmd.hide("mesh", "ph4_centers")
        cmd.show("nb_spheres", "ph4_centers")
    return model.get("name", os.path.basename(json_path))


def _show_mesh_spheres():
    """Render the ph4_* feature pseudoatoms as mesh (wireframe) spheres.

    Pseudoatoms are excluded from surfaces by default, so their ``ignore`` flag is
    cleared before ``show mesh`` renders each vdw sphere as a wireframe. A raised
    ``surface_quality`` smooths the spheres from a coarse polyhedron into a round mesh."""
    cmd.set("surface_quality", 2)
    cmd.set("mesh_width", 0.6)
    cmd.flag("ignore", "ph4_*", "clear")
    cmd.show("mesh", "ph4_*")


def _read_clusters(features_csv, n_ligands, membership_radius, min_cluster_size):
    """Per (family, cluster): centroid + support from a features.csv (EV-free).

    ``support = distinct ligands with a point within ``membership_radius`` of the cluster
    centre / ``n_ligands`` — the same hard-membership rule the model uses (a far basin
    outlier does not count). Support is measured over ALL points of the family, so a
    ligand whose nearest point sits in a neighbouring basin still counts if it reaches."""
    by_family = defaultdict(list)                 # family -> [(x, y, z, ligand), ...]
    by_cluster = defaultdict(list)                # (family, cluster) -> [...]
    with open(features_csv, encoding="utf-8") as fh:
        for row in csv.DictReader(fh):
            pt = (float(row["x"]), float(row["y"]), float(row["z"]), row["ligand_id"])
            by_family[row["family"]].append(pt)
            by_cluster[(row["family"], row["cluster"])].append(pt)
    r2 = membership_radius * membership_radius
    clusters = []
    for (family, _cl), rows in by_cluster.items():
        if len(rows) < min_cluster_size:
            continue
        cx = sum(r[0] for r in rows) / len(rows)
        cy = sum(r[1] for r in rows) / len(rows)
        cz = sum(r[2] for r in rows) / len(rows)
        ligs = {lig for (x, y, z, lig) in by_family[family]
                if (x - cx) ** 2 + (y - cy) ** 2 + (z - cz) ** 2 <= r2}
        clusters.append({
            "family": family, "x": cx, "y": cy, "z": cz,
            "support": len(ligs) / n_ligands if n_ligands else 0.0,
        })
    return clusters


def load_sweep(features_csv, n_ligands, membership_radius, min_cluster_size, step=0.05):
    """Build the support-cutoff sweep across 20 states; returns the number of states.

    Each raw cluster (no overlap merge, no support floor) is a mesh sphere present in
    states ``1..floor(support/step)`` — so as the state (support cutoff) rises from 0.05
    to 1.00, poorly-supported clusters drop out and the well-supported ones remain."""
    clusters = _read_clusters(features_csv, n_ligands, membership_radius, min_cluster_size)
    if not clusters:
        return 0
    # A cluster whose support sits in [step, 2*step) spans a single state, making it a
    # single-coordinate-state object; with PyMOL's default static_singletons those objects
    # are drawn in EVERY frame, so the weakest clusters bleed across the whole sweep. Turn it
    # off so each cluster shows only in the states it actually occupies.
    cmd.set("static_singletons", 0)
    n_states = round(1.0 / step)                  # 0.05 .. 1.00 -> 20 states
    for idx, c in enumerate(clusters):
        k_max = min(n_states, math.floor(c["support"] / step + 1e-9))
        if k_max < 1:                             # support below the lowest cutoff
            continue
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
                       label=f"support >= {step * k:.2f}")
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

    # --- support-cutoff sweep (separate file, 20 states, 0.05 -> 1.00) ---
    if args.sweep_out or args.sweep_image:
        features_csv = args.features or os.path.join(
            os.path.dirname(args.pharmacophore), "features.csv")
        if not os.path.exists(features_csv):
            print(f"sweep skipped: no features.csv ({features_csv})")
            return
        with open(args.pharmacophore, encoding="utf-8") as fh:
            n_ligands = int((json.load(fh).get("metadata", {})
                             .get("source", {}).get("n_ligands", 0)) or 0)
        if not n_ligands:
            print("sweep skipped: n_ligands unknown (needs metadata.source.n_ligands)")
            return
        _new_scene()
        _load_ligand_or_compounds(args, ligand)
        n_states = load_sweep(features_csv, n_ligands, args.membership_radius,
                              args.min_cluster_size)
        if n_states == 0:
            print("sweep skipped: no clusters")
            return
        cmd.orient()
        cmd.set("state", 1)
        print(f"{name}: support sweep with {n_states} states")
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
