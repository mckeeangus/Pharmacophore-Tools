#!/usr/bin/env python
"""Stage 3 CLI — organise Stage-2 site-aligned poses into effect-coherent,
pocket-verified cells: cell = (verified pocket) × (efficacy sign).

OFFLINE: reads only the tracked catalogue + the cached native structures under
data/targets/<slug>/structures/ (no network), so it is safe on a Gadi compute
node. PyMOL ``.pse`` baking needs the ``viz`` feature:

    pixi run group-effects --config config/targets.yaml --targets gaba_a
    pixi run -e viz group-effects --config config/targets.yaml   # also bake .pse

Outputs per target under catalogue/<slug>/: effect_groups.json,
<slug>_stage3_report.md, groups/<pocket>__<efficacy>/ (mol2 + session),
review/{separate_state,unknown,quarantine}/, and <slug>_grouped.pse. The shared
catalogue/run_summary.md gains a Stage 3 section.
"""

from __future__ import annotations

import argparse
import logging
import sys
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from pharmpipe.config import load_config  # noqa: E402
from pharmpipe.groups import group, report, visualize  # noqa: E402
from pharmpipe.groups.efficacy import load_efficacy  # noqa: E402
from pharmpipe.groups.pockets import load_pockets  # noqa: E402
from pharmpipe.sites.config import load_sites  # noqa: E402

log = logging.getLogger("pharmpipe")


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--config", required=True, type=Path, help="Path to targets.yaml")
    p.add_argument("--pockets", type=Path, default=None, help="Path to pockets.yaml")
    p.add_argument("--efficacy", type=Path, default=None, help="Path to efficacy.yaml")
    p.add_argument("--sites", type=Path, default=None, help="Path to sites.yaml (anchors)")
    p.add_argument("--targets", default="", help="Comma-separated subset of slugs")
    p.add_argument("--no-pse", action="store_true", help="Write .pml only, never bake .pse")
    p.add_argument("-v", "--verbose", action="store_true")
    return p.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    logging.basicConfig(
        level=logging.INFO if args.verbose else logging.WARNING,
        format="%(asctime)s %(levelname)s %(name)s %(message)s", datefmt="%H:%M:%S")

    cfg = load_config(args.config)
    pockets = load_pockets(args.pockets)
    efficacy = load_efficacy(args.efficacy)
    sites = load_sites(args.sites)

    wanted = {s.strip() for s in args.targets.split(",") if s.strip()}
    targets = [t for t in cfg.targets if not wanted or t.slug in wanted]
    if not targets:
        print(f"No matching targets for {sorted(wanted)}", file=sys.stderr)
        return 2

    search_date = date.today().isoformat()
    results: list[group.GroupResult] = []
    for t in targets:
        slug = t.slug
        res = group.group_target(slug, pockets.get(slug), pockets.defaults,
                                 efficacy.get(slug))
        if not res.poses:
            print(f"[{slug}] no Stage-2 poses found — skipping", flush=True)
            continue

        folders = report.write_pose_folders(res)
        report.write_effect_groups_json(res)
        report.write_stage3_report(res, search_date)
        datasets = report.write_datasets(res)
        site = sites.get(slug)
        arts = visualize.build_sessions(res, folders,
                                        anchor_het=site.anchor_het if site else None,
                                        make_pse=not args.no_pse)
        visualize.build_set_sessions(datasets, make_pse=not args.no_pse)

        sc = group.status_counts(res)
        pse = "pse" if "grouped_pse" in arts else "pml-only"
        print(f"[{slug}] pockets={res.pockets_found} | {sc['cells']} cells "
              f"({sc['in_cells']} poses) | sep-state {sc['separate_state']} | "
              f"unknown {sc['unknown']} | quarantined {sc['quarantined']} | "
              f"{arts['cell_sessions']} cell sessions [{pse}] | "
              f"datasets: {len(datasets['all_poses'])} all / "
              f"{len(datasets['representative'])} representative", flush=True)
        results.append(res)

    if results and not wanted:
        # Only rebuild the cross-target master pools on a full run, so a targeted
        # re-run doesn't wipe the other targets' contributions.
        combined = report.write_combined_datasets(results)
        visualize.build_set_sessions(combined, make_pse=not args.no_pse)
        print(f"\nCombined master datasets: {len(combined['all_poses'])} poses / "
              f"{len(combined['representative'])} representative", flush=True)
    if results:
        path = report.update_run_summary(results, search_date)
        print(f"Run summary updated: {path}", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
