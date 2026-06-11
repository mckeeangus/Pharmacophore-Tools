"""Per-target resolved-accession records (JSON) and the overall run summary."""

from __future__ import annotations

import json
from collections import Counter
from dataclasses import asdict
from pathlib import Path

from .build import TargetResult
from ..util.paths import ensure_dir, target_catalogue_dir


def write_resolved_json(tr: TargetResult) -> Path:
    out = ensure_dir(target_catalogue_dir(tr.slug)) / "resolved.json"
    payload = {
        "target": tr.resolved.target.name,
        "slug": tr.slug,
        "search_date": tr.resolved.search_date,
        "primary_accessions": tr.resolved.primary_accessions(),
        "surrogate_accessions": tr.resolved.surrogate_accessions(),
        "accessions": [asdict(a) for a in tr.resolved.accessions],
        "warnings": tr.resolved.warnings,
        "n_structures_found": len(tr.hits),
        "n_unique_ligands_kept": len(tr.curation.kept_het_codes()),
    }
    out.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return out


def _extract_status_counts(tr: TargetResult) -> Counter:
    c: Counter = Counter()
    for r in tr.extract_results:
        c[r.status] += 1
    return c


def build_run_summary(results: list[TargetResult], search_date: str) -> str:
    lines = [f"# Run summary — {search_date}", ""]
    g_struct = g_kept = g_excl = g_flag = g_mol2 = g_fail = 0
    g_status: Counter = Counter()
    lines.append("| Target | Acc (primary) | Structs | Uniq kept | Excl | "
                 "Flagged | mol2 | Fallback | Failed |")
    lines.append("|--------|---------------|--------:|----------:|-----:|"
                 "--------:|-----:|---------:|-------:|")
    for tr in results:
        sc = _extract_status_counts(tr)
        n_mol2 = sum(1 for r in tr.extract_results if r.ok)
        n_fail = sc.get("failed", 0)
        n_fallback = sc.get("openbabel_fallback", 0)
        prim = ",".join(tr.resolved.primary_accessions()) or "—"
        lines.append(
            f"| {tr.resolved.target.name[:34]} | {prim} | {len(tr.hits)} | "
            f"{len(tr.curation.kept_het_codes())} | "
            f"{len(tr.curation.excluded_het_codes())} | "
            f"{len(tr.curation.flagged_het_codes())} | {n_mol2} | "
            f"{n_fallback} | {n_fail} |")
        g_struct += len(tr.hits)
        g_kept += len(tr.curation.kept_het_codes())
        g_excl += len(tr.curation.excluded_het_codes())
        g_flag += len(tr.curation.flagged_het_codes())
        g_mol2 += n_mol2
        g_fail += n_fail
        g_status += sc
    lines.append(f"| **TOTAL** | | {g_struct} | {g_kept} | {g_excl} | {g_flag} "
                 f"| {g_mol2} | {g_status.get('openbabel_fallback', 0)} | {g_fail} |")
    lines.append("")
    lines.append("Bond-order assignment breakdown (mol2): "
                 + ", ".join(f"{k}={v}" for k, v in sorted(g_status.items())))
    lines.append("")
    warned = [tr for tr in results if tr.resolved.warnings]
    if warned:
        lines.append("## Warnings")
        for tr in warned:
            lines.append(f"- **{tr.resolved.target.name}**")
            lines.extend(f"    - {w}" for w in tr.resolved.warnings)
    failures = [(tr.slug, r) for tr in results for r in tr.extract_results
                if not r.ok]
    if failures:
        lines.append("")
        lines.append("## Extraction failures")
        for slug, r in failures[:200]:
            lines.append(f"- {slug}: {r.instance.pdb_id} {r.instance.comp_id} "
                         f"{r.instance.auth_asym_id}{r.instance.auth_seq_id} — {r.message}")
    return "\n".join(lines)


def write_run_summary(results: list[TargetResult], out_path: Path,
                      search_date: str) -> Path:
    ensure_dir(out_path.parent)
    text = build_run_summary(results, search_date)
    out_path.write_text(text, encoding="utf-8")
    return out_path
