#!/usr/bin/env python
"""CLI: keep only ligands bound at each target's relevant site, superpose their
poses into a per-target reference frame, and render a PyMOL session for visual
comparison.

NETWORK-HEAVY (downloads structures that hold a kept ligand) — run on a Gadi
login/data-mover node. Catalogue metadata is reused from cache; structure
downloads are cached under data/_cache too. Structures are processed
best-resolution first and capped at --max-ligands distinct poses, so large
targets stop early.

    pixi run align-sites --config config/targets.yaml --targets cox2,hmgcr
    pixi run -e viz align-sites --config config/targets.yaml   # also bake .pse
    pixi run -e viz build-sessions --config config/targets.yaml # sessions only

`.pml` session scripts are written under data/; `.pse` files (self-contained,
tracked) are written under catalogue/<slug>/ when PyMOL is importable.
"""

from __future__ import annotations

import argparse
import logging
import sys
from datetime import date
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

_OTHER_DROPPED = ("poor_fit", "no_pocket", "not_found", "align_error")


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--config", required=True, type=Path, help="Path to targets.yaml")
    p.add_argument("--sites", type=Path, default=None, help="Path to sites.yaml")
    p.add_argument("--targets", default="", help="Comma-separated subset of slugs")
    p.add_argument("--max-ligands", type=int, default=100,
                   help="Cap distinct poses per target's session (default 100)")
    p.add_argument("--max-structures", type=int, default=None,
                   help="Hard cap on structures processed per target")
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

    rows: list[tuple] = []   # (target, TargetResult|None, AlignTargetResult)

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
        out = sitefilter.align_target(tr, site, http_cfg, max_ligands=args.max_ligands,
                                      max_structures=args.max_structures, progress=bar)
        if bar is not None:
            bar.close()

        if out.reference is None:
            print(f"[{t.slug}] FAILED to build site reference — skipping", flush=True)
            rows.append((t, tr, out))
            continue

        arts = visualize.build_session(out, make_pse=not args.no_pse)
        dropped = {k: v for k, v in out.status_counts.items()
                   if k not in ("kept", "symmetry_dup")}
        print(f"[{t.slug}] {out.n_kept} poses in session "
              f"({out.n_at_site} at-site incl. symmetry) from "
              f"{out.structures_processed}/{out.structures_total} structures"
              f"{' [capped]' if out.capped else ''} | dropped {dropped} | "
              f"{', '.join(k + '=' + str(p) for k, p in arts.items())}", flush=True)
        rows.append((t, tr, out))

    if rows and not args.sessions_only:
        path = _write_run_summary(rows, date.today().isoformat(), args.max_ligands)
        print(f"\nRun summary: {path}", flush=True)
    return 0


def _write_run_summary(rows: list[tuple], search_date: str, max_ligands: int) -> Path:
    lines = [
        f"# Run summary — {search_date}",
        "",
        "Two-stage pipeline. **Stage 1** scrapes every ligand-bound PDB structure "
        "mapped to each verified UniProt accession and curates the bound ligands "
        "(drop additives/buffers/cryo/waters; keep cofactors; flag metals). "
        "**Stage 2** keeps only ligands bound at the *relevant site* of each model "
        "system, superposes their poses into one reference frame (binding-site-local "
        "fit), and writes a PyMOL session for comparison.",
        "",
        "## Stage 1 — scrape & curate",
        "",
        "| Target | Primary acc | Structures | Uniq kept | Excl HET | Flagged |",
        "|--------|-------------|-----------:|----------:|---------:|--------:|",
    ]
    for t, tr, _ in rows:
        if tr is None:
            continue
        n_struct = len({h.pdb_id for h in tr.hits})
        acc = ",".join(tr.resolved.primary_accessions()) or "—"
        lines.append(
            f"| {t.name[:34]} | {acc} | {n_struct} | "
            f"{len(tr.curation.kept_het_codes())} | "
            f"{len(tr.curation.excluded_het_codes())} | "
            f"{len(tr.curation.flagged_het_codes())} |")

    lines += [
        "",
        "## Stage 2 — site filtering & alignment",
        "",
        f"Poses per session capped at **{max_ligands}** (best-resolution first). "
        "Symmetry-equivalent copies of a ligand within a structure are collapsed to "
        "one representative pose. `off-site` = correct location test failed (wrong "
        "site/cofactor/lipid); `other` = no matching pocket / unavailable "
        "(`poor_fit`, `no_pocket`, `not_found`, `align_error`).",
        "",
        "| Target | Ref | Anchor | Structs (proc/total) | Poses in .pse | At-site | Off-site | Other | Capped |",  # noqa: E501
        "|--------|-----|--------|---------------------|--------------:|--------:|---------:|------:|:------:|",  # noqa: E501
    ]
    for t, _, out in rows:
        if out.reference is None:
            lines.append(f"| {t.slug} | {out.site.reference_pdb} | {out.site.anchor_het} "
                         f"| — | reference failed | — | — | — | — |")
            continue
        off = out.status_counts.get("off_site", 0)
        other = sum(out.status_counts.get(k, 0) for k in _OTHER_DROPPED)
        lines.append(
            f"| {t.slug} | {out.site.reference_pdb} | {out.site.anchor_het} | "
            f"{out.structures_processed}/{out.structures_total} | {out.n_kept} | "
            f"{out.n_at_site} | {off} | {other} | "
            f"{'yes' if out.capped else '—'} |")

    lines += [
        "",
        "Per-target detail: `catalogue/<slug>/site_filter.csv` (every instance, its "
        "status, distance-to-anchor and pocket RMSD) and the session "
        "`catalogue/<slug>/<slug>_aligned.pse`.",
        "",
    ]
    path = ensure_dir(CATALOGUE_DIR) / "run_summary.md"
    path.write_text("\n".join(lines), encoding="utf-8")
    return path


if __name__ == "__main__":
    raise SystemExit(main())
