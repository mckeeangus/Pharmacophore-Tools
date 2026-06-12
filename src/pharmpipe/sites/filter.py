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

    @property
    def n_candidates(self) -> int:
        return len(self.rows)

    @property
    def n_kept(self) -> int:
        return self.status_counts.get("kept", 0)


def _kept_instances_by_pdb(tr: TargetResult) -> dict[str, list]:
    keep = {c for c, d in tr.curation.decisions.items() if d.keep}
    by_pdb: dict[str, list] = defaultdict(list)
    for hit in tr.hits:
        for inst in hit.instances:
            if inst.comp_id.upper() in keep:
                by_pdb[hit.pdb_id].append(inst)
    return by_pdb


def _resolution_of(tr: TargetResult) -> dict[str, float]:
    return {h.pdb_id: (h.resolution if h.resolution is not None else 1e9) for h in tr.hits}


def align_target(tr: TargetResult, site: SiteDef, cfg: http.HttpConfig,
                 max_structures: int | None = None, progress=None) -> AlignTargetResult:
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
    smiles = {c: cc.smiles for c, cc in tr.chem_comps.items()}

    by_pdb = _kept_instances_by_pdb(tr)
    pdb_ids = sorted(by_pdb)
    if max_structures is not None and len(pdb_ids) > max_structures:
        res = _resolution_of(tr)
        pdb_ids = sorted(pdb_ids, key=lambda p: res.get(p, 1e9))[:max_structures]

    for pdb_id in pdb_ids:
        path = structures.download_mmcif(pdb_id, slug, cfg)
        if path is None:
            for inst in by_pdb[pdb_id]:
                out.rows.append(_row(inst, AlignedInstance(inst, "not_found",
                                                           message="mmCIF unavailable")))
                out.status_counts["not_found"] += 1
            if progress is not None:
                progress.update(1)
            continue
        try:
            st = structures.read_structure(path)
        except Exception as exc:  # noqa: BLE001
            for inst in by_pdb[pdb_id]:
                out.rows.append(_row(inst, AlignedInstance(inst, "align_error",
                                                           message=f"parse error: {exc}")))
                out.status_counts["align_error"] += 1
            if progress is not None:
                progress.update(1)
            continue

        model = st[0]
        for inst in by_pdb[pdb_id]:
            res_align = align.align_instance(st, inst, reference)
            mol2_name = ""
            if res_align.kept:
                res = align.find_residue(model, inst)
                if res is not None:
                    align.transform_residue(res, res_align.transform)
                    er = mol2.extract_instance(st, inst, aligned_dir, cfg,
                                               smiles.get(inst.comp_id.upper(), ""))
                    if er.ok and er.out_path is not None:
                        mol2_name = er.out_path.name
                        out.aligned_files.append(er.out_path)
                    else:
                        # Alignment succeeded; only the mol2 write failed. Keep the
                        # true alignment status, flag the write problem separately.
                        res_align.message = f"mol2 write failed: {er.message}"
            out.rows.append(_row(inst, res_align, mol2_name))
            out.status_counts[res_align.status] += 1
        if progress is not None:
            progress.update(1)

    _write_csv(out)
    return out


def _row(inst, a: AlignedInstance, mol2_name: str = "") -> dict:
    return {
        "pdb_id": inst.pdb_id,
        "het_code": inst.comp_id,
        "chain": inst.auth_asym_id,
        "seqid": inst.auth_seq_id,
        "status": a.status,
        "centroid_distance": None if a.centroid_distance is None else round(a.centroid_distance, 2),
        "pocket_rmsd": None if a.pocket_rmsd is None else round(a.pocket_rmsd, 2),
        "n_pocket": a.n_pocket,
        "aligned_mol2": mol2_name,
        "message": a.message,
    }


def _write_csv(out: AlignTargetResult) -> Path:
    cols = ["pdb_id", "het_code", "chain", "seqid", "status", "centroid_distance",
            "pocket_rmsd", "n_pocket", "aligned_mol2", "message"]
    df = pd.DataFrame(out.rows, columns=cols)
    df = df.sort_values(["status", "het_code", "pdb_id"], kind="stable")
    path = ensure_dir(target_catalogue_dir(out.slug)) / "site_filter.csv"
    df.to_csv(path, index=False)
    return path
