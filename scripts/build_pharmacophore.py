#!/usr/bin/env python
"""Tool 2 — pharmacophore construction. See README.md / docs/pharmacophore_construction.md.

    pixi run build-pharmacophore --input aligned_compounds.sdf|mol2_dir --out DIR
                                 [--smiles het.csv] [--pkasolver]
"""

from __future__ import annotations

import argparse
import logging
import os
import subprocess
import sys
from datetime import date
from pathlib import Path

os.environ.setdefault("OMP_NUM_THREADS", "1")
REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "src"))

from rdkit import Chem, RDLogger  # noqa: E402

RDLogger.DisableLog("rdApp.*")

from pharmpipe.features.load import (  # noqa: E402
    LoadReport,
    read_protonation_map,
    read_smiles_map,
)
from pharmpipe.pharmacophore.config import load_pharmacophore_config  # noqa: E402
from pharmpipe.pharmacophore.run import (  # noqa: E402
    build_from_directory,
    build_from_molecules,
)

log = logging.getLogger("build_pharmacophore")


def _run_pkasolver(smiles_csv: Path, out_csv: Path) -> None:
    """Shell out to ``pixi run -e prep protonate-ligands`` (incremental: cached HETs are reused)."""
    cmd = ["pixi", "run", "-e", "prep", "protonate-ligands",
           "--input-smiles", str(smiles_csv), "--out", str(out_csv)]
    log.info("protonating %s at pH 7.4 (prep env / pkasolver)...", smiles_csv.name)
    proc = subprocess.run(cmd, cwd=REPO, capture_output=True, text=True)
    if proc.returncode != 0 or not out_csv.exists():
        sys.stderr.write((proc.stdout or "") + "\n" + (proc.stderr or "") + "\n")
        raise SystemExit(
            "build-pharmacophore: --pkasolver failed. Run `pixi run setup-prep` to provision the "
            "isolated 'prep' env, or omit --pkasolver to build from neutral SMILES.")


def _crystal_smiles_map(smiles_csv: Path | None, use_pkasolver: bool) -> dict[str, str]:
    """SMILES for a heavy-atom mol2 directory, with pH-7.4 protonation optionally overlaid."""
    if smiles_csv is None:
        return {}
    smiles_csv = smiles_csv.resolve()
    smiles_map = read_smiles_map(smiles_csv)
    if not use_pkasolver:
        log.warning("pkasolver protonation off (pass --pkasolver) - building from NEUTRAL SMILES")
        return smiles_map
    protonated_csv = smiles_csv.parent / "protonated_ligands.csv"
    _run_pkasolver(smiles_csv, protonated_csv)
    protonated = read_protonation_map(protonated_csv)
    if protonated:
        log.warning("pH-7.4 protonation (pkasolver + weak-acid guard) for %d HETs from %s",
                    len(protonated), protonated_csv.name)
        return {**smiles_map, **protonated}
    log.warning("pkasolver returned no protonation states - building from NEUTRAL SMILES")
    return smiles_map


def _from_sdf(sdf: Path, out: Path, cfg, name: str):
    """Build from an SDF of aligned molecules (bonds/coords intact — perceived directly).

    Hydrogens are kept (``removeHs=False``) so donor D->H orientation vectors can be perceived.
    """
    molecules = []
    report = LoadReport()
    for mol in Chem.SDMolSupplier(str(sdf), removeHs=False):
        if mol is None:
            report.skip("?", "unreadable")
            continue
        lig = mol.GetProp("_Name").strip() if mol.HasProp("_Name") else f"mol{len(molecules)}"
        report.record("sdf")
        molecules.append((lig, mol))
    source = {"input": str(sdf), "n_ligands": len(molecules), "load": report.by_method,
              "created": date.today().isoformat()}
    return build_from_molecules(molecules, report, out, cfg, source=source, name=name)


def main(argv=None) -> int:
    logging.basicConfig(level=logging.WARNING, format="%(levelname)s %(message)s")
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--input", type=Path, required=True,
                    help="aligned SDF, or a directory of aligned mol2")
    ap.add_argument("--out", type=Path, required=True, help="output directory")
    ap.add_argument("--smiles", type=Path, default=None,
                    help="het_code,smiles CSV (required for a mol2 directory)")
    ap.add_argument("--pkasolver", action="store_true",
                    help="protonate --smiles to pH 7.4 (pkasolver, needs the 'prep' env)")
    ap.add_argument("--support-floor", dest="support_floor", type=float, default=None,
                    help="override selection.min_support_fraction (0-1): keep only features "
                         "present in at least this fraction of ligands. Lower it for a "
                         "chemically heterogeneous hit set where a real feature (e.g. a basic "
                         "amine) sits in only a subset of ligands (default: config, 0.5)")
    ap.add_argument("--config", type=Path, default=None)
    args = ap.parse_args(argv)

    cfg = load_pharmacophore_config(args.config)
    if args.support_floor is not None:
        if not 0.0 <= args.support_floor <= 1.0:
            ap.error("--support-floor must be between 0 and 1")
        cfg.selection.min_support_fraction = args.support_floor
    inp = args.input.resolve()
    out = args.out.resolve()
    out.mkdir(parents=True, exist_ok=True)
    name = out.name

    if inp.is_dir():
        smiles_map = _crystal_smiles_map(args.smiles, args.pkasolver)
        res = build_from_directory(inp, out, cfg, smiles_map=smiles_map, name=name)
    elif inp.suffix.lower() == ".sdf":
        res = _from_sdf(inp, out, cfg, name)
    else:
        ap.error("--input must be an .sdf of aligned molecules or a directory of aligned *.mol2")

    if res is None:
        print("build-pharmacophore: no model built (no ligands loaded or no features survived)")
        return 1
    n_feat = len(res.pharmacophore.features)
    print(f"{res.name}: {n_feat} features -> {out}/pharmacophore.csv "
          f"(+ pharmacophore_model.json, model_summary.md)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
