#!/usr/bin/env python
"""Tool 2 — **pharmacophore construction**.

Build a consensus pharmacophore from a set of **aligned molecules**: either the
``aligned_compounds.sdf`` produced by ``align-molecules``, or a directory of aligned crystal
``*.mol2`` poses. The molecules must already be superposed into one common frame. Features are
perceived (pH-7.4 microstate for mol2 via the ``prep`` env), then a molecule-weighted Gaussian-KDE
occupancy field is peaked and support-filtered into consensus features. Purely ligand-based — no
receptor, no excluded volume.

    pixi run build-pharmacophore --input aligned_compounds.sdf|mol2_dir --out DIR [--smiles het.csv]

Output (in ``--out``): **``pharmacophore.csv``** (the downstream interchange, one row per feature),
``pharmacophore.json`` (canonical), ``model_summary.md``, ``features.csv`` (raw points),
``representative_ligand.sdf``, per-family PNGs. Feed ``pharmacophore.csv`` to
``visualise-pharmacophore``. Methodology: docs/pharmacophore_construction.md.
"""

from __future__ import annotations

import argparse
import logging
import os
import sys
from datetime import date
from pathlib import Path

os.environ.setdefault("OMP_NUM_THREADS", "1")
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from rdkit import Chem, RDLogger  # noqa: E402

RDLogger.DisableLog("rdApp.*")

from pharmpipe.features.load import LoadReport, read_smiles_map  # noqa: E402
from pharmpipe.pharmacophore.config import load_pharmacophore_config  # noqa: E402
from pharmpipe.pharmacophore.run import (  # noqa: E402
    build_from_directory,
    build_from_molecules,
)

log = logging.getLogger("build_pharmacophore")


def _from_sdf(sdf: Path, out: Path, cfg, name: str):
    """Build from an SDF of aligned molecules (bonds/coords intact — perceived directly)."""
    molecules = []
    report = LoadReport()
    for mol in Chem.SDMolSupplier(str(sdf), removeHs=True):
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
                    help="aligned molecules: an SDF (from align-molecules) or a dir of aligned "
                         "mol2")
    ap.add_argument("--out", type=Path, required=True, help="output directory")
    ap.add_argument("--smiles", type=Path, default=None,
                    help="het_code,smiles CSV — required for a directory of heavy-atom mol2 "
                         "(bond orders + pH-7.4 protonation); not needed for an SDF")
    ap.add_argument("--config", type=Path, default=None)
    args = ap.parse_args(argv)

    cfg = load_pharmacophore_config(args.config)
    inp = args.input.resolve()
    out = args.out.resolve()
    out.mkdir(parents=True, exist_ok=True)
    name = out.name

    if inp.is_dir():
        smiles_map = read_smiles_map(args.smiles.resolve()) if args.smiles else {}
        res = build_from_directory(inp, out, cfg, smiles_map=smiles_map, name=name)
    elif inp.suffix.lower() == ".sdf":
        res = _from_sdf(inp, out, cfg, name)
    else:
        ap.error("--input must be an .sdf of aligned molecules or a directory of aligned *.mol2")

    if res is None:
        print(f"build-pharmacophore: too few molecules (< {cfg.selection.min_ligands}) — skipped")
        return 1
    n_feat = len(res.pharmacophore.features)
    print(f"{res.name}: {n_feat} features -> {out}/pharmacophore.csv (+ .json, model_summary.md)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
