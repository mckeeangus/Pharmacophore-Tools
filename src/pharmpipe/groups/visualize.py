"""Stage 3 PyMOL sessions.

Two kinds of artifact, mirroring Stage 2's portable-.pml + baked-.pse split:

* ``<slug>_grouped.pse`` — the reference protein with every cell's poses overlaid
  and coloured by cell (the comprehensive view, with pocket context).
* per-cell ``groups/<cell>/<cell>.pse`` + ``.pml`` — a lightweight, protein-free
  overlay of just that cell's molecules ("one visualisation file per set"). The
  poses are already in the common reference frame, so they are directly
  comparable; keeping the protein out of the per-cell files keeps them tiny.

PyMOL (the ``viz`` pixi feature) is imported best-effort; ``.pml`` scripts are
always written so the sessions are reproducible without it.
"""

from __future__ import annotations

import logging
from pathlib import Path

from ..util.paths import (
    target_grouped_pml,
    target_grouped_pse,
    target_reference_pdb,
)
from .group import GroupResult

log = logging.getLogger("pharmpipe.groups.visualize")

# Stable, readable colours for cells (efficacy-suggestive where it helps).
_CELL_COLOURS = {
    "positive": "green",
    "negative": "salmon",
    "neutral": "yellow",
}
_FALLBACK = ["cyan", "magenta", "orange", "wheat", "slate", "purple", "teal",
             "lime", "pink", "deepblue", "olive"]


def _cell_colour(cell: str, index: int) -> str:
    sign = cell.rsplit("__", 1)[-1]
    return _CELL_COLOURS.get(sign, _FALLBACK[index % len(_FALLBACK)])


def _try_pymol():
    try:
        import pymol
        from pymol import cmd, util
    except Exception as exc:  # noqa: BLE001
        log.info("PyMOL unavailable (%s); writing .pml only", exc)
        return None
    pymol.finish_launching(["pymol", "-qc"])
    return cmd, util


# --- combined grouped session -----------------------------------------------

def write_grouped_pml(res: GroupResult, pose_folders: dict[str, list[Path]]) -> Path:
    """Portable script: load each cell's (tracked) mol2 and colour by cell."""
    lines = [
        f"# {res.slug} — Stage 3 cells overlay ({len(res.cells)} cells)",
        f"# Open from catalogue/{res.slug}/:  pymol {target_grouped_pml(res.slug).name}",
        "reinitialize", "bg_color white", "set valence, 1", "",
    ]
    for i, (cell, paths) in enumerate(sorted(pose_folders.items())):
        if cell not in res.cells:
            continue
        colour = _cell_colour(cell, i)
        for p in paths:
            obj = f"{cell}__{p.stem}"
            lines.append(f"load groups/{cell}/{p.name}, {obj}")
        lines.append(f"group {cell}, {cell}__*")
        lines.append(f"color {colour}, {cell} and elem C")
    lines += ["show sticks", "hide everything, hydro",
              "set stick_radius, 0.15", "orient", ""]
    path = target_grouped_pml(res.slug)
    path.write_text("\n".join(lines), encoding="utf-8")
    return path


def build_grouped_pse(res: GroupResult, anchor_het: str | None) -> Path | None:
    pm = _try_pymol()
    if pm is None:
        return None
    cmd, util = pm
    ref = target_reference_pdb(res.slug)
    if not ref.exists():
        log.warning("[%s] reference.pdb missing; skipping grouped .pse", res.slug)
        return None

    cmd.reinitialize()
    cmd.bg_color("white")
    cmd.set("valence", 1)
    cmd.load(str(ref), "reference")
    cmd.hide("everything", "reference")
    cmd.show("cartoon", "reference")
    cmd.color("grey80", "reference")
    if anchor_het:
        cmd.select("anchor", f"reference and resn {anchor_het}")
        cmd.show("sticks", "anchor")
        cmd.color("yellow", "anchor")

    for i, (cell, poses) in enumerate(res.cells.items()):
        colour = _cell_colour(cell, i)
        members = []
        for p in poses:
            if not p.aligned_mol2.exists():
                continue
            obj = f"{cell}__{p.aligned_mol2.stem}"
            cmd.load(str(p.aligned_mol2), obj)
            members.append(obj)
        if members:
            cmd.group(cell, " ".join(members))
            cmd.color(colour, f"{cell} and elem C")
    cmd.show("sticks", "not reference")
    cmd.hide("everything", "hydro")
    cmd.set("stick_radius", 0.15, "not reference")
    cmd.deselect()
    cmd.orient("not reference")
    out = target_grouped_pse(res.slug)
    cmd.save(str(out))
    log.info("[%s] wrote %s", res.slug, out.name)
    return out


# --- per-cell / per-set sessions --------------------------------------------

def _write_set_pml(folder: Path, paths: list[Path], colour: str | None) -> Path:
    name = folder.name
    lines = [f"# {name} — {len(paths)} molecules (reference frame; protein omitted)",
             "reinitialize", "bg_color white", "set valence, 1", ""]
    for p in paths:
        lines.append(f"load {p.name}, {p.stem}")
    lines += ["show sticks", "hide everything, hydro", "util.cbag *"
              if colour is None else f"color {colour}, elem C",
              "set stick_radius, 0.16", "orient", ""]
    out = folder / f"{name}.pml"
    out.write_text("\n".join(lines), encoding="utf-8")
    return out


def _build_set_pse(folder: Path, paths: list[Path], colour: str | None):
    pm = _try_pymol()
    if pm is None:
        return None
    cmd, util = pm
    cmd.reinitialize()
    cmd.bg_color("white")
    cmd.set("valence", 1)
    for p in paths:
        cmd.load(str(p), p.stem)
    if colour:
        cmd.color(colour, "elem C")
    else:
        util.cbag("all")
    cmd.show("sticks")
    cmd.hide("everything", "hydro")
    cmd.set("stick_radius", 0.16)
    cmd.deselect()
    cmd.orient()
    out = folder / f"{folder.name}.pse"
    cmd.save(str(out))
    return out


def build_cell_sessions(res: GroupResult, pose_folders: dict[str, list[Path]],
                        make_pse: bool = True) -> int:
    """One .pml (+ .pse) per cell and per review set. Returns count written."""
    n = 0
    for i, (name, paths) in enumerate(sorted(pose_folders.items())):
        if not paths:
            continue
        folder = paths[0].parent
        colour = _cell_colour(name, i) if name in res.cells else None
        _write_set_pml(folder, paths, colour)
        if make_pse:
            _build_set_pse(folder, paths, colour)
        n += 1
    return n


def build_sessions(res: GroupResult, pose_folders: dict[str, list[Path]],
                   anchor_het: str | None = None, make_pse: bool = True) -> dict:
    artifacts = {"grouped_pml": write_grouped_pml(res, pose_folders)}
    if make_pse:
        pse = build_grouped_pse(res, anchor_het)
        if pse is not None:
            artifacts["grouped_pse"] = pse
    artifacts["cell_sessions"] = build_cell_sessions(res, pose_folders, make_pse=make_pse)
    return artifacts
