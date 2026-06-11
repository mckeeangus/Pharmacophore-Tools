"""Resolve & verify each target to UniProt accession(s).

Policy: ``human_preferred`` — resolve the human (taxonomy 9606) reviewed entry
per gene where possible; verify the config hint and warn on mismatch. Surrogate
accessions (e.g. AChBP, dDAT) are verified and recorded with role="surrogate"
and only used downstream as gap-fillers. Non-human targets (HIV-1 protease,
CavAb) verify their hint accession directly.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from datetime import date

from ..config import SearchOptions, Target
from ..util import http

log = logging.getLogger("pharmpipe.uniprot")

UNIPROT_ENTRY = "https://rest.uniprot.org/uniprotkb/{acc}.json"
UNIPROT_SEARCH = "https://rest.uniprot.org/uniprotkb/search"


@dataclass
class ResolvedAccession:
    accession: str
    uniprot_id: str
    taxonomy_id: int
    organism_name: str
    genes: list[str]
    protein_name: str
    reviewed: bool
    role: str = "primary"            # primary | surrogate
    surrogate_name: str | None = None


@dataclass
class ResolvedTarget:
    target: Target
    search_date: str
    accessions: list[ResolvedAccession] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    def primary_accessions(self) -> list[str]:
        return [a.accession for a in self.accessions if a.role == "primary"]

    def surrogate_accessions(self) -> list[str]:
        return [a.accession for a in self.accessions if a.role == "surrogate"]

    def all_accessions(self) -> list[str]:
        return [a.accession for a in self.accessions]


def _parse_entry(data: dict, *, role: str = "primary",
                 surrogate_name: str | None = None) -> ResolvedAccession:
    org = data.get("organism", {})
    genes = [g.get("geneName", {}).get("value") for g in data.get("genes", [])]
    genes = [g for g in genes if g]
    desc = data.get("proteinDescription", {})
    rec = desc.get("recommendedName") or {}
    name = (rec.get("fullName", {}) or {}).get("value")
    if not name:
        submitted = desc.get("submissionNames") or []
        if submitted:
            name = submitted[0].get("fullName", {}).get("value")
    return ResolvedAccession(
        accession=data.get("primaryAccession", "?"),
        uniprot_id=data.get("uniProtkbId", "?"),
        taxonomy_id=org.get("taxonId", 0),
        organism_name=org.get("scientificName", "?"),
        genes=genes,
        protein_name=name or "?",
        reviewed=data.get("entryType", "").lower().find("reviewed") >= 0,
        role=role,
        surrogate_name=surrogate_name,
    )


def verify_accession(acc: str, cfg: http.HttpConfig, *, role: str = "primary",
                     surrogate_name: str | None = None) -> ResolvedAccession | None:
    data = http.get_json(UNIPROT_ENTRY.format(acc=acc), cfg,
                         category="uniprot_entry", cache_key=f"entry:{acc}",
                         allow_404=True)
    if not data:
        log.warning("UniProt accession %s not found", acc)
        return None
    return _parse_entry(data, role=role, surrogate_name=surrogate_name)


def resolve_human_gene(gene: str, taxonomy_id: int,
                       cfg: http.HttpConfig) -> ResolvedAccession | None:
    """Find the reviewed (Swiss-Prot) entry for a gene in a given organism."""
    params = {
        "query": f"gene_exact:{gene} AND organism_id:{taxonomy_id} AND reviewed:true",
        "format": "json",
        "size": "5",
        "fields": "accession,id,gene_names,organism_name,protein_name,reviewed",
    }
    url = UNIPROT_SEARCH + "?" + "&".join(f"{k}={v}" for k, v in params.items())
    data = http.get_json(url, cfg, category="uniprot_search",
                         cache_key=f"gene:{gene}:{taxonomy_id}")
    results = (data or {}).get("results") or []
    if not results:
        return None
    # Prefer an exact primary-gene match; otherwise take the first reviewed hit.
    for entry in results:
        primary = [g.get("geneName", {}).get("value", "").upper()
                   for g in entry.get("genes", [])]
        if gene.upper() in primary:
            return _parse_entry(entry)
    return _parse_entry(results[0])


def resolve_target(target: Target, opts: SearchOptions) -> ResolvedTarget:
    cfg = opts.http()
    rt = ResolvedTarget(target=target, search_date=date.today().isoformat())
    seen: set[str] = set()

    def add(acc: ResolvedAccession | None) -> None:
        if acc and acc.accession not in seen:
            rt.accessions.append(acc)
            seen.add(acc.accession)

    is_human = target.organism == "human" and opts.organism_policy != "any"

    # 1) Resolve human accessions from gene symbols where possible.
    if is_human and target.genes:
        for gene in target.genes:
            resolved = resolve_human_gene(gene, opts.human_taxonomy_id, cfg)
            if resolved is None:
                rt.warnings.append(f"No reviewed human entry found for gene {gene}.")
                continue
            add(resolved)
            if target.uniprot_hint and resolved.accession not in target.uniprot_hint:
                rt.warnings.append(
                    f"Gene {gene} resolved to {resolved.accession} "
                    f"(hint listed {target.uniprot_hint}).")

    # 2) Verify hint accessions directly (covers non-human targets and confirms
    #    the hints; only added as primary if not already covered by gene resolution).
    for acc in target.uniprot_hint:
        if acc in seen:
            continue
        verified = verify_accession(acc, cfg)
        if verified is None:
            rt.warnings.append(f"Hint accession {acc} did not verify against UniProt.")
            continue
        # If we already resolved human genes, a non-matching hint is informational.
        if is_human and target.genes and verified.taxonomy_id != opts.human_taxonomy_id:
            rt.warnings.append(
                f"Hint {acc} is {verified.organism_name} (tax {verified.taxonomy_id}), "
                f"not human; not used as primary under human_preferred policy.")
            continue
        add(verified)

    # 3) Surrogates: verified and recorded, used only as gap-fillers.
    if opts.include_surrogates:
        for sur in target.surrogates:
            verified = verify_accession(sur.uniprot, cfg, role="surrogate",
                                        surrogate_name=sur.name)
            if verified is None:
                rt.warnings.append(f"Surrogate accession {sur.uniprot} ({sur.name}) "
                                   f"did not verify.")
                continue
            add(verified)

    if not rt.primary_accessions():
        rt.warnings.append("No primary accession resolved — "
                           "downstream search will rely on surrogates only.")
    return rt
