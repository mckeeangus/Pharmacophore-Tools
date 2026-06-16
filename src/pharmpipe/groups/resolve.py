"""Stage 3.3 — resolve the efficacy of unclassified ligands via ChEMBL.

Pipeline (network at the edges, pure logic in the middle):

  1. ``HET -> InChIKey`` is **offline** — read from the cached RCSB chem-component
     JSON written in Stage 1 (``data/_cache/rcsb_chemcomp/``), which already
     carries a computed InChIKey. No RDKit round-trip is needed.
  2. ``UniProt accession -> ChEMBL target`` — the structure's *verified* accession
     (from ``resolved.json``) is mapped to ChEMBL target id(s). The sign is keyed
     to these targets so subtype-flips (e.g. 4BP-TQS: alpha7 agonist vs alpha4beta2
     antagonist) are never crossed.
  3. ``InChIKey -> molecule -> mechanism`` (ChEMBL REST), filtered to the target(s)
     of step 2, yields an ``action_type``.
  4. ``action_type -> sign`` is a fixed lookup; degraders route to separate-state.

Conflicting subtype mechanisms, unmapped action types, and missing data all leave
the ligand ``unknown`` — it stays on the review list, never force-bucketed. Every
network response is cached under ``data/_cache/chembl/`` so re-runs are offline.
"""

from __future__ import annotations

import hashlib
import json
import logging
import time
from dataclasses import dataclass
from pathlib import Path

import requests

from ..util.paths import CACHE_DIR, ensure_dir

log = logging.getLogger("pharmpipe.groups.resolve")

CHEMBL_BASE = "https://www.ebi.ac.uk/chembl/api/data"

# action_type (ChEMBL/IUPHAR vocabulary, upper-cased) -> efficacy sign.
ACTION_SIGN: dict[str, str] = {
    "AGONIST": "positive",
    "PARTIAL AGONIST": "positive",
    "POSITIVE ALLOSTERIC MODULATOR": "positive",
    "POSITIVE MODULATOR": "positive",
    "RELEASING AGENT": "positive",
    "OPENER": "positive",
    "ACTIVATOR": "positive",
    "ANTAGONIST": "neutral",
    "BLOCKER": "neutral",
    "INVERSE AGONIST": "negative",
    "NEGATIVE ALLOSTERIC MODULATOR": "negative",
    "NEGATIVE MODULATOR": "negative",
    "INHIBITOR": "negative",
    "REUPTAKE INHIBITOR": "negative",
}
# action types that mean the ligand changes the protein's *state* (not a cell).
DEGRADER_ACTIONS = {"DEGRADER", "PROTEIN DEGRADER"}


@dataclass(frozen=True)
class Resolution:
    """One ligand's resolved efficacy (chemical-level, not per-pose)."""
    het: str
    inchikey: str | None
    chembl_id: str | None
    action_type: str | None
    sign: str               # positive | neutral | negative | unknown
    track: str              # cell | separate_state
    source: str             # chembl | none
    confidence: str         # high | medium | low | none
    note: str = ""


# --- offline: HET -> InChIKey ------------------------------------------------

