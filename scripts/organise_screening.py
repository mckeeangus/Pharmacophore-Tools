#!/usr/bin/env python
"""Organise the DrugCLIP screening deposit into data/screening/<key>/.

Moves each docked PDB directory (out/<pdb>/) to its catalogue-keyed home
data/screening/<key>/ and drops the paired DrugCLIP index there as index_<key>.csv (copied
from website_output/, already in pipeline format), so the existing --docked-dir / --seed-docked
auto-detection works unchanged. Every pairing is validated by mol_id overlap before anything
moves. Writes data/screening/manifest.csv. Idempotent: a set already organised is left in place
(its index refreshed). Run: pixi run python scripts/organise_screening.py [--min-overlap 0.99].
"""

from __future__ import annotations

import argparse
import csv
import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from pharmpipe.screening.crosswalk import (  # noqa: E402
    RAW_DOCKED_DIR,
    RAW_INDEX_DIR,
    SCREENING_DIR,
    docked_mol_ids,
    load_crosswalk,
    validate_overlap,
)


def _score_range(index_path: Path) -> tuple[float, float] | None:
    scores = []
    with index_path.open(encoding="utf-8") as fh:
        for row in csv.DictReader(fh):
            try:
                scores.append(float(row["drugclip_score"]))
            except (KeyError, ValueError, TypeError):
                pass
    return (min(scores), max(scores)) if scores else None


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--min-overlap", type=float, default=0.99,
                    help="minimum docked/index mol_id overlap to accept a pairing (default 0.99)")
    ap.add_argument("--dry-run", action="store_true", help="report but do not move anything")
    args = ap.parse_args(argv)

    _, targets = load_crosswalk()
    SCREENING_DIR.mkdir(parents=True, exist_ok=True)
    rows = []
    for t in targets:
        src = RAW_DOCKED_DIR / t.pdb
        dest = SCREENING_DIR / t.key
        index_src = RAW_INDEX_DIR / t.index
        # Locate the SDFs (still in out/, or already moved to data/screening/<key>/).
        organised = dest.exists() and any(dest.glob("*_docked.sdf"))
        check_dir = dest if organised else src
        overlap = validate_overlap(t, check_dir, RAW_INDEX_DIR)
        n = len(docked_mol_ids(check_dir))
        if n == 0:
            print(f"  SKIP {t.key}: no docked poses in {check_dir}")
            continue
        if overlap < args.min_overlap:
            print(f"  ERROR {t.key}: docked/index overlap {overlap:.0%} < {args.min_overlap:.0%} "
                  f"({t.pdb} vs {t.index}) — check the crosswalk", file=sys.stderr)
            continue
        if not organised and not args.dry_run:
            dest.mkdir(parents=True, exist_ok=True)
            for sdf in src.glob("*_docked.sdf"):
                shutil.move(str(sdf), str(dest / sdf.name))
            log = RAW_DOCKED_DIR / f"{t.pdb}.log"
            if log.exists():
                shutil.copy2(str(log), str(dest / f"{t.key}.log"))
        if not args.dry_run:
            shutil.copy2(str(index_src), str(dest / f"index_{t.key}.csv"))
        rng = _score_range(index_src)
        print(f"  {t.key:<22} {t.pdb:<10} n={n:<5} overlap={overlap:.0%} "
              f"score={rng[0]:.2f}..{rng[1]:.2f}" if rng else f"  {t.key}: n={n}")
        rows.append({"key": t.key, "slug": t.slug, "pdb": t.pdb, "n_poses": n,
                     "index": f"index_{t.key}.csv",
                     "drugclip_score_min": f"{rng[0]:.3f}" if rng else "",
                     "drugclip_score_max": f"{rng[1]:.3f}" if rng else "",
                     "known_actives_cell": t.cell or "", "literature": t.literature or ""})

    if not args.dry_run and rows:
        manifest = SCREENING_DIR / "manifest.csv"
        with manifest.open("w", newline="", encoding="utf-8") as fh:
            w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
            w.writeheader()
            w.writerows(rows)
        print(f"\nOrganised {len(rows)} screening set(s) -> {SCREENING_DIR} (manifest.csv)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
