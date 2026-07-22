#!/usr/bin/env python
"""Stage 4 CLI: build ensemble pharmacophores from aligned compound sets.

Four modes:

  * single directory  -- one-shot model from any folder of aligned ``*.mol2``:
        pixi run build-pharmacophores --input DIR --out DIR --smiles ligands.csv
  * one target        -- build a model per cell of a catalogue target:
        pixi run build-pharmacophores --target gr_nr3c1
  * whole catalogue   -- every cell of every target:
        pixi run build-pharmacophores --catalogue
  * render sweeps     -- bake the support-sweep .pse for every built model (viz env):
        pixi run build-pharmacophores --render-sweeps

The ``--input`` one-shot runs the whole local methodology end-to-end for one aligned
directory: (A) protonate the ligands to their pH-7.4 microstate via the isolated
``prep`` env (reused if already present in ``--out``), (B) build the model in-process,
(C) bake the kept-model PyMOL ``.pse``/``.png`` **and** the support-sweep
``.pse``/``.png`` via the ``viz`` env. It requires a
``--smiles`` HET->SMILES CSV (the heavy-atom mol2 need it for both protonation and clean
bond perception); ``--reference-pdb`` enables density excluded volume, and
``--force-protonate`` / ``--allow-unprotonated`` / ``--no-render`` tune the steps. It
shells out across pixi envs, so it is local-only.

Catalogue modes only build the ``groups/<pocket>__<efficacy>/`` cells (never the
review tracks separate_state / unknown / quarantine) and write to
``catalogue/<slug>/pharmacophores/<cell>/``. Offline; no protonation subprocess/render
(they consume the pre-built ``protonated_ligands.csv`` and write the ``.pml`` only).
"""

from __future__ import annotations

import argparse
import logging
import os
import shutil
import subprocess
import sys
from pathlib import Path

# One BLAS thread each keeps the numpy field maths reproducible and avoids MKL
# oversubscription (and its Windows memory-leak warning) on Gadi.
os.environ.setdefault("OMP_NUM_THREADS", "1")

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from rdkit import RDLogger  # noqa: E402

# The mol2 loader deliberately falls back when RDKit can't perceive a pose; its
# per-atom kekulize/valence warnings are expected noise, so quiet them here.
RDLogger.DisableLog("rdApp.*")

from pharmpipe.features.load import (  # noqa: E402
    read_protonation_map,
    read_smiles_map,
)
from pharmpipe.pharmacophore.config import load_pharmacophore_config  # noqa: E402
from pharmpipe.pharmacophore.run import (  # noqa: E402
    build_for_cell,
    build_from_directory,
)
from pharmpipe.util.paths import (  # noqa: E402
    CATALOGUE_DIR,
    target_groups_dir,
    target_pharmacophores_dir,
    target_reference_pdb,
)

log = logging.getLogger("build_pharmacophores")

REPO = Path(__file__).resolve().parents[1]


def _pixi() -> str:
    """Locate the ``pixi`` executable (needed to reach the prep/viz envs)."""
    exe = shutil.which("pixi")
    if exe is None:
        raise RuntimeError(
            "pixi not found on PATH; the one-shot needs it to reach the prep/viz envs")
    return exe


def _protonate(smiles_csv: Path, out_csv: Path, force: bool) -> bool:
    """Protonate ``smiles_csv`` -> ``out_csv`` via the isolated ``prep`` env.

    Reuses an existing ``out_csv`` unless ``force`` (protonation is deterministic and
    the slow step). Returns True when the output exists afterwards.
    """
    if out_csv.exists() and not force:
        print(f"  protonation: reusing {out_csv}")
        return True
    cmd = [_pixi(), "run", "-e", "prep", "protonate-ligands",
           "--input-smiles", str(smiles_csv), "--out", str(out_csv)]
    if force:
        cmd.append("--force")
    print(f"  protonation: {' '.join(cmd)}")
    subprocess.run(cmd, cwd=REPO, check=False)
    return out_csv.exists()


def _render(model_dir: Path, name: str, membership_radius: float) -> None:
    """Bake the kept-model ``.pse``/``.png`` **and** the support-sweep ``.pse``/``.png``
    from the model JSON via the ``viz`` env.

    Non-fatal: the model artifacts are already on disk, so a PyMOL failure only warns.
    """
    script = REPO / "scripts" / "pymol_pharmacophore.py"
    cmd = [_pixi(), "run", "-e", "viz", "pymol", "-cq", str(script), "--",
           "--pharmacophore", str(model_dir / "pharmacophore.json"),
           "--out", str(model_dir / f"{name}.pse"),
           "--image", str(model_dir / f"{name}.png"),
           "--sweep-out", str(model_dir / f"{name}_sweep.pse"),
           "--sweep-image", str(model_dir / f"{name}_sweep.png"),
           "--membership-radius", str(membership_radius)]
    print(f"  render: {' '.join(cmd)}")
    result = subprocess.run(cmd, cwd=REPO, check=False)
    if result.returncode != 0:
        log.warning("render failed (exit %d); model artifacts are still written",
                    result.returncode)


def _render_sweep(model_dir: Path, membership_radius: float) -> bool:
    """Bake only the support-sweep ``<cell>_sweep.pse`` for one built model dir.

    The kept-model view stays the offline ``.pml``; this adds the interactive sweep.
    Non-fatal (returns False on failure); needs the ``viz`` env for PyMOL.
    """
    script = REPO / "scripts" / "pymol_pharmacophore.py"
    cmd = [_pixi(), "run", "-e", "viz", "pymol", "-cq", str(script), "--",
           "--pharmacophore", str(model_dir / "pharmacophore.json"),
           "--sweep-out", str(model_dir / f"{model_dir.name}_sweep.pse"),
           "--membership-radius", str(membership_radius)]
    return subprocess.run(cmd, cwd=REPO, check=False).returncode == 0


