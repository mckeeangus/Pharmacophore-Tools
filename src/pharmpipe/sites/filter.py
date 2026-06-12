"""Per-target orchestration: keep only ligands bound at the relevant site and
write their poses, superposed into the reference frame, as mol2.

Reuses the cached catalogue metadata (TargetResult) for the list of curated
ligand instances, downloads every structure that holds one, aligns each instance
to the site reference, and writes the kept poses (transformed into the reference
frame) plus an auditable ``site_filter.csv``.
"""

from __future__ import annotations

import logging
from collections import Counter, defaultdict
from dataclasses import dataclass, field
from pathlib import Path

import pandas as pd

from ..catalogue.build import TargetResult
from ..io import mol2, structures
from ..util import http
from ..util.paths import (
    ensure_dir,
    target_aligned_mol2_dir,
    target_catalogue_dir,
    target_reference_pdb,
)
from . import align
from .align import AlignedInstance, SiteReference
from .config import SiteDef

log = logging.getLogger("pharmpipe.sites.filter")


@dataclass
class AlignTargetResult:
    slug: str
    site: SiteDef
    reference: SiteReference | None
    rows: list[dict] = field(default_factory=list)
    aligned_files: list[Path] = field(default_factory=list)
    status_counts: Counter = field(default_factory=Counter)
    structures_total: int = 0
    structures_processed: int = 0
    capped: bool = False

    @property
    def n_candidates(self) -> int:
        return len(self.rows)

    @property
    def n_kept(self) -> int:
        # Distinct poses written to the overlay (symmetry-deduplicated representatives).
        return len(self.aligned_files)

    @property
    def n_at_site(self) -> int:
        # All instances at the site, including symmetry mates.
        return self.status_counts.get("kept", 0) + self.status_counts.get("symmetry_dup", 0)


def _kept_instances_by_pdb(tr: TargetResult) -> dict[str, list]:
    # Overlay organic ligands/cofactors only. Single metal ions are kept+flagged by
    # curation but are not comparable pharmacophore poses — and when the anchor is a
    # catalytic metal (e.g. Zn in carbonic anhydrase) they would otherwise flood the
    # cap with identical ions. They still mark the site via the reference anchor.
    keep = {c for c, d in tr.curation.decisions.items() if d.keep and d.category != "metal"}
    by_pdb: dict[str, list] = defaultdict(list)
    for hit in tr.hits:
        for inst in hit.instances:
            if inst.comp_id.upper() in keep:
                by_pdb[hit.pdb_id].append(inst)
    return by_pdb


def _resolution_of(tr: TargetResult) -> dict[str, float]:
    return {h.pdb_id: (h.resolution if h.resolution is not None else 1e9) for h in tr.hits}


