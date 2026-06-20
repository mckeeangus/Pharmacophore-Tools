#!/usr/bin/env python
"""Diagnostic: measure binding-site overlay quality of the current alignment.

For each kept pose we recompute the alignment transform (via the live align
module) and report two RMSDs over reference pocket Calpha that have a candidate
partner within `match_distance`:

  * broad_rmsd  — all paired pocket Calpha inside `pocket_shell` (what site_filter
                  currently reports);
  * inner_rmsd  — only paired Calpha within INNER of the anchor centroid, i.e.
                  the residues that actually line the binding site.

`inner_rmsd` is the number the pharmacophore cares about ("nearby residue geometry
kept constant"). Split by native vs surrogate (per_structure.csv `mapping`).
OFFLINE — uses cached mmCIF in data/targets/<slug>/structures.
"""

from __future__ import annotations

import argparse
import csv
import statistics
import sys
from pathlib import Path

import gemmi

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from pharmpipe.pdb.rcsb import LigandInstance  # noqa: E402
from pharmpipe.sites import align  # noqa: E402
from pharmpipe.sites.config import load_sites  # noqa: E402
from pharmpipe.util.paths import target_catalogue_dir, target_structures_dir  # noqa: E402

INNER = 8.0


def _mapping(slug: str) -> dict[str, str]:
    path = target_catalogue_dir(slug) / "per_structure.csv"
    out: dict[str, str] = {}
    if path.exists():
        for r in csv.DictReader(path.open(encoding="utf-8")):
            out[r["pdb_id"].upper()] = r.get("mapping", "")
    return out


def _rmsd(pairs: list[tuple[gemmi.Position, gemmi.Position]]) -> float | None:
    if not pairs:
        return None
    return (sum(a.dist(b) ** 2 for a, b in pairs) / len(pairs)) ** 0.5


def _read(slug: str, pdb: str) -> gemmi.Structure | None:
    p = target_structures_dir(slug) / f"{pdb}.cif"
    return gemmi.read_structure(str(p)) if p.exists() else None


def diagnose(slug: str, site) -> dict | None:
    ref_st = _read(slug, site.reference_pdb)
    if ref_st is None:
        return None
    ref = align.build_reference(ref_st, site)
    if ref is None:
        return None
    mapping = _mapping(slug)
    sf = target_catalogue_dir(slug) / "site_filter.csv"
    rows = list(csv.DictReader(sf.open(encoding="utf-8")))
    inner_by: dict[str, list[float]] = {"native": [], "surrogate": []}
    broad_by: dict[str, list[float]] = {"native": [], "surrogate": []}
    cache: dict[str, gemmi.Structure] = {}
    for r in rows:
        if r["status"] != "kept":
            continue
        pdb = r["pdb_id"].upper()
        st = cache.get(pdb)
        if st is None:
            st = _read(slug, pdb)
            if st is None:
                continue
            cache[pdb] = st
        inst = LigandInstance(pdb_id=pdb, comp_id=r["het_code"],
                              auth_asym_id=r["chain"], auth_seq_id=str(r["seqid"]))
        a = align.align_instance(st, inst, ref)
        if not a.kept or a.transform is None:
            continue
        moved = [align._apply(a.transform, rr.get_ca().pos)
                 for chain in st[0] for rr in chain.get_polymer()
                 if rr.get_ca() is not None]
        broad, inner = [], []
        for pc in ref.pocket:
            d = min((pc.pos.dist(m) for m in moved), default=1e9)
            if d <= site.match_distance_angstrom:
                # nearest moved candidate Calpha to this pocket residue
                m = min(moved, key=lambda q: pc.pos.dist(q))
                broad.append((pc.pos, m))
                if pc.pos.dist(ref.anchor_centroid) <= INNER:
                    inner.append((pc.pos, m))
        grp = "surrogate" if mapping.get(pdb) == "surrogate" else "native"
        if (v := _rmsd(inner)) is not None:
            inner_by[grp].append(v)
        if (v := _rmsd(broad)) is not None:
            broad_by[grp].append(v)
    return {"inner": inner_by, "broad": broad_by}


def _fmt(vals: list[float]) -> str:
    if not vals:
        return "n=0"
    return (f"n={len(vals):3d} median={statistics.median(vals):.2f} "
            f"mean={statistics.mean(vals):.2f} max={max(vals):.2f} "
            f"p90={sorted(vals)[max(0, int(0.9 * len(vals)) - 1)]:.2f}")


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--targets", default="")
    ap.add_argument("--sigma", type=float, default=None, help="override anchor_weight_sigma")
    ap.add_argument("--iters", type=int, default=None, help="override refine_iterations")
    ap.add_argument("--no-backbone", action="store_true", help="fit on CA only")
    args = ap.parse_args(argv)
    sites = load_sites(Path("config/sites.yaml"))
    slugs = [s.strip() for s in args.targets.split(",") if s.strip()] or list(sites.sites)
    print(f"{'target':14s} {'group':9s} inner-site Calpha RMSD                  broad pocket RMSD")
    for slug in slugs:
        site = sites.get(slug)
        if site is None:
            continue
        if args.sigma is not None:
            site.anchor_weight_sigma_angstrom = args.sigma
        if args.iters is not None:
            site.refine_iterations = args.iters
        if args.no_backbone:
            site.use_backbone = False
        d = diagnose(slug, site)
        if d is None:
            print(f"{slug:14s} (no cached data)")
            continue
        for grp in ("native", "surrogate"):
            iv, bv = d["inner"][grp], d["broad"][grp]
            if iv or bv:
                print(f"{slug:14s} {grp:9s} {_fmt(iv):40s} {_fmt(bv)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