def _model_dirs() -> list[Path]:
    """Every built catalogue model dir (pharmacophores/) with a JSON + features.csv."""
    dirs: list[Path] = []
    for slug_dir in sorted(p for p in CATALOGUE_DIR.iterdir() if p.is_dir()):
        base = target_pharmacophores_dir(slug_dir.name)
        if not base.is_dir():
            continue
        dirs.extend(sorted(
            cell for cell in base.iterdir()
            if (cell / "pharmacophore.json").exists()
            and (cell / "features.csv").exists()))
    return dirs


def _render_all_sweeps(cfg) -> int:
    """Render the support-sweep ``.pse`` for every built catalogue model."""
    dirs = _model_dirs()
    ok = 0
    for d in dirs:
        print(f"sweep: {d}")
        if _render_sweep(d, cfg.density.membership_radius):
            ok += 1
        else:
            log.warning("sweep render failed for %s", d)
    print(f"\nRendered {ok}/{len(dirs)} support-sweep .pse file(s).")
    return 0 if ok == len(dirs) else 1


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
    ref = target_reference_pdb(slug)
    built = skipped = 0
    for cell in _cells(slug):
        out = target_pharmacophores_dir(slug) / cell.name
        res = build_for_cell(cell, out, cfg, uniq, name=f"{slug}/{cell.name}",
                             reference_pdb=ref)
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


def _one_shot(args, cfg) -> int:
    """Local one-shot for one aligned directory: protonate -> build -> render.

    Assumes ``--input``/``--out``/``--smiles`` are set (validated by the caller). Writes
    every artifact into ``--out``: the protonated map, the model + its CSV/SDF/PML/PNGs +
    ``model_summary.md``, and (unless ``--no-render``) a baked ``.pse`` + ``.png``.
    """
    out = args.out.resolve()
    smiles_csv = args.smiles.resolve()
    out.mkdir(parents=True, exist_ok=True)

    # Step A — protonate to the pH-7.4 microstate (isolated prep env), reuse if cached.
    protonated_csv = out / "protonated_ligands.csv"
    smiles_map = read_smiles_map(smiles_csv)
    if _protonate(smiles_csv, protonated_csv, args.force_protonate):
        smiles_map = {**smiles_map, **read_protonation_map(protonated_csv)}
    elif args.allow_unprotonated:
        log.warning("protonation unavailable; building from neutral SMILES")
    else:
        print("ERROR: protonation failed. Re-run with --allow-unprotonated to build "
              "from neutral SMILES, or check the prep env "
              "(pixi run -e prep protonate-ligands ...).", file=sys.stderr)
        return 1

    # Step B — build the model in-process (writes json/csv/sdf/pml/png/summary).
    res = build_from_directory(args.input, out, cfg, smiles_map=smiles_map,
                               name=args.input.name,
                               reference_pdb=args.reference_pdb)
    if res is None:
        print(f"{args.input.name}: skipped (< {cfg.selection.min_ligands} ligands)")
        return 0

    # Step C — bake the PyMOL session + snapshot (viz env), unless suppressed.
    if not args.no_render:
        _render(out, out.name, cfg.density.membership_radius)

    print(f"{res.name}: {len(res.pharmacophore.features)} features -> {out}")
    return 0


def main(argv=None) -> int:
    logging.basicConfig(level=logging.WARNING, format="%(levelname)s %(message)s")
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    mode = ap.add_mutually_exclusive_group(required=True)
    mode.add_argument("--input", type=Path, help="a single directory of aligned mol2")
    mode.add_argument("--target", help="build every cell of one catalogue target (slug)")
    mode.add_argument("--catalogue", action="store_true", help="every cell of every target")
    mode.add_argument("--render-sweeps", dest="render_sweeps", action="store_true",
                      help="bake the occupancy-sweep .pse for every built catalogue model "
                           "(viz env; run after a --catalogue build)")
    ap.add_argument("--out", type=Path, help="output dir (required with --input)")
    ap.add_argument("--smiles", type=Path,
                    help="HET->SMILES csv (unique_ligands.csv); required with --input")
    ap.add_argument("--reference-pdb", type=Path,
                    help="aligned receptor for density excluded volume (--input)")
    ap.add_argument("--force-protonate", action="store_true",
                    help="recompute protonation even if cached (--input)")
    ap.add_argument("--allow-unprotonated", action="store_true",
                    help="build from neutral SMILES if protonation fails (--input)")
    ap.add_argument("--no-render", action="store_true",
                    help="skip the PyMOL .pse/.png render (--input)")
    ap.add_argument("--config", type=Path, default=None)
    args = ap.parse_args(argv)

    cfg = load_pharmacophore_config(args.config)

    if args.render_sweeps:
        return _render_all_sweeps(cfg)

    if args.input:
        if not args.out:
            ap.error("--out is required with --input")
        if not args.smiles:
            ap.error("--smiles (a het_code,smiles CSV) is required with --input")
        return _one_shot(args, cfg)

    slugs = [args.target] if args.target else _targets()
    total_built = total_skipped = 0
    for slug in slugs:
        print(f"{slug}:")
        built, skipped = _build_target(slug, cfg)
        total_built += built
        total_skipped += skipped
    print(f"\nBuilt {total_built} pharmacophore model(s) across {len(slugs)} target(s); "
          f"{total_skipped} cell(s) skipped (< {cfg.selection.min_ligands} ligands) "
          f"-> catalogue/<slug>/pharmacophores/.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
