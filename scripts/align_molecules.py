#!/usr/bin/env python
"""Tool 1 — **molecule alignment**.

Align a set of molecules to each other by their pharmacophoric features (no protein needed) and
write the aligned molecules out. Input is either a **DrugCLIP output CSV** (a rank index with
``mol_id,…,smiles,…,drugclip_score`` columns) or a **multi-molecule SDF**; the tool embeds a
conformer ensemble per molecule and iteratively superposes them on their shared features
(feature-clique matching on relative intramolecular distances → EM refinement → directional
matching), seedless by default.

    pixi run align-molecules --input hits.csv|mols.sdf --out DIR [--top-n 50] [--seed frame.sdf]

Output (in ``--out``): ``aligned_compounds.sdf`` (the aligned molecules, best conformer each),
``aligned_points.csv`` (pooled feature points), ``alignment_manifest.csv`` (per-mol provenance).
Feed ``aligned_compounds.sdf`` to ``build-pharmacophore``. Methodology: docs/molecule_alignment.md.
"""

from __future__ import annotations

import argparse
import csv
import logging
import os
import sys
import tempfile
from pathlib import Path

os.environ.setdefault("OMP_NUM_THREADS", "1")
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from rdkit import Chem, RDLogger  # noqa: E402

RDLogger.DisableLog("rdApp.*")

from pharmpipe.pharmacophore.config import load_pharmacophore_config  # noqa: E402
from pharmpipe.pharmacophore.run import build_from_seed_alignment  # noqa: E402

log = logging.getLogger("align_molecules")

INDEX_COLUMNS = ["entity_id", "mol_id", "library_name", "smiles", "drugclip_score",
                 "vina_docking_score"]


def _index_from_sdf(sdf: Path, dest_dir: Path) -> Path:
    """Derive a rank-index CSV (mol_id,smiles) from a multi-molecule SDF, so the SDF path reuses
    the same alignment core as a DrugCLIP CSV. Molecule order = rank; id = title or ``mol<i>``."""
    index = dest_dir / "index_input.csv"
    with index.open("w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(INDEX_COLUMNS)
        for i, mol in enumerate(Chem.SDMolSupplier(str(sdf), removeHs=True)):
            if mol is None:
                continue
            name = mol.GetProp("_Name").strip() if mol.HasProp("_Name") else ""
            mol_id = name or f"mol{i}"
            # score column left blank -> read_rank_index keeps input order (stable rank)
            w.writerow(["", mol_id, "input", Chem.MolToSmiles(mol), "", ""])
    return index


def _resolve_input(inp: Path, tmp: Path) -> tuple[Path, Path]:
    """Return (docked_dir, index_csv) for the alignment core, from a CSV or an SDF input."""
    if inp.suffix.lower() in (".sdf", ".mol"):
        index = _index_from_sdf(inp, tmp)
        return tmp, index
    # a DrugCLIP CSV: the file itself is the index; its directory may hold docked SDFs (for --seed)
    return inp.parent, inp


def main(argv=None) -> int:
    logging.basicConfig(level=logging.WARNING, format="%(levelname)s %(message)s")
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--input", type=Path, required=True,
                    help="a DrugCLIP output CSV or a multi-molecule SDF")
    ap.add_argument("--out", type=Path, required=True, help="output directory")
    ap.add_argument("--top-n", dest="top_n", type=int, default=50,
                    help="align the top-N molecules (by score for a CSV; default 50 — the depth "
                         "that best matched the known-actives models; >=100 dilutes)")
    ap.add_argument("--seed", type=Path, default=None,
                    help="optional 3D seed (a holo co-crystal ligand; .sdf or .mol2). It anchors "
                         "the alignment frame through the growing pass, then is dropped before the "
                         "EM refinement so the model reflects the aligned molecules alone "
                         "(best-performing seed mode). If given in a protein's coordinates the "
                         "output is positioned in that binding site. Default: seedless.")
    ap.add_argument("--config", type=Path, default=None)
    args = ap.parse_args(argv)

    cfg = load_pharmacophore_config(args.config)
    args.out.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory() as td:
        docked_dir, index = _resolve_input(args.input.resolve(), Path(td))
        res = build_from_seed_alignment(
            docked_dir, index, args.out.resolve(), cfg, top_n_hits=args.top_n,
            seed_k=cfg.alignment.seed_k, name=args.out.name,
            seed_poses=args.seed.resolve() if args.seed else None,
            seedless=args.seed is None, align_only=True)
    if res is None:
        print("align-molecules: nothing aligned (no molecules loaded, or none shared enough "
              "features to align)")
        return 1
    print(f"aligned {res.name} -> {args.out} "
          f"(aligned_compounds.sdf, aligned_points.csv, alignment_manifest.csv)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
