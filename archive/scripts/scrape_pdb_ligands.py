#!/usr/bin/env python
"""CLI: scrape PDB ligand-bound structures for the configured targets and build
the catalogue + bound-pose mol2 files.

NETWORK-HEAVY — run on a Gadi login/data-mover node (compute nodes have no
internet). All responses are cached under data/_cache so re-runs are offline.

    pixi run scrape-pdb-ligands --config config/targets.yaml
"""

from __future__ import annotations

import argparse
import logging
import sys
from datetime import date
from pathlib import Path

# Make `pharmpipe` importable even without the editable install.
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))

from pharmpipe.catalogue import build, report  # noqa: E402
from pharmpipe.config import load_config  # noqa: E402
from pharmpipe.pipeline import extract_mol2, search_and_curate  # noqa: E402
from pharmpipe.util.paths import CATALOGUE_DIR, ensure_dir  # noqa: E402

try:
    from tqdm import tqdm
except ImportError:  # pragma: no cover
    tqdm = None

log = logging.getLogger("pharmpipe")


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--config", required=True, type=Path, help="Path to targets.yaml")
    p.add_argument("--targets", default="", help="Comma-separated subset of slugs")
    p.add_argument("--extract-mode", choices=["all_instances", "representative"],
                   help="Override config extract_mode")
    p.add_argument("--max-extract", type=int, default=None,
                   help="Cap structures downloaded for mol2 extraction per target")
    p.add_argument("--no-mol2", action="store_true",
                   help="Build catalogue only; skip mmCIF download + mol2 extraction")
    p.add_argument("--no-xlsx", action="store_true", help="Skip xlsx workbook")
    p.add_argument("-v", "--verbose", action="store_true")
    return p.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    logging.basicConfig(
        level=logging.INFO if args.verbose else logging.WARNING,
        format="%(asctime)s %(levelname)s %(name)s %(message)s",
        datefmt="%H:%M:%S")

    cfg = load_config(args.config)
    opts = cfg.search
    if args.extract_mode:
        opts.extract_mode = args.extract_mode
    http_cfg = opts.http()

    wanted = {s.strip() for s in args.targets.split(",") if s.strip()}
    targets = [t for t in cfg.targets if not wanted or t.slug in wanted]
    if not targets:
        print(f"No matching targets for {sorted(wanted)}", file=sys.stderr)
        return 2

    search_date = date.today().isoformat()
    results: list[build.TargetResult] = []

    for t in targets:
        print(f"[{t.slug}] resolving & searching …", flush=True)
        tr = search_and_curate(t, opts, http_cfg)
        print(f"[{t.slug}] {len(tr.hits)} structures | "
              f"{len(tr.curation.kept_het_codes())} unique ligands kept | "
              f"{len(tr.curation.flagged_het_codes())} flagged", flush=True)

        if not args.no_mol2:
            bar = tqdm(desc=f"{t.slug} mol2", unit="struct") if tqdm else None
            extract_mol2(tr, opts, http_cfg, max_structures=args.max_extract, progress=bar)
            if bar is not None:
                bar.close()
            n_ok = sum(1 for r in tr.extract_results if r.ok)
            print(f"[{t.slug}] mol2 written: {n_ok}", flush=True)

        build.write_target_csvs(tr)
        report.write_resolved_json(tr)
        results.append(tr)

    ensure_dir(CATALOGUE_DIR)
    md = build.write_combined_markdown(results, CATALOGUE_DIR / "ligand_catalogue.md",
                                       search_date)
    summary_path = report.write_run_summary(results, CATALOGUE_DIR / "run_summary.md",
                                             search_date)
    if not args.no_xlsx:
        build.write_xlsx(results, CATALOGUE_DIR / "ligand_catalogue.xlsx")

    print("\n" + report.build_run_summary(results, search_date))
    print(f"\nCatalogue: {md}")
    print(f"Summary:   {summary_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
