#!/usr/bin/env python
"""Tool 1 — **molecule alignment**.

Align a set of molecules to each other by their pharmacophoric features (no protein needed) and
write the aligned molecules out. Input is either a **ranked CSV** (columns ``mol_id``, ``smiles``,
and optionally a score column such as ``drugclip_score`` — e.g. a virtual-screening output; with no
score column, input order is the rank) or a **multi-molecule SDF**; the tool embeds a conformer
ensemble per molecule and iteratively superposes them on their shared features (feature-clique
matching on relative intramolecular distances -> EM refinement -> directional matching), seedless by
default.

    pixi run align-molecules --input hits.csv|mols.sdf --out DIR [--top-n 50] [--seed frame.sdf]
                             [--protonate]

``--protonate`` sets each aligned ligand to its pH-7.4 dominant microstate (pkasolver, prep env)
before conformers are built — needed for acids (carboxylate etc.); a no-op for amine/base cations,
whose cationic centre RDKit already perceives from the neutral SMILES.

Output (in ``--out``): ``aligned_compounds.sdf`` (the aligned molecules, best conformer each),
``aligned_points.csv`` (pooled feature points), ``alignment_manifest.csv`` (per-mol provenance).
Feed ``aligned_compounds.sdf`` to ``build-pharmacophore``. Methodology: docs/molecule_alignment.md.
"""

from __future__ import annotations

import argparse
import csv
import logging
import os
import subprocess
import sys
import tempfile
from pathlib import Path

os.environ.setdefault("OMP_NUM_THREADS", "1")
REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "src"))

from rdkit import Chem, RDLogger  # noqa: E402

RDLogger.DisableLog("rdApp.*")

from pharmpipe.features.dock_load import read_rank_index  # noqa: E402
from pharmpipe.pharmacophore.config import load_pharmacophore_config  # noqa: E402
from pharmpipe.pharmacophore.run import build_from_seed_alignment  # noqa: E402

log = logging.getLogger("align_molecules")

INDEX_COLUMNS = ["entity_id", "mol_id", "library_name", "smiles", "drugclip_score",
                 "vina_docking_score"]


def _index_from_sdf(sdf: Path, dest_dir: Path) -> Path:
    """Derive a rank-index CSV (mol_id,smiles) from a multi-molecule SDF, so the SDF path reuses
    the same alignment core as a ranked CSV. Molecule order = rank; id = title or ``mol<i>``."""
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
    # a ranked CSV: the file itself is the index; its directory may hold docked SDFs (for --seed)
    return inp.parent, inp


def _protonate_smiles_map(index_csv: Path, top_n: int, tmp: Path) -> dict[str, str]:
    """Protonate the top-N ligands to their pH-7.4 dominant microstate, returning
    ``{mol_id: protonated_smiles}`` to override the neutral index SMILES during alignment.

    Shells out to ``pixi run -e prep protonate-ligands`` (pkasolver): its pinned 2021 stack lives in
    the isolated ``prep`` env, not this one. Molecules with no ionisable site fall back to their
    input SMILES, so the returned map covers every ligand. Only the top-N are protonated (the set
    actually aligned), so the cost is small. Raises ``SystemExit`` with guidance if the step fails.
    """
    hits = read_rank_index(index_csv)[:max(top_n, 0)]
    src = tmp / "to_protonate.csv"
    with src.open("w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["het_code", "smiles"])
        for h in hits:
            w.writerow([h.mol_id, h.smiles])
    out = tmp / "protonated.csv"
    cmd = ["pixi", "run", "-e", "prep", "protonate-ligands",
           "--input-smiles", str(src), "--out", str(out)]
    log.info("protonating %d ligand(s) at pH 7.4 (prep env / pkasolver)...", len(hits))
    proc = subprocess.run(cmd, cwd=REPO, capture_output=True, text=True)
    if proc.returncode != 0 or not out.exists():
        sys.stderr.write((proc.stdout or "") + "\n" + (proc.stderr or "") + "\n")
        raise SystemExit(
            "align-molecules: --protonate failed. It needs the isolated 'prep' env (pkasolver); "
            "check `pixi run -e prep protonate-ligands --help` runs. Omit --protonate to align the "
            "input SMILES as-is (fine for amine/base cations; only acids need protonation).")
    smiles_map: dict[str, str] = {}
    with out.open(encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            het, smi = r.get("het_code"), (r.get("protonated_smiles") or r.get("smiles"))
            if het and smi:
                smiles_map[het] = smi
    log.info("protonation done: %d/%d ligands mapped", len(smiles_map), len(hits))
    return smiles_map


def main(argv=None) -> int:
    logging.basicConfig(level=logging.WARNING, format="%(levelname)s %(message)s")
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--input", type=Path, required=True,
                    help="a ranked CSV (mol_id,smiles[,score]) or a multi-molecule SDF")
    ap.add_argument("--out", type=Path, required=True, help="output directory")
    ap.add_argument("--top-n", dest="top_n", type=int, default=50,
                    help="align the top-N molecules (by the CSV score column; none -> input order; "
                         "default 50 — the depth that benchmarked best; >=100 tends to dilute)")
    ap.add_argument("--seed", type=Path, default=None,
                    help="optional 3D seed (a holo co-crystal ligand; .sdf or .mol2). It anchors "
                         "the alignment frame through the growing pass, then is dropped before the "
                         "EM refinement so the model reflects the aligned molecules alone "
                         "(best-performing seed mode). If given in a protein's coordinates the "
                         "output is positioned in that binding site. Default: seedless.")
    ap.add_argument("--protonate", action="store_true",
                    help="protonate the top-N aligned ligands to their pH-7.4 dominant "
                         "microstate (pkasolver, in the isolated 'prep' env) before "
                         "conformers are built. Off by default: RDKit perceives the "
                         "cationic centre of amine/base ligands in the neutral SMILES "
                         "already; acids (carboxylate, phosphate, tetrazole) need it to "
                         "avoid a spurious donor + extra acceptor. Requires the 'prep' env.")
    ap.add_argument("--config", type=Path, default=None)
    args = ap.parse_args(argv)

    cfg = load_pharmacophore_config(args.config)
    args.out.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory() as td:
        docked_dir, index = _resolve_input(args.input.resolve(), Path(td))
        smiles_map = _protonate_smiles_map(index, args.top_n, Path(td)) if args.protonate else None
        res = build_from_seed_alignment(
            docked_dir, index, args.out.resolve(), cfg, top_n_hits=args.top_n,
            seed_k=cfg.alignment.seed_k, name=args.out.name, smiles_map=smiles_map,
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
