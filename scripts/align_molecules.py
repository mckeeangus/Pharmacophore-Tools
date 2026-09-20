#!/usr/bin/env python
"""Tool 1 — molecule alignment. See README.md / docs/molecule_alignment.md.

    pixi run align-molecules --input hits.csv|mols.sdf --out DIR [--top-n 50] [--seed frame.sdf]
                             [--pkasolver]
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
    recs: list[tuple[str, str, str]] = []
    for i, mol in enumerate(Chem.SDMolSupplier(str(sdf), removeHs=True)):
        if mol is None:
            continue
        name = mol.GetProp("_Name").strip() if mol.HasProp("_Name") else ""
        # score column left blank -> read_rank_index keeps input order (stable rank)
        recs.append((name or f"mol{i}", Chem.MolToSmiles(mol), ""))
    with index.open("w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(INDEX_COLUMNS)
        for mol_id, smi, sc in _dedup_by_smiles(recs):
            w.writerow(["", mol_id, "input", smi, sc, ""])
    return index


def _looks_like_header(fields: list[str]) -> bool:
    """True if a row looks like a header (names a smiles/mol_id column) rather than data."""
    low = {f.strip().lower() for f in fields}
    return bool(low & {"smiles", "smi", "mol_id"})


def _dedup_by_smiles(recs: list[tuple[str, str, str]]) -> list[tuple[str, str, str]]:
    """Drop duplicate molecules from ``(mol_id, smiles, score)`` records, keyed by canonical SMILES.

    A screen merged across libraries repeats the same molecule under several vendor ids, which
    would over-weight it in the consensus, so every SMILES is kept once. The retained copy is the
    highest-scoring occurrence (blank score sorts last); order of first appearance is preserved for
    the rest. SMILES RDKit cannot parse are keyed by their raw string, so nothing is silently lost.
    """
    def key(smi: str) -> str:
        m = Chem.MolFromSmiles(smi)
        return Chem.MolToSmiles(m) if m is not None else smi

    def score(sc: str) -> float:
        try:
            return float(sc) if sc not in (None, "") else float("-inf")
        except ValueError:
            return float("-inf")

    best: dict[str, tuple[str, str, str]] = {}
    order: list[str] = []
    for mid, smi, sc in recs:
        if not smi:
            continue
        k = key(smi)
        if k not in best:
            order.append(k)
            best[k] = (mid, smi, sc)
        elif score(sc) > score(best[k][2]):
            best[k] = (mid, smi, sc)
    return [best[k] for k in order]


def _normalise_csv_index(inp: Path, tmp: Path) -> Path:
    """Normalise any tabular input into the canonical rank-index CSV (``INDEX_COLUMNS``).

    Accepts, robustly:
      * a **ranked CSV with a header** — ``smiles`` (or ``smi``) required, ``mol_id`` and a score
        column (``drugclip_score`` or ``score``) optional, in any order;
      * a **header-less** ``smiles,score`` file — e.g. the raw ``retrieval.py`` screen output;
      * a **header-less single-column** SMILES list.
    A ``mol_id`` is generated (``hit1``, ``hit2`` …) when the input has none, so the SMILES alone is
    enough — the id is only a row label. Rows with no SMILES are dropped.
    """
    rows = [r for r in csv.reader(inp.open(encoding="utf-8")) if r and any(c.strip() for c in r)]
    if not rows:
        raise SystemExit(f"align-molecules: no rows in {inp}")

    def col(idx, i):
        return idx[i].strip() if i is not None and i < len(idx) else ""

    if _looks_like_header(rows[0]):
        h = {c.strip().lower(): i for i, c in enumerate(rows[0])}
        smi_i = h.get("smiles", h.get("smi"))
        if smi_i is None:
            raise SystemExit(f"align-molecules: {inp} has a header but no 'smiles' column")
        mid_i, sc_i = h.get("mol_id"), h.get("drugclip_score", h.get("score"))
        recs = [(col(r, mid_i) or f"hit{n}", col(r, smi_i), col(r, sc_i))
                for n, r in enumerate(rows[1:], 1)]
    else:  # header-less: [smiles] or [smiles, score]
        recs = [(f"hit{n}", r[0].strip(), r[1].strip() if len(r) > 1 else "")
                for n, r in enumerate(rows, 1)]

    out = tmp / "index_input.csv"
    with out.open("w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(INDEX_COLUMNS)
        for mid, smi, sc in _dedup_by_smiles(recs):
            w.writerow(["", mid, "input", smi, sc, ""])
    return out


def _resolve_input(inp: Path, tmp: Path) -> tuple[Path, Path]:
    """Return (docked_dir, index_csv) for the alignment core, from a CSV/txt or an SDF input.

    The index is normalised (see ``_normalise_csv_index``) so a header-less ``smiles,score`` screen
    output works as directly as a full ranked CSV. ``docked_dir`` stays the input's own directory so
    any co-located ``<mol_id>_docked.sdf`` (for ``--seed`` / protonation) is still found.
    """
    if inp.suffix.lower() in (".sdf", ".mol"):
        return tmp, _index_from_sdf(inp, tmp)
    return inp.parent, _normalise_csv_index(inp, tmp)


def _protonate_smiles_map(index_csv: Path, top_n: int, tmp: Path) -> dict[str, str]:
    """Protonate the top-N ligands to their pH-7.4 dominant microstate (pkasolver, prep env),
    returning ``{mol_id: protonated_smiles}`` to override the neutral index SMILES."""
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
            "align-molecules: --pkasolver failed. Run `pixi run setup-prep` to provision the "
            "isolated 'prep' env, or omit --pkasolver to align the input SMILES as-is.")
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
    ap.add_argument("--input", type=Path, required=True, help="ranked CSV or multi-molecule SDF")
    ap.add_argument("--out", type=Path, required=True, help="output directory")
    ap.add_argument("--top-n", dest="top_n", type=int, default=50,
                    help="align the top-N molecules (default 50)")
    ap.add_argument("--seed", type=Path, default=None,
                    help="optional 3D seed ligand (.sdf/.mol2); default seedless")
    ap.add_argument("--pkasolver", action="store_true",
                    help="protonate the top-N ligands to pH 7.4 (pkasolver, needs the 'prep' env)")
    ap.add_argument("--config", type=Path, default=None)
    args = ap.parse_args(argv)

    cfg = load_pharmacophore_config(args.config)
    args.out.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory() as td:
        docked_dir, index = _resolve_input(args.input.resolve(), Path(td))
        smiles_map = _protonate_smiles_map(index, args.top_n, Path(td)) if args.pkasolver else None
        res = build_from_seed_alignment(
            docked_dir, index, args.out.resolve(), cfg, top_n_hits=args.top_n,
            seed_k=cfg.alignment.seed_k, name=args.out.name, smiles_map=smiles_map,
            seed_poses=args.seed.resolve() if args.seed else None,
            seedless=args.seed is None, align_only=True)
    if res is None:
        print("align-molecules: nothing aligned (no molecules loaded, or none shared enough "
              "features to align)")
        return 1
    attempted = res.n_aligned + res.n_dropped
    print(f"aligned {res.n_aligned}/{attempted} molecules successfully "
          f"({res.n_dropped} could not be aligned) -> {args.out} "
          f"(aligned_compounds.sdf, aligned_points.csv, alignment_manifest.csv)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
