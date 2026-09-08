#!/usr/bin/env python
"""Build a hand-off worklist for literature-based efficacy curation.

OFFLINE. The agonist/antagonist *direction* of the research-grade ligands left
`unknown` by the ChEMBL pass almost always lives in each structure's primary
publication, not in a structured database. This script gathers, for every
still-`unknown` ligand, the facts a curator (or a separate Claude chat session
with PubMed access) needs to look it up: the representative PDB, its primary-
citation PubMed id / DOI / title (read from the cached mmCIF), whether ChEMBL has
binding data, and the ligand's chemical name.

Reads `catalogue/stage3_efficacy_resolved.csv`; writes
`catalogue/literature_worklist.csv`. The curated result drops back into
`config/efficacy.yaml` as `source: literature` (the loader's top tier).
"""

from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path

import gemmi

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))

from pharmpipe.util.paths import (  # noqa: E402
    CATALOGUE_DIR,
    target_catalogue_dir,
    target_structures_dir,
)

_FIELDS = ["target", "het", "ligand_name", "in_chembl", "representative_pdb",
           "pubmed_id", "doi", "citation_title"]


def _clean(value: str | None) -> str:
    if not value:
        return ""
    v = gemmi.cif.as_string(value).strip()
    return "" if v in {"?", ".", ""} else v


def primary_citation(cif: Path) -> tuple[str, str, str]:
    """(pubmed_id, doi, title) for the structure's *primary* citation."""
    if not cif.exists():
        return "", "", ""
    block = gemmi.cif.read(str(cif)).sole_block()
    ids = [gemmi.cif.as_string(x) for x in block.find_loop("_citation.id")]
    if ids:                                     # loop form: pick the 'primary' row
        pm = list(block.find_loop("_citation.pdbx_database_id_PubMed"))
        do = list(block.find_loop("_citation.pdbx_database_id_DOI"))
        ti = list(block.find_loop("_citation.title"))
        i = ids.index("primary") if "primary" in ids else 0
        pick = lambda lst: _clean(lst[i]) if i < len(lst) else ""  # noqa: E731
        return pick(pm), pick(do), pick(ti)
    return (_clean(block.find_value("_citation.pdbx_database_id_PubMed")),
            _clean(block.find_value("_citation.pdbx_database_id_DOI")),
            _clean(block.find_value("_citation.title")))


def _ligand_names(slug: str) -> dict[str, str]:
    path = target_catalogue_dir(slug) / "unique_ligands.csv"
    if not path.exists():
        return {}
    return {r["het_code"].upper(): r.get("name", "")
            for r in csv.DictReader(path.open(encoding="utf-8"))}


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--resolved", type=Path,
                    default=CATALOGUE_DIR / "stage3_efficacy_resolved.csv")
    ap.add_argument("--out", type=Path, default=CATALOGUE_DIR / "literature_worklist.csv")
    args = ap.parse_args(argv)

    names: dict[str, dict[str, str]] = {}
    rows: list[dict] = []
    for r in csv.DictReader(args.resolved.open(encoding="utf-8")):
        if r["sign"] != "unknown" or r["track"] == "separate_state":
            continue                            # already classified
        slug = r["target"]
        names.setdefault(slug, _ligand_names(slug))
        cif = target_structures_dir(slug) / f"{r['pdb_id']}.cif"
        pmid, doi, title = primary_citation(cif)
        rows.append({
            "target": slug,
            "het": r["het"],
            "ligand_name": names[slug].get(r["het"].upper(), ""),
            "in_chembl": "yes" if r.get("chembl_id") else "no",
            "representative_pdb": r["pdb_id"],
            "pubmed_id": pmid,
            "doi": doi,
            "citation_title": title,
        })

    rows.sort(key=lambda x: (x["target"], x["het"]))
    with args.out.open("w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=_FIELDS)
        w.writeheader()
        w.writerows(rows)

    with_pmid = sum(1 for x in rows if x["pubmed_id"])
    print(f"Wrote {args.out} — {len(rows)} ligands, {with_pmid} with a PubMed id "
          f"({100 * with_pmid / max(1, len(rows)):.0f}%)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
