"""End-to-end orchestration for one target and a whole run.

Catalogue tables are built purely from cached RCSB API metadata (cheap); mol2
bound-pose extraction downloads mmCIF per structure (heavy) and is governed by
``extract_mode`` plus an optional structure cap.
"""

from __future__ import annotations

import logging
from collections import defaultdict

from .catalogue.build import TargetResult
from .config import SearchOptions, Target
from .io import mol2, structures
from .pdb import ligands, rcsb, uniprot
from .pdb.rcsb import LigandInstance
from .util import http
from .util.paths import target_mol2_dir

log = logging.getLogger("pharmpipe.pipeline")


def _accessions_to_search(resolved: uniprot.ResolvedTarget,
                          opts: SearchOptions) -> list[str]:
    accs = list(resolved.primary_accessions())
    if opts.include_surrogates:
        accs += resolved.surrogate_accessions()
    return accs


def search_and_curate(target: Target, opts: SearchOptions,
                      cfg: http.HttpConfig) -> TargetResult:
    resolved = uniprot.resolve_target(target, opts)

    pdb_ids: set[str] = set()
    for acc in _accessions_to_search(resolved, opts):
        ids = rcsb.search_entries_by_accession(acc, cfg)
        log.info("[%s] %s -> %d entries", target.slug, acc, len(ids))
        pdb_ids.update(ids)

    meta = rcsb.fetch_structure_metadata(sorted(pdb_ids), cfg)
    hits = list(meta.values())

    curation = ligands.curate_structures(hits, target.keep_extra, target.exclude_extra)

    chem_comps = {c: rcsb.get_chem_comp(c, cfg) for c in curation.kept_het_codes()}

    return TargetResult(resolved=resolved, hits=hits, curation=curation,
                        chem_comps=chem_comps, extract_results=[])


def _instances_to_extract(tr: TargetResult, opts: SearchOptions,
                          max_structures: int | None) -> dict[str, list[LigandInstance]]:
    """Map pdb_id -> kept instances to extract, honouring extract_mode/cap."""
    kept_by_pdb: dict[str, list[LigandInstance]] = defaultdict(list)

    if opts.extract_mode == "representative":
        for comp_id in tr.curation.kept_het_codes():
            rep = tr.representative_pdb(comp_id)
            for hit in tr.hits:
                if hit.pdb_id != rep:
                    continue
                for inst in hit.instances:
                    if inst.comp_id.upper() == comp_id:
                        kept_by_pdb[rep].append(inst)
                        break
                break
        return kept_by_pdb

    # all_instances
    keep = {c for c, d in tr.curation.decisions.items() if d.keep}
    for hit in tr.hits:
        for inst in hit.instances:
            if inst.comp_id.upper() in keep:
                kept_by_pdb[hit.pdb_id].append(inst)

    if max_structures is not None and len(kept_by_pdb) > max_structures:
        # Prefer best-resolution structures when capping.
        res_of = {h.pdb_id: (h.resolution if h.resolution is not None else 1e9)
                  for h in tr.hits}
        chosen = sorted(kept_by_pdb, key=lambda p: res_of.get(p, 1e9))[:max_structures]
        kept_by_pdb = {p: kept_by_pdb[p] for p in chosen}
    return kept_by_pdb


def extract_mol2(tr: TargetResult, opts: SearchOptions, cfg: http.HttpConfig,
                 max_structures: int | None = None,
                 progress=None) -> None:
    out_dir = target_mol2_dir(tr.slug)
    smiles = {c: cc.smiles for c, cc in tr.chem_comps.items()}
    plan = _instances_to_extract(tr, opts, max_structures)
    for pdb_id in sorted(plan):
        path = structures.download_mmcif(pdb_id, tr.slug, cfg)
        if path is None:
            for inst in plan[pdb_id]:
                tr.extract_results.append(
                    mol2.ExtractResult(inst, None, "failed", "mmCIF unavailable"))
            if progress:
                progress.update(1)
            continue
        try:
            st = structures.read_structure(path)
        except Exception as exc:  # noqa: BLE001
            for inst in plan[pdb_id]:
                tr.extract_results.append(
                    mol2.ExtractResult(inst, None, "failed", f"parse error: {exc}"))
            if progress:
                progress.update(1)
            continue
        for inst in plan[pdb_id]:
            r = mol2.extract_instance(st, inst, out_dir, cfg,
                                      smiles.get(inst.comp_id.upper(), ""))
            tr.extract_results.append(r)
        if progress is not None:
            progress.update(1)
