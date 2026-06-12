"""Render a per-target PyMOL session: the reference protein (cartoon) with the
site anchor highlighted, plus every site-filtered ligand pose superposed into the
same frame, so the bound poses can be compared at a glance.

Two artifacts:
  * ``<slug>_aligned.pml`` — a portable, diff-able script (always written; open
    it with ``pymol <slug>_aligned.pml`` from the target directory).
  * ``<slug>_aligned.pse`` — a self-contained session baked by PyMOL (written
    when PyMOL is importable, e.g. ``pixi run -e viz build-sessions``).
"""

from __future__ import annotations

import logging
from pathlib import Path

from ..util.paths import (
    target_aligned_mol2_dir,
    target_reference_pdb,
    target_session_pml,
    target_session_pse,
)
from .filter import AlignTargetResult

log = logging.getLogger("pharmpipe.sites.visualize")

# A small palette to give overlaid ligand poses distinct carbon colours.
_PALETTE = ["green", "cyan", "magenta", "yellow", "salmon", "lightblue", "orange",
            "purple", "teal", "wheat", "slate", "pink", "limon", "deepteal"]


def _ligand_objects(out: AlignTargetResult) -> list[tuple[str, str]]:
    """(object_name, relative_path) for each aligned ligand mol2."""
    objs = []
    for p in sorted(out.aligned_files, key=lambda x: x.name):
        objs.append((f"lig_{p.stem}", f"ligands/aligned_mol2/{p.name}"))
    return objs


def write_pml(out: AlignTargetResult) -> Path:
    slug = out.slug
    anchor = out.site.anchor_het
    objs = _ligand_objects(out)
    lines = [
        f"# {slug} — site-aligned ligand overlay ({len(objs)} poses)",
        f"# Reference {out.site.reference_pdb}; anchor {anchor}.",
        "# Open from this directory:  pymol "
        f"{target_session_pml(slug).name}",
        "reinitialize",
        "bg_color white",
        "set valence, 1",
        "",
        "load reference.pdb, reference",
        "hide everything, reference",
        "show cartoon, reference",
        "color grey80, reference",
        f"select anchor, reference and resn {anchor}",
        "show sticks, anchor",
        "color yellow, anchor",
        "",
    ]
    for name, rel in objs:
        lines.append(f"load {rel}, {name}")
    if objs:
        lines += [
            "",
            "group ligands, lig_*",
            "show sticks, ligands",
            "hide everything, hydro",
            "util.cbag ligands",
            "set stick_radius, 0.15, ligands",
        ]
    lines += ["", "orient anchor", "zoom anchor, 12", ""]
    path = target_session_pml(slug)
    path.write_text("\n".join(lines), encoding="utf-8")
    return path


def build_pse(out: AlignTargetResult) -> Path | None:
    """Bake a .pse using PyMOL (best-effort; returns None if PyMOL unavailable)."""
    try:
        import pymol
        from pymol import cmd, util
    except Exception as exc:  # noqa: BLE001
        log.info("PyMOL not available (%s); wrote .pml only for %s", exc, out.slug)
        return None

    slug = out.slug
    ref_pdb = target_reference_pdb(slug)
    aligned_dir = target_aligned_mol2_dir(slug)
    if not ref_pdb.exists():
        return None

    pymol.finish_launching(["pymol", "-qc"])  # quiet, no GUI
    cmd.reinitialize()
    cmd.bg_color("white")
    cmd.set("valence", 1)

    cmd.load(str(ref_pdb), "reference")
    cmd.hide("everything", "reference")
    cmd.show("cartoon", "reference")
    cmd.color("grey80", "reference")
    cmd.select("anchor", f"reference and resn {out.site.anchor_het}")
    cmd.show("sticks", "anchor")
    cmd.color("yellow", "anchor")

    for i, p in enumerate(sorted(out.aligned_files, key=lambda x: x.name)):
        name = f"lig_{p.stem}"
        cmd.load(str(aligned_dir / p.name), name)
        cmd.show("sticks", name)
        util.cbac(name)  # colour by atom; we override carbons next
        cmd.color(_PALETTE[i % len(_PALETTE)], f"{name} and elem C")
    if out.aligned_files:
        cmd.group("ligands", "lig_*")
    cmd.hide("everything", "hydro")
    cmd.set("stick_radius", 0.15, "ligands")
    cmd.deselect()
    cmd.orient("anchor")
    cmd.zoom("anchor", 12)

    pse = target_session_pse(slug)
    cmd.save(str(pse))
    log.info("[%s] wrote session %s (%d poses)", slug, pse.name, len(out.aligned_files))
    return pse


def build_session(out: AlignTargetResult, make_pse: bool = True) -> dict[str, Path]:
    artifacts = {"pml": write_pml(out)}
    if make_pse:
        pse = build_pse(out)
        if pse is not None:
            artifacts["pse"] = pse
    return artifacts
