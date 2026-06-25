#!/usr/bin/env python
"""Stage 4 CLI: build ensemble pharmacophores from aligned compound sets.

Three modes:

  * single directory  -- build one model from any folder of aligned ``*.mol2``:
        pixi run build-pharmacophores --input PATH/TO/cell --out PATH/TO/out
  * one target        -- build a model per cell of a catalogue target:
        pixi run build-pharmacophores --target gr_nr3c1
  * whole catalogue   -- every cell of every target:
        pixi run build-pharmacophores --catalogue

Catalogue modes only build the ``groups/<pocket>__<efficacy>/`` cells (never the
review tracks separate_state / unknown / quarantine) and write to
``catalogue/<slug>/pharmacophores/<cell>/``. Offline.
"""

from __future__ import annotations

import argparse
import logging
import os
import shutil
import sys
from pathlib import Path

# k-means runs many small clusterings; one thread each avoids MKL oversubscription
# (and its Windows memory-leak warning) and keeps behaviour reproducible on Gadi.
os.environ.setdefault("OMP_NUM_THREADS", "1")

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from rdkit import RDLogger  # noqa: E402

# The mol2 loader deliberately falls back when RDKit can't perceive a pose; its
# per-atom kekulize/valence warnings are expected noise, so quiet them here.
RDLogger.DisableLog("rdApp.*")

from pharmpipe.features.load import read_smiles_map  # noqa: E402
from pharmpipe.pharmacophore.config import load_pharmacophore_config  # noqa: E402
from pharmpipe.pharmacophore.run import (  # noqa: E402
    build_for_cell,
    build_from_directory,
)
from pharmpipe.util.paths import (  # noqa: E402
    CATALOGUE_DIR,
    target_groups_dir,
    target_pharmacophores_dir,
)

log = logging.getLogger("build_pharmacophores")


def _cells(slug: str) -> list[Path]:
    groups = target_groups_dir(slug)
    if not groups.is_dir():
        return []
    return sorted(d for d in groups.iterdir() if d.is_dir() and any(d.glob("*.mol2")))


def _targets() -> list[str]:
    return sorted(d.name for d in CATALOGUE_DIR.iterdir()
                  if d.is_dir() and target_groups_dir(d.name).is_dir())


def _build_target(slug: str, cfg) -> tuple[int, int]:
    """Build every buildable cell of a target; returns (built, skipped)."""
    uniq = CATALOGUE_DIR / slug / "unique_ligands.csv"
    built = skipped = 0
    for cell in _cells(slug):
        out = target_pharmacophores_dir(slug) / cell.name
        res = build_for_cell(cell, out, cfg, uniq, name=f"{slug}/{cell.name}")
        if res is None:
            # Too few ligands: drop any model left over from a previous run.
            if out.exists():
                shutil.rmtree(out)
            print(f"  {slug}/{cell.name}: skipped (< {cfg.selection.min_ligands} "
                  f"ligands); removed stale output")
            skipped += 1
            continue
        print(f"  {slug}/{cell.name}: {len(res.pharmacophore.features)} features "
              f"from {res.pharmacophore.metadata['source']['n_ligands']} ligands")
        built += 1
    return built, skipped


def main(argv=None) -> int:
    logging.basicConfig(level=logging.WARNING, format="%(levelname)s %(message)s")
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    mode = ap.add_mutually_exclusive_group(required=True)
    mode.add_argument("--input", type=Path, help="a single directory of aligned mol2")
    mode.add_argument("--target", help="build every cell of one catalogue target (slug)")
    mode.add_argument("--catalogue", action="store_true", help="every cell of every target")
    ap.add_argument("--out", type=Path, help="output dir (required with --input)")
    ap.add_argument("--smiles", type=Path,
                    help="optional HET->SMILES csv (unique_ligands.csv) for --input")
    ap.add_argument("--config", type=Path, default=None)
    ap.add_argument("--method", help="override clustering.method from config")
    args = ap.parse_args(argv)

    cfg = load_pharmacophore_config(args.config)
    if args.method:
        cfg.clustering.method = args.method

    if args.input:
        if not args.out:
            ap.error("--out is required with --input")
        smiles = read_smiles_map(args.smiles) if args.smiles else None
        res = build_from_directory(args.input, args.out, cfg, smiles_map=smiles)
        if res is None:
            print(f"{args.input.name}: skipped (< {cfg.selection.min_ligands} ligands)")
            return 0
        print(f"{res.name}: {len(res.pharmacophore.features)} features -> {res.model_dir}")
        return 0

    slugs = [args.target] if args.target else _targets()
    total_built = total_skipped = 0
    for slug in slugs:
        print(f"{slug}:")
        built, skipped = _build_target(slug, cfg)
        total_built += built
        total_skipped += skipped
    print(f"\nBuilt {total_built} pharmacophore model(s) across {len(slugs)} target(s); "
          f"{total_skipped} cell(s) skipped (< {cfg.selection.min_ligands} ligands).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
