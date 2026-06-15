"""Stage 3 outputs: cell mol2 folders, effect_groups.json, the per-target
report, and the three-stage run summary.

Everything written here is tracked under ``catalogue/<slug>/``. The pose mol2 are
copied (not symlinked) so a cell folder is a self-contained, portable input for
downstream clustering.
"""

from __future__ import annotations

import json
import re
import shutil
from collections import Counter
from pathlib import Path

from ..util.paths import (
    CATALOGUE_DIR,
    ensure_dir,
    target_effect_groups_json,
    target_groups_dir,
    target_review_dir,
    target_stage3_report,
)
from .group import GroupResult, Pose, status_counts

_SAFE = re.compile(r"[^A-Za-z0-9_.-]+")


def _safe(name: str) -> str:
    return _SAFE.sub("-", name)


def _residue_names(fingerprint: frozenset[str]) -> Counter:
    """Multiset of residue *names* (numbers stripped) — numbering-robust."""
    return Counter(re.sub(r"\d+$", "", r) for r in fingerprint)


def candidate_pocket(pose: Pose, res: GroupResult) -> str | None:
    """Best-guess pocket for a quarantined pose by residue-*name* overlap.

    Quarantine is usually a real outlier, but a deposition with non-standard
    residue numbering can orphan an otherwise-valid pose (zero number overlap yet
    matching residue composition). We surface a hint without reclassifying it.
    """
    names = _residue_names(pose.fingerprint)
    if not names:
        return None
    best, best_score = None, 0.0
    for cluster in res.clusters:
        if not cluster.label or cluster.status != "assigned":
            continue
        cons = _residue_names(frozenset(cluster.consensus_residues))
        shared = sum((names & cons).values())
        score = shared / max(1, sum(names.values()))
        if score > best_score:
            best, best_score = cluster.label, score
    return best if best_score >= 0.5 else None


# --- mol2 cell folders -------------------------------------------------------

def write_pose_folders(res: GroupResult) -> dict[str, list[Path]]:
    """Copy each pose's aligned mol2 into its cell / review folder.

    Returns ``{group_name: [mol2 paths]}`` for the session writer. ``groups/``
    and ``review/`` are cleared first so re-runs don't leave stale poses.
    """
    groups_dir = target_groups_dir(res.slug)
    review_dir = target_review_dir(res.slug)
    for d in (groups_dir, review_dir):
        if d.exists():
            shutil.rmtree(d)

    out: dict[str, list[Path]] = {}

    def place(name: str, base: Path, poses: list[Pose]) -> None:
        if not poses:
            return
        dest_dir = ensure_dir(base / _safe(name))
        paths = []
        for p in poses:
            if p.aligned_mol2.exists():
                dest = dest_dir / p.aligned_mol2.name
                shutil.copy2(p.aligned_mol2, dest)
                paths.append(dest)
        out[name] = paths

    for cell, poses in res.cells.items():
        place(cell, groups_dir, poses)
    place("separate_state", review_dir, res.separate_state)
    place("unknown", review_dir, res.unknown)
    place("quarantine", review_dir, res.quarantined)
    return out


# --- effect_groups.json ------------------------------------------------------

def _efficacy_label(eff) -> str:
    if eff is None:
        return "unknown"
    return "n/a" if eff.is_separate_state else eff.efficacy


def _pose_record(p: Pose) -> dict:
    eff = p.efficacy
    return {
        "pdb_id": p.pdb_id,
        "ligand_id": p.het_code,
        "chain": p.chain,
        "seqid": p.seqid,
        "pocket": p.pocket,
        "efficacy": _efficacy_label(eff),
        "track": eff.track if eff else "reversible",
        "cell": p.cell,
        "efficacy_source": eff.source if eff else "",
        "efficacy_note": eff.note if eff else "",
        "separate_state_reason": eff.reason if eff else "",
        "mapping": p.mapping,
        "subtype_accessions": p.accessions,
        "subtype_organisms": p.organisms,
        "mol2": p.aligned_mol2.name,
    }


def write_effect_groups_json(res: GroupResult) -> Path:
    payload = {
        "slug": res.slug,
        "primary_pocket": res.pdef.primary_label,
        "expected_pockets": res.expected_pockets,
        "pockets_found": res.pockets_found,
        "cells": {cell: [p.label for p in poses] for cell, poses in res.cells.items()},
        "counts": dict(status_counts(res)),
        "poses": [_pose_record(p) for p in res.poses],
    }
    path = target_effect_groups_json(res.slug)
    ensure_dir(path.parent)
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return path


# --- per-target markdown report ---------------------------------------------

def _cell_table(res: GroupResult) -> list[str]:
    lines = ["| Cell (pocket × efficacy) | Poses | Distinct ligands | Example HETs |",
             "|---|--:|--:|---|"]
    for cell, poses in res.cells.items():
        hets = sorted({p.het_code for p in poses})
        lines.append(f"| `{cell}` | {len(poses)} | {len(hets)} | "
                     f"{', '.join(hets[:6])}{' …' if len(hets) > 6 else ''} |")
    if not res.cells:
        lines.append("| _none_ | | | |")
    return lines


