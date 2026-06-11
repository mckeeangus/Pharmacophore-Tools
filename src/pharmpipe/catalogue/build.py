"""Build the catalogue deliverable: per-target CSVs, a combined markdown
summary, and an optional xlsx workbook.

Two tables per target:
  * unique-ligand table  — HET code, name, SMILES, category, #structures,
    representative PDB ID (best resolution).
  * per-structure table  — PDB ID -> kept ligand(s), with resolution/method and
    whether the structure maps to the primary target or a surrogate.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

import pandas as pd

from ..io.mol2 import ExtractResult
from ..pdb.ligands import CurationResult
from ..pdb.rcsb import ChemComp, StructureHit
from ..pdb.uniprot import ResolvedTarget
from ..util.paths import ensure_dir, target_catalogue_dir


@dataclass
class TargetResult:
    resolved: ResolvedTarget
    hits: list[StructureHit]
    curation: CurationResult
    chem_comps: dict[str, ChemComp] = field(default_factory=dict)
    extract_results: list[ExtractResult] = field(default_factory=list)

    @property
    def slug(self) -> str:
        return self.resolved.target.slug

    def mapping_for(self, hit: StructureHit) -> str:
        primary = set(self.resolved.primary_accessions())
        surrogate = set(self.resolved.surrogate_accessions())
        accs = set(hit.uniprot_accessions)
        if accs & primary:
            return "primary"
        if accs & surrogate:
            return "surrogate"
        return "unknown"

    def representative_pdb(self, comp_id: str) -> str:
        pdbs = self.curation.structure_counts.get(comp_id, set())
        best, best_res = "", float("inf")
        for hit in self.hits:
            if hit.pdb_id in pdbs:
                res = hit.resolution if hit.resolution is not None else float("inf")
                if res < best_res or (best == ""):
                    best, best_res = hit.pdb_id, res
        return best


def unique_ligand_frame(tr: TargetResult) -> pd.DataFrame:
    rows = []
    for comp_id in tr.curation.kept_het_codes():
        d = tr.curation.decisions[comp_id]
        cc = tr.chem_comps.get(comp_id, ChemComp(comp_id))
        rows.append({
            "het_code": comp_id,
            "name": cc.name,
            "category": d.category,
            "flagged": d.flagged,
            "n_structures": tr.curation.n_structures_for(comp_id),
            "n_instances": tr.curation.instance_counts.get(comp_id, 0),
            "representative_pdb": tr.representative_pdb(comp_id),
            "formula_weight": cc.formula_weight,
            "smiles": cc.smiles,
        })
    rows.sort(key=lambda r: (-r["n_structures"], r["het_code"]))
    return pd.DataFrame(rows, columns=[
        "het_code", "name", "category", "flagged", "n_structures", "n_instances",
        "representative_pdb", "formula_weight", "smiles"])


def per_structure_frame(tr: TargetResult) -> pd.DataFrame:
    rows = []
    for hit in sorted(tr.hits, key=lambda h: h.pdb_id):
        kept, excluded = [], []
        for cid in hit.het_codes:
            d = tr.curation.decisions.get(cid.upper())
            if d is None:
                continue
            (kept if d.keep else excluded).append(cid)
        rows.append({
            "pdb_id": hit.pdb_id,
            "resolution": hit.resolution,
            "method": hit.method,
            "mapping": tr.mapping_for(hit),
            "uniprot_accessions": ";".join(hit.uniprot_accessions),
            "kept_ligands": ";".join(sorted(kept)),
            "excluded_ligands": ";".join(sorted(excluded)),
        })
    return pd.DataFrame(rows, columns=[
        "pdb_id", "resolution", "method", "mapping", "uniprot_accessions",
        "kept_ligands", "excluded_ligands"])


def write_target_csvs(tr: TargetResult) -> dict[str, Path]:
    out = ensure_dir(target_catalogue_dir(tr.slug))
    paths = {}
    uniq = out / "unique_ligands.csv"
    perstruct = out / "per_structure.csv"
    unique_ligand_frame(tr).to_csv(uniq, index=False)
    per_structure_frame(tr).to_csv(perstruct, index=False)
    paths["unique_ligands"] = uniq
    paths["per_structure"] = perstruct
    return paths


# --- markdown ------------------------------------------------------------

def target_markdown_section(tr: TargetResult) -> str:
    t = tr.resolved.target
    lines: list[str] = [f"## {t.name}", ""]
    lines.append(f"- **Slug:** `{t.slug}`")
    prim = ", ".join(tr.resolved.primary_accessions()) or "—"
    sur = ", ".join(tr.resolved.surrogate_accessions()) or "—"
    lines.append(f"- **Primary UniProt:** {prim}")
    if tr.resolved.surrogate_accessions():
        lines.append(f"- **Surrogate UniProt (gap-filler, labelled):** {sur}")
    lines.append(f"- **Search date:** {tr.resolved.search_date}")
    lines.append(f"- **Structures (ligand-bound / total found):** "
                 f"{sum(1 for h in tr.hits if any(tr.curation.decisions.get(c.upper(), None) and tr.curation.decisions[c.upper()].keep for c in h.het_codes))}"
                 f" / {len(tr.hits)}")
    n_mol2 = sum(1 for r in tr.extract_results if r.ok)
    lines.append(f"- **Unique ligands kept:** {len(tr.curation.kept_het_codes())} "
                 f"| **excluded HET types:** {len(tr.curation.excluded_het_codes())} "
                 f"| **flagged (review):** {len(tr.curation.flagged_het_codes())}")
    lines.append(f"- **mol2 bound poses written:** {n_mol2}")
    if t.notes:
        lines.append(f"- **Notes:** {t.notes}")
    if tr.resolved.warnings:
        lines.append("- **Warnings:**")
        lines.extend(f"    - {w}" for w in tr.resolved.warnings)
    lines.append("")

    df = unique_ligand_frame(tr)
    flagged = tr.curation.flagged_het_codes()
    if flagged:
        lines.append(f"**Flagged for review (kept):** {', '.join(flagged)}")
        lines.append("")
    lines.append("### Unique ligands")
    lines.append("")
    if df.empty:
        lines.append("_No ligands kept after curation._")
    else:
        head = df.head(40)
        lines.append("| HET | Name | Cat | #Struct | Rep PDB | SMILES |")
        lines.append("|-----|------|-----|--------:|---------|--------|")
        for _, r in head.iterrows():
            name = (r["name"] or "")[:40]
            smi = (r["smiles"] or "")[:48]
            lines.append(f"| {r['het_code']} | {name} | {r['category']} | "
                         f"{r['n_structures']} | {r['representative_pdb']} | `{smi}` |")
        if len(df) > 40:
            lines.append(f"| … | _{len(df) - 40} more — see "
                         f"`catalogue/{tr.slug}/unique_ligands.csv`_ | | | | |")
    excluded = tr.curation.excluded_het_codes()
    if excluded:
        lines.append("")
        lines.append(f"**Excluded as additives/buffers/solvents "
                     f"({len(excluded)} types):** {', '.join(excluded)}")
    lines.append("")
    return "\n".join(lines)


def write_combined_markdown(results: list[TargetResult], out_path: Path,
                            search_date: str) -> Path:
    parts = [
        "# Ligand catalogue",
        "",
        f"Generated by `pharmpipe` scrape on **{search_date}**. "
        "One section per target. Machine-readable tables live under "
        "`catalogue/<slug>/`.",
        "",
        "Curation policy: crystallographic additives/buffers/cryoprotectants/"
        "waters are excluded; genuine cofactors (heme, FAD, NAD, ...) are kept; "
        "single metal ions are kept **and flagged** for review (they may be "
        "catalytic cofactors, e.g. Zn²⁺ in carbonic anhydrase, Ca²⁺ in CavAb).",
        "",
        "---",
        "",
    ]
    for tr in results:
        parts.append(target_markdown_section(tr))
        parts.append("---")
        parts.append("")
    ensure_dir(out_path.parent)
    out_path.write_text("\n".join(parts), encoding="utf-8")
    return out_path


def write_xlsx(results: list[TargetResult], out_path: Path) -> Path | None:
    try:
        with pd.ExcelWriter(out_path, engine="openpyxl") as xl:
            for tr in results:
                sheet = tr.slug[:31]
                unique_ligand_frame(tr).to_excel(xl, sheet_name=sheet, index=False)
    except Exception:  # noqa: BLE001
        return None
    return out_path