def build_het_inchikey_index(cache_dir: Path | None = None) -> dict[str, str]:
    """Map every cached chem-component HET code to its InChIKey (offline)."""
    base = (cache_dir or CACHE_DIR) / "rcsb_chemcomp"
    index: dict[str, str] = {}
    if not base.exists():
        return index
    for f in base.glob("*.json"):
        try:
            data = json.loads(f.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            continue
        het = (data.get("chem_comp") or {}).get("id")
        ik = (data.get("rcsb_chem_comp_descriptor") or {}).get("InChIKey")
        if het and ik:
            index[het.upper()] = ik
    return index


# --- network: cached ChEMBL GETs ---------------------------------------------

def _cache_path(kind: str, url: str, params: dict) -> Path:
    key = hashlib.sha1(f"{url}?{json.dumps(params, sort_keys=True)}".encode()).hexdigest()[:16]
    return ensure_dir(CACHE_DIR / "chembl") / f"{kind}_{key}.json"


def _get(kind: str, url: str, params: dict, session: requests.Session,
         delay: float, retries: int) -> dict | None:
    """Cached GET. Caches the empty/404 result too, so misses stay offline."""
    cf = _cache_path(kind, url, params)
    if cf.exists():
        return json.loads(cf.read_text(encoding="utf-8"))
    for attempt in range(retries):
        try:
            r = session.get(url, params={**params, "format": "json"}, timeout=30)
        except requests.RequestException as exc:
            log.warning("ChEMBL %s request error (%s); retry %d", kind, exc, attempt + 1)
            time.sleep(delay * (attempt + 1))
            continue
        if r.status_code == 200:
            data = r.json()
            cf.write_text(json.dumps(data), encoding="utf-8")
            time.sleep(delay)
            return data
        if r.status_code == 404:
            cf.write_text("null", encoding="utf-8")
            return None
        log.warning("ChEMBL %s HTTP %d; retry %d", kind, r.status_code, attempt + 1)
        time.sleep(delay * (attempt + 1))
    return None


def accession_to_chembl_targets(accession: str, session: requests.Session,
                                delay: float = 0.2, retries: int = 3) -> list[str]:
    data = _get("target", f"{CHEMBL_BASE}/target.json",
                {"target_components__accession": accession, "limit": 200},
                session, delay, retries)
    if not data:
        return []
    return [t["target_chembl_id"] for t in data.get("targets", [])
            if t.get("target_chembl_id")]


def inchikey_to_molecule(inchikey: str, session: requests.Session,
                         delay: float = 0.2, retries: int = 3) -> str | None:
    """Return the *parent* ChEMBL id for an InChIKey (mechanism is keyed by parent).

    ChEMBL attaches mechanism-of-action to the parent molecule, so a salt/child
    hit is normalised to its parent here; falls back to the matched id.
    """
    data = _get("molecule", f"{CHEMBL_BASE}/molecule.json",
                {"molecule_structures__standard_inchi_key": inchikey, "limit": 1},
                session, delay, retries)
    if not data or not data.get("molecules"):
        return None
    mol = data["molecules"][0]
    parent = (mol.get("molecule_hierarchy") or {}).get("parent_chembl_id")
    return parent or mol.get("molecule_chembl_id")


def molecule_mechanisms(parent_chembl_id: str, session: requests.Session,
                        delay: float = 0.2, retries: int = 3) -> list[dict]:
    data = _get("mechanism", f"{CHEMBL_BASE}/mechanism.json",
                {"parent_molecule_chembl_id": parent_chembl_id, "limit": 200},
                session, delay, retries)
    return data.get("mechanisms", []) if data else []


# --- resolution logic (pure given the fetched data) --------------------------

def _sign_from_actions(actions: set[str]) -> tuple[str, str]:
    """(sign, confidence) from the set of subtype-relevant action types."""
    signs = {ACTION_SIGN[a] for a in actions if a in ACTION_SIGN}
    if len(signs) == 1:
        return next(iter(signs)), "high"
    if not signs:
        return "unknown", "low"          # action types present but none mapped
    return "unknown", "low"              # conflicting signs across subtypes


def resolve_het(het: str, inchikey: str | None, target_chembl_ids: set[str],
                session: requests.Session, delay: float = 0.2,
                retries: int = 3) -> Resolution:
    if not inchikey:
        return Resolution(het, None, None, None, "unknown", "cell", "none", "none",
                          "no cached InChIKey")
    mol = inchikey_to_molecule(inchikey, session, delay, retries)
    if not mol:
        return Resolution(het, inchikey, None, None, "unknown", "cell", "none", "none",
                          "no ChEMBL molecule for InChIKey")
    mechs = molecule_mechanisms(mol, session, delay, retries)
    relevant = [m for m in mechs
                if m.get("target_chembl_id") in target_chembl_ids and m.get("action_type")]
    actions = {m["action_type"].upper() for m in relevant}
    if not actions:
        return Resolution(het, inchikey, mol, None, "unknown", "cell", "chembl", "none",
                          "no subtype-specific mechanism")
    if actions & DEGRADER_ACTIONS:
        return Resolution(het, inchikey, mol, "DEGRADER", "n/a", "separate_state",
                          "chembl", "high", "degrader/SERD — separate state")
    sign, confidence = _sign_from_actions(actions)
    note = "" if sign != "unknown" else "unmapped or conflicting subtype mechanisms"
    return Resolution(het, inchikey, mol, "|".join(sorted(actions)), sign, "cell",
                      "chembl", confidence, note)
