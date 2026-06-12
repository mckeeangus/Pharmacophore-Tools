#!/usr/bin/env python
"""CLI: keep only ligands bound at each target's relevant site, superpose their
poses into a per-target reference frame, and render a PyMOL session for visual
comparison.

NETWORK-HEAVY (downloads every structure that holds a kept ligand) — run on a
Gadi login/data-mover node. Catalogue metadata is reused from cache, so re-runs
are cheap; structure downloads are cached under data/_cache too.

    pixi run align-sites --config config/targets.yaml --targets cox2,hmgcr
    pixi run -e viz build-sessions --config config/targets.yaml   # bake .pse files

`.pml` session scripts are always written; `.pse` files are baked only when
PyMOL is importable (the `viz` environment).
"""

from __future__ import annotations

import argparse
import logging
import sys
from pathlib import Path

# Make `pharmpipe` importable even without the editable install.
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from pharmpipe.config import load_config  # noqa: E402
from pharmpipe.pipeline import search_and_curate  # noqa: E402
from pharmpipe.sites import filter as sitefilter  # noqa: E402
from pharmpipe.sites import visualize  # noqa: E402
from pharmpipe.sites.config import load_sites  # noqa: E402
from pharmpipe.sites.filter import AlignTargetResult  # noqa: E402
from pharmpipe.util.paths import (  # noqa: E402
    CATALOGUE_DIR,
    ensure_dir,
    target_aligned_mol2_dir,
)

try:
    from tqdm import tqdm
except ImportError:  # pragma: no cover
    tqdm = None

log = logging.getLogger("pharmpipe")


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--config", required=True, type=Path, help="Path to targets.yaml")
    p.add_argument("--sites", type=Path, default=None, help="Path to sites.yaml")
    p.add_argument("--targets", default="", help="Comma-separated subset of slugs")
    p.add_argument("--max-structures", type=int, default=None,
                   help="Cap structures downloaded per target (best resolution first)")
    p.add_argument("--no-pse", action="store_true", help="Write .pml only, never bake .pse")
    p.add_argument("--sessions-only", action="store_true",
                   help="Skip alignment; (re)build sessions from existing aligned mol2")
    p.add_argument("-v", "--verbose", action="store_true")
    return p.parse_args(argv)


def _existing_result(slug, site) -> AlignTargetResult:
    """Reconstruct just enough state to (re)build a session from disk."""
    files = sorted(target_aligned_mol2_dir(slug).glob("*.mol2"))
    out = AlignTargetResult(slug=slug, site=site, reference=None)
    out.aligned_files = list(files)
    return out


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    logging.basicConfig(
        level=logging.INFO if args.verbose else logging.WARNING,
        format="%(asctime)s %(levelname)s %(name)s %(message)s",
        datefmt="%H:%M:%S")

    cfg = load_config(args.config)
    sites = load_sites(args.sites)
    http_cfg = cfg.search.http()

    wanted = {s.strip() for s in args.targets.split(",") if s.strip()}
    targets = [t for t in cfg.targets if not wanted or t.slug in wanted]
    if not targets:
        print(f"No matching targets for {sorted(wanted)}", file=sys.stderr)
        return 2

    summary_rows: list[tuple[str, str, int, int, dict]] = []

    for t in targets:
        site = sites.get(t.slug)
        if site is None:
            print(f"[{t.slug}] no site definition in sites.yaml — skipping", flush=True)
            continue

        if args.sessions_only:
            out = _existing_result(t.slug, site)
            arts = visualize.build_session(out, make_pse=not args.no_pse)
            print(f"[{t.slug}] session: {', '.join(str(p) for p in arts.values())}",
                  flush=True)
            continue

        print(f"[{t.slug}] reference {site.reference_pdb} anchor {site.anchor_het} — "
              f"resolving catalogue …", flush=True)
        tr = search_and_curate(t, cfg.search, http_cfg)
        bar = tqdm(desc=f"{t.slug} align", unit="struct") if tqdm else None
        out = sitefilter.align_target(tr, site, http_cfg,
                                      max_structures=args.max_structures, progress=bar)
        if bar is not None:
            bar.close()

        if out.reference is None:
            print(f"[{t.slug}] FAILED to build site reference — skipping session",
                  flush=True)
            summary_rows.append((t.slug, site.reference_pdb, 0, 0, {}))
            continue

        arts = visualize.build_session(out, make_pse=not args.no_pse)
        kept = out.n_kept
        cand = out.n_candidates
        print(f"[{t.slug}] kept {kept}/{cand} instances at the {site.anchor_het} site "
              f"| dropped { {k: v for k, v in out.status_counts.items() if k != 'kept'} } "
              f"| {', '.join(k + '=' + str(p) for k, p in arts.items())}", flush=True)
        summary_rows.append((t.slug, site.reference_pdb, kept, cand,
                             dict(out.status_counts)))

    if summary_rows and not args.sessions_only:
        _write_summary(summary_rows)
    return 0


def _write_summary(rows) -> Path:
    lines = ["# Site-alignment summary", "",
             "Ligands kept only if their pose superposes into the reference site "
             "(binding-site-local fit) and the centroid lands within cutoff of the "
             "anchor. Dropped categories: `off_site` (wrong location), `poor_fit` / "
             "`no_pocket` (no matching pocket, e.g. wrong protein/allosteric), "
             "`not_found` (instance/structure unavailable).", "",
             "| Target | Ref | Anchor kept | Candidates | Dropped breakdown |",
             "|--------|-----|------------:|-----------:|-------------------|"]
    for slug, ref, kept, cand, counts in rows:
        dropped = {k: v for k, v in counts.items() if k != "kept"}
        lines.append(f"| {slug} | {ref} | {kept} | {cand} | "
                     f"{dropped if dropped else '—'} |")
    path = ensure_dir(CATALOGUE_DIR) / "site_alignment_summary.md"
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"\nSummary: {path}", flush=True)
    return path


if __name__ == "__main__":
    raise SystemExit(main())
