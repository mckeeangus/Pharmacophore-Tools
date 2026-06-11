"""Query the RCSB Search + Data APIs for ligand-bound structures.

Two stages:
  1. Search API (POST JSON) -> all entry IDs whose polymer entities map to a
     given UniProt accession.
  2. Data GraphQL API (batched) -> per-entry resolution, method, title, mapped
     UniProt accessions, and every non-polymer (ligand) *instance* with its
     comp_id / chain / residue number (used to name and locate bound poses).

Chem-component metadata (name, formula, SMILES) is fetched per HET code from the
Data REST API and cached.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field

from ..util import http

log = logging.getLogger("pharmpipe.rcsb")

SEARCH_URL = "https://search.rcsb.org/rcsbsearch/v2/query"
GRAPHQL_URL = "https://data.rcsb.org/graphql"
CHEMCOMP_URL = "https://data.rcsb.org/rest/v1/core/chemcomp/{comp_id}"

ACC_ATTR = ("rcsb_polymer_entity_container_identifiers."
            "reference_sequence_identifiers.database_accession")
DB_ATTR = ("rcsb_polymer_entity_container_identifiers."
           "reference_sequence_identifiers.database_name")


@dataclass
class LigandInstance:
    pdb_id: str
    comp_id: str
    auth_asym_id: str        # chain
    auth_seq_id: str         # residue number (string; may carry insertion code)


@dataclass
class StructureHit:
    pdb_id: str
    title: str = ""
    method: str = ""
    resolution: float | None = None
    uniprot_accessions: list[str] = field(default_factory=list)
    instances: list[LigandInstance] = field(default_factory=list)

    @property
    def het_codes(self) -> list[str]:
        return sorted({i.comp_id for i in self.instances})


@dataclass
class ChemComp:
    comp_id: str
    name: str = ""
    formula: str = ""
    smiles: str = ""
    formula_weight: float | None = None


def search_entries_by_accession(accession: str, cfg: http.HttpConfig) -> list[str]:
    """All PDB entry IDs whose polymer entities map to ``accession`` (UniProt)."""
    payload = {
        "query": {
            "type": "group",
            "logical_operator": "and",
            "nodes": [
                {"type": "terminal", "service": "text", "parameters": {
                    "attribute": ACC_ATTR, "operator": "exact_match",
                    "value": accession}},
                {"type": "terminal", "service": "text", "parameters": {
                    "attribute": DB_ATTR, "operator": "exact_match",
                    "value": "UniProt"}},
            ],
        },
        "return_type": "entry",
        "request_options": {"return_all_hits": True},
    }
    data = http.post_json(SEARCH_URL, payload, cfg, category="rcsb_search")
    if not data:
        return []
    return [r["identifier"] for r in data.get("result_set", [])]


_ENTRY_FIELDS = """
    rcsb_id
    struct { title }
    rcsb_entry_info { resolution_combined experimental_method }
    polymer_entities {
      rcsb_polymer_entity_container_identifiers {
        reference_sequence_identifiers { database_accession database_name }
      }
    }
    nonpolymer_entities {
      nonpolymer_entity_instances {
        rcsb_nonpolymer_entity_instance_container_identifiers {
          comp_id auth_asym_id auth_seq_id
        }
      }
    }
"""


def _batched(seq: list[str], n: int):
    for i in range(0, len(seq), n):
        yield seq[i:i + n]


def fetch_structure_metadata(pdb_ids: list[str], cfg: http.HttpConfig,
                             batch_size: int = 50) -> dict[str, StructureHit]:
    """Batched GraphQL fetch of per-entry metadata + ligand instances."""
    hits: dict[str, StructureHit] = {}
    for batch in _batched(pdb_ids, batch_size):
        ids = '","'.join(batch)
        query = f'{{ entries(entry_ids: ["{ids}"]) {{{_ENTRY_FIELDS}}} }}'
        data = http.post_json(GRAPHQL_URL, {"query": query}, cfg, category="rcsb_graphql")
        for entry in (data or {}).get("data", {}).get("entries") or []:
            hit = _parse_entry(entry)
            hits[hit.pdb_id] = hit
    return hits


def _parse_entry(entry: dict) -> StructureHit:
    pdb_id = entry["rcsb_id"].upper()
    info = entry.get("rcsb_entry_info") or {}
    res_list = info.get("resolution_combined") or []
    resolution = min(res_list) if res_list else None
    accessions: list[str] = []
    for pe in entry.get("polymer_entities") or []:
        ids = (pe or {}).get("rcsb_polymer_entity_container_identifiers") or {}
        for ref in ids.get("reference_sequence_identifiers") or []:
            if ref.get("database_name") == "UniProt" and ref.get("database_accession"):
                accessions.append(ref["database_accession"])
    instances: list[LigandInstance] = []
    for ne in entry.get("nonpolymer_entities") or []:
        for inst in (ne or {}).get("nonpolymer_entity_instances") or []:
            cid = inst.get("rcsb_nonpolymer_entity_instance_container_identifiers") or {}
            if cid.get("comp_id"):
                instances.append(LigandInstance(
                    pdb_id=pdb_id,
                    comp_id=cid["comp_id"],
                    auth_asym_id=str(cid.get("auth_asym_id", "")),
                    auth_seq_id=str(cid.get("auth_seq_id", "")),
                ))
    return StructureHit(
        pdb_id=pdb_id,
        title=(entry.get("struct") or {}).get("title", "") or "",
        method=info.get("experimental_method", "") or "",
        resolution=resolution,
        uniprot_accessions=sorted(set(accessions)),
        instances=instances,
    )


def get_chem_comp(comp_id: str, cfg: http.HttpConfig) -> ChemComp:
    """Chem-component name / formula / SMILES for a HET code (cached)."""
    data = http.get_json(CHEMCOMP_URL.format(comp_id=comp_id), cfg,
                         category="rcsb_chemcomp", cache_key=f"cc:{comp_id}",
                         allow_404=True)
    if not data:
        return ChemComp(comp_id=comp_id)
    cc = data.get("chem_comp") or {}
    desc = data.get("rcsb_chem_comp_descriptor") or {}
    smiles = desc.get("SMILES_stereo") or desc.get("SMILES") or ""
    return ChemComp(
        comp_id=comp_id,
        name=cc.get("name", "") or "",
        formula=cc.get("formula", "") or "",
        smiles=smiles,
        formula_weight=cc.get("formula_weight"),
    )