def align_target(tr: TargetResult, site: SiteDef, cfg: http.HttpConfig,
                 max_ligands: int | None = 100, max_structures: int | None = None,
                 progress=None) -> AlignTargetResult:
    """Align kept instances into the reference frame, keeping one representative
    pose per (structure, ligand) — symmetry-equivalent copies in a structure are
    collapsed — and stopping once ``max_ligands`` distinct poses are collected.
    Structures are processed best-resolution first so the cap keeps the best data.
    """
    slug = tr.slug
    out = AlignTargetResult(slug=slug, site=site, reference=None)

    # --- reference setup ---
    ref_path = structures.download_mmcif(site.reference_pdb, slug, cfg)
    if ref_path is None:
        log.error("[%s] reference %s could not be downloaded", slug, site.reference_pdb)
        return out
    ref_st = structures.read_structure(ref_path)
    reference = align.build_reference(ref_st, site)
    out.reference = reference
    if reference is None:
        log.error("[%s] could not build site reference from %s", slug, site.reference_pdb)
        return out
    # Persist the reference protein as the overlay scaffold for the session.
    ref_pdb_path = target_reference_pdb(slug)
    ensure_dir(ref_pdb_path.parent)
    ref_st.write_pdb(str(ref_pdb_path))

    aligned_dir = ensure_dir(target_aligned_mol2_dir(slug))
    # Start clean so a re-run with a different cap does not leave stale poses.
    for old in aligned_dir.glob("*.mol2"):
        old.unlink()
    smiles = {c: cc.smiles for c, cc in tr.chem_comps.items()}

    by_pdb = _kept_instances_by_pdb(tr)
    res_of = _resolution_of(tr)
    pdb_ids = sorted(by_pdb, key=lambda p: (res_of.get(p, 1e9), p))
    if max_structures is not None:
        pdb_ids = pdb_ids[:max_structures]
    out.structures_total = len(by_pdb)

    for pdb_id in pdb_ids:
        if max_ligands is not None and len(out.aligned_files) >= max_ligands:
            out.capped = True
            break
        out.structures_processed += 1

        path = structures.download_mmcif(pdb_id, slug, cfg)
        if path is None:
            for inst in by_pdb[pdb_id]:
                out.rows.append(_row(inst, AlignedInstance(inst, "not_found",
                                                           message="mmCIF unavailable")))
            if progress is not None:
                progress.update(1)
            continue
        try:
            st = structures.read_structure(path)
        except Exception as exc:  # noqa: BLE001
            for inst in by_pdb[pdb_id]:
                out.rows.append(_row(inst, AlignedInstance(inst, "align_error",
                                                           message=f"parse error: {exc}")))
            if progress is not None:
                progress.update(1)
            continue

        # Align every candidate; group the at-site ones by ligand for symmetry dedup.
        aligned: list[tuple] = []                       # (AlignedInstance, inst)
        kept_by_comp: dict[str, tuple] = {}             # comp_id -> best (AlignedInstance, inst)
        for inst in by_pdb[pdb_id]:
            a = align.align_instance(st, inst, reference)
            aligned.append((a, inst))
            if a.kept:
                c = inst.comp_id.upper()
                best = kept_by_comp.get(c)
                if best is None or (a.pocket_rmsd or 1e9) < (best[0].pocket_rmsd or 1e9):
                    kept_by_comp[c] = (a, inst)

        # Write one representative pose per ligand; mark symmetry mates.
        model = st[0]
        written: dict[str, str] = {}
        for a, inst in kept_by_comp.values():
            res = align.find_residue(model, inst)
            if res is None:
                continue
            align.transform_residue(res, a.transform)
            er = mol2.extract_instance(st, inst, aligned_dir, cfg,
                                       smiles.get(inst.comp_id.upper(), ""))
            if er.ok and er.out_path is not None:
                out.aligned_files.append(er.out_path)
                written[inst.comp_id.upper()] = er.out_path.name
            else:
                a.message = f"mol2 write failed: {er.message}"

        for a, inst in aligned:
            is_rep = (a.kept and kept_by_comp.get(inst.comp_id.upper(), (None,))[0] is a)
            status = a.status
            mol2_name = ""
            if a.kept and not is_rep:
                status = "symmetry_dup"          # at the site but a symmetry mate of the rep
            elif is_rep:
                mol2_name = written.get(inst.comp_id.upper(), "")
            out.rows.append(_row(inst, a, mol2_name, representative=is_rep, status=status))

        if progress is not None:
            progress.update(1)

    out.status_counts = Counter(r["status"] for r in out.rows)
    _write_csv(out)
    return out


def _row(inst, a: AlignedInstance, mol2_name: str = "", representative: bool = False,
         status: str | None = None) -> dict:
    return {
        "pdb_id": inst.pdb_id,
        "het_code": inst.comp_id,
        "chain": inst.auth_asym_id,
        "seqid": inst.auth_seq_id,
        "status": status or a.status,
        "representative": representative,
        "centroid_distance": None if a.centroid_distance is None else round(a.centroid_distance, 2),
        "pocket_rmsd": None if a.pocket_rmsd is None else round(a.pocket_rmsd, 2),
        "n_pocket": a.n_pocket,
        "aligned_mol2": mol2_name,
        "message": a.message,
    }


def _write_csv(out: AlignTargetResult) -> Path:
    cols = ["pdb_id", "het_code", "chain", "seqid", "status", "representative",
            "centroid_distance", "pocket_rmsd", "n_pocket", "aligned_mol2", "message"]
    df = pd.DataFrame(out.rows, columns=cols)
    df = df.sort_values(["status", "het_code", "pdb_id"], kind="stable")
    path = ensure_dir(target_catalogue_dir(out.slug)) / "site_filter.csv"
    df.to_csv(path, index=False)
    return path
