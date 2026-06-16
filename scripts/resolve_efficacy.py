#!/usr/bin/env python
"""Stage 3.3 CLI — resolve the efficacy of still-`unknown` ligands via ChEMBL.

NETWORK: run on a login/data-mover node on Gadi (compute nodes have no internet).
Every ChEMBL response is cached under data/_cache/chembl/, so a second run (and the
offline Stage 3 grouping that consumes the output) needs no network.

For each target it finds the HET codes that resolve to `unknown` under the curated
config alone, maps the structure's verified UniProt accession(s) to ChEMBL
target(s), looks up each ligand's subtype-specific mechanism, and writes
catalogue/stage3_efficacy_resolved.csv. Unmatched ligands stay `unknown`.

    pixi run resolve-efficacy --config config/targets.yaml
    pixi run resolve-efficacy --config config/targets.yaml --targets adrb2,net_slc6a2
"""

from __future__ import annotations

import argparse
import csv
import json
import logging
import sys
from pathlib import Path

import requests

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from pharmpipe.config import load_config  # noqa: E402
from pharmpipe.groups import group, resolve  # noqa: E402
from pharmpipe.groups.efficacy import load_efficacy  # noqa: E402
from pharmpipe.util.paths import (  # noqa: E402
    CATALOGUE_DIR,
    ensure_dir,
    target_catalogue_dir,
)

log = logging.getLogger("pharmpipe.resolve")

_FIELDS = ["target", "het", "pdb_id", "inchikey", "chembl_id", "action_type",
           "sign", "track", "source", "confidence", "note"]


def _accessions(slug: str) -> list[str]:
    path = target_catalogue_dir(slug) / "resolved.json"
    if not path.exists():
        return []
    data = json.loads(path.read_text(encoding="utf-8"))
    return [a["accession"] for a in data.get("accessions", []) if a.get("accession")]


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--config", required=True, type=Path, help="Path to targets.yaml")
    p.add_argument("--efficacy", type=Path, default=None, help="Path to efficacy.yaml")
    p.add_argument("--targets", default="", help="Comma-separated subset of slugs")
    p.add_argument("--delay", type=float, default=0.2, help="Politeness delay (s)")
    p.add_argument("-v", "--verbose", action="store_true")
    return p.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    logging.basicConfig(
        level=logging.INFO if args.verbose else logging.WARNING,
        format="%(asctime)s %(levelname)s %(name)s %(message)s", datefmt="%H:%M:%S")

    cfg = load_config(args.config)
    # Config-only efficacy (no resolved CSV) so we target genuine unknowns.
    eff = load_efficacy(args.efficacy, resolved_path=Path("does-not-exist"))
    het_index = resolve.build_het_inchikey_index()
    log.info("HET->InChIKey index: %d entries", len(het_index))

    wanted = {s.strip() for s in args.targets.split(",") if s.strip()}
    targets = [t for t in cfg.targets if not wanted or t.slug in wanted]

    rows: list[dict] = []
    session = requests.Session()
    session.headers.update({"Accept": "application/json"})

    for t in targets:
        slug = t.slug
        teff = eff.get(slug)
        poses = group.load_poses(slug)
        if not poses:
            continue
        rep_pdb: dict[str, str] = {}
        unknown_hets: list[str] = []
        for p in poses:
            het = p.het_code.upper()
            rep_pdb.setdefault(het, p.pdb_id)
            if teff.call(het).is_unknown and het not in unknown_hets:
                unknown_hets.append(het)
        if not unknown_hets:
            print(f"[{slug}] no unknowns to resolve", flush=True)
            continue

        chembl_targets: set[str] = set()
        for acc in _accessions(slug):
            chembl_targets.update(
                resolve.accession_to_chembl_targets(acc, session, args.delay))
        if not chembl_targets:
            log.warning("[%s] no ChEMBL target for accessions; all stay unknown", slug)

        resolved_n = 0
        for het in unknown_hets:
            r = resolve.resolve_het(het, het_index.get(het), chembl_targets,
                                    session, args.delay)
            rows.append({
                "target": slug, "het": het, "pdb_id": rep_pdb.get(het, ""),
                "inchikey": r.inchikey or "", "chembl_id": r.chembl_id or "",
                "action_type": r.action_type or "", "sign": r.sign,
                "track": r.track, "source": r.source, "confidence": r.confidence,
                "note": r.note,
            })
            if r.track == "separate_state" or r.sign != "unknown":
                resolved_n += 1
        print(f"[{slug}] {resolved_n}/{len(unknown_hets)} unknowns resolved "
              f"(ChEMBL targets: {len(chembl_targets)})", flush=True)

    out = ensure_dir(CATALOGUE_DIR) / "stage3_efficacy_resolved.csv"
    with out.open("w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=_FIELDS)
        w.writeheader()
        w.writerows(rows)
    decided = sum(1 for r in rows if r["sign"] != "unknown" or r["track"] == "separate_state")
    print(f"\nWrote {out} — {decided}/{len(rows)} ligands resolved", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