def _pockets_section(res: GroupResult) -> list[str]:
    expected = set(res.expected_pockets)
    found = set(res.pockets_found)
    status = "as expected" if found == expected or not expected else "**DEPARTS from expectation**"
    lines = [f"**Pockets found:** {', '.join(res.pockets_found) or '—'} "
             f"(expected: {', '.join(res.expected_pockets) or '—'}) — {status}", ""]
    lines += ["| Cluster | Label | Poses | Status | Consensus residues (sample) |",
              "|--:|---|--:|---|---|"]
    for c in sorted(res.clusters, key=lambda x: x.cluster_id):
        flag = " ⚠ review" if c.review else ""
        cons = ", ".join(sorted(c.consensus_residues)[:8])
        lines.append(f"| {c.cluster_id} | {c.label or '_quarantined_'}{flag} | "
                     f"{len(c.pose_indices)} | {c.status} | {cons} |")
    return lines


def _review_section(title: str, poses: list[Pose], reason_attr: str | None,
                    res: GroupResult | None = None) -> list[str]:
    if not poses:
        return [f"**{title}:** none.", ""]
    lines = [f"**{title}** ({len(poses)}):", ""]
    for p in sorted(poses, key=lambda x: (x.het_code, x.pdb_id)):
        extra = ""
        if reason_attr and p.efficacy:
            extra = f" — {getattr(p.efficacy, reason_attr)}"
        elif res is not None:
            hint = candidate_pocket(p, res)
            extra = f" — candidate pocket: {hint}" if hint else " — no pocket match"
        lines.append(f"- `{p.het_code}` ({p.label}, {p.mapping}){extra}")
    lines.append("")
    return lines


def write_stage3_report(res: GroupResult, search_date: str) -> Path:
    sc = status_counts(res)
    lines = [
        f"# Stage 3 — effect groups: {res.slug}",
        "",
        f"_Generated {search_date}. Cell = (verified pocket) × (efficacy sign)._",
        "",
        f"- Poses carried from Stage 2: **{sc['poses']}**",
        f"- In partition cells: **{sc['in_cells']}** across **{sc['cells']}** cells",
        f"- Routed to separate-state track: **{sc['separate_state']}**",
        f"- Efficacy unknown (review): **{sc['unknown']}**",
        f"- Quarantined (not in pocket of interest): **{sc['quarantined']}**",
        "",
        "## Pocket verification",
        "",
        *(_pockets_section(res)),
        "",
        f"_Notes: {res.pdef.notes}_" if res.pdef.notes else "",
        "",
        "## Partition cells",
        "",
        *(_cell_table(res)),
        "",
        "## Separate-state ligands (routed out of cells)",
        "",
        *(_review_section("Separate-state", res.separate_state, "reason")),
        "## Efficacy review list",
        "",
        *(_review_section("Unknown efficacy", res.unknown, None)),
        "## Quarantined poses",
        "",
        *(_review_section("Quarantined", res.quarantined, None, res=res)),
        "---",
        "",
        "Cell mol2 sets: `groups/<pocket>__<efficacy>/`. Review sets: "
        "`review/{separate_state,unknown,quarantine}/`. Sessions: "
        f"`{res.slug}_grouped.pse` (all cells) and per-cell `.pse` in each folder.",
        "",
    ]
    path = target_stage3_report(res.slug)
    ensure_dir(path.parent)
    path.write_text("\n".join(line for line in lines), encoding="utf-8")
    return path


# --- three-stage run summary -------------------------------------------------

_STAGE3_HEADER = "## Stage 3 — effect-based grouping (pocket-verified)"


def update_run_summary(results: list[GroupResult], search_date: str) -> Path:
    """Append/replace the Stage 3 section in the shared run_summary.md.

    Stage 1/2 own the top of the file; we only manage our own trailing section so
    re-running Stage 3 alone does not clobber the earlier stages.
    """
    path = ensure_dir(CATALOGUE_DIR) / "run_summary.md"
    existing = path.read_text(encoding="utf-8") if path.exists() else ""
    head = existing.split(_STAGE3_HEADER, 1)[0].rstrip() if existing else ""

    lines = [
        head,
        "",
        _STAGE3_HEADER,
        "",
        f"_Stage 3 run {search_date}._ Each pose is assigned a **geometry-verified "
        "pocket** (native contact fingerprints, not the coarse Stage-2 distance) "
        "and an **efficacy sign** from curated external pharmacology "
        "(`config/efficacy.yaml`). A cell = (pocket × efficacy). Covalent/"
        "reactivator/degrader/substrate ligands are routed to a separate-state "
        "track; unconfident efficacy and out-of-pocket poses are first-class "
        "review outputs, never force-bucketed.",
        "",
        "| Target | Pockets found | Cells | In cells | Separate-state | Unknown eff. | Quarantined |",  # noqa: E501
        "|--------|---------------|------:|---------:|---------------:|-------------:|------------:|",  # noqa: E501
    ]
    for res in results:
        sc = status_counts(res)
        lines.append(
            f"| {res.slug} | {', '.join(res.pockets_found) or '—'} | {sc['cells']} | "
            f"{sc['in_cells']} | {sc['separate_state']} | {sc['unknown']} | "
            f"{sc['quarantined']} |")
    lines += [
        "",
        "Per-target detail: `catalogue/<slug>/<slug>_stage3_report.md`, the cell "
        "mol2 in `catalogue/<slug>/groups/`, `effect_groups.json`, and the "
        "recoloured session `catalogue/<slug>/<slug>_grouped.pse`.",
        "",
    ]
    path.write_text("\n".join(lines), encoding="utf-8")
    return path
