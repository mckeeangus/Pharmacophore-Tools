#!/usr/bin/env python
"""Stage-4 prep: protonate catalogue ligands to their dominant microstate at pH 7.4.

For every catalogue target it reads ``catalogue/<slug>/unique_ligands.csv`` (HET ->
neutral SMILES) and writes ``catalogue/<slug>/protonated_ligands.csv`` (HET ->
protonation-state SMILES at pH 7.4). The pharmacophore loader prefers this file, so the
features fed to *both* consensus strategies reflect the ligand's actual ionisation.

pKa values are predicted with **pkasolver** (Mayr et al.; https://github.com/mayrf/
pkasolver) — a graph-NN ensemble — and the dominant microstate at pH 7.4 is selected by
walking the pKa ladder (``pharmpipe.prep.protonate.dominant_microstate_at_ph``). A
ligand with no ionisable site, or that pkasolver cannot process, falls back to its
original SMILES (recorded as such), so a hard case never blocks the batch.

Environment & portability: pkasolver's pretrained GIN checkpoints require its 2021-era
stack (torch 1.11 / torch-geometric 2.0.1 / python 3.10), isolated in the pixi ``prep``
environment. pkasolver itself is vendored as a clone under ``external/pkasolver`` (on
PYTHONPATH here), not installed, so its bundled weights resolve via ``__file__``. This
step is network-heavy at setup time (cloning) — run it on a Gadi login node.

Run:  pixi run protonate-ligands            # all targets
      pixi run protonate-ligands --target drd1
Re-runs are incremental: a HET already present in the output is reused unless --force.
"""

from __future__ import annotations

import argparse
import csv
import logging
import os
import sys
from collections import Counter
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
PKASOLVER = REPO / "external" / "pkasolver"
# Pure helper (RDKit-only) imported by path — pharmpipe is not installed in this 3.10 env.
sys.path.insert(0, str(REPO / "src"))
# Vendored pkasolver clone (see module docstring); holds the bundled model weights.
sys.path.insert(0, str(PKASOLVER))
# pkasolver shells out to a dimorphite-dl subprocess that itself `import pkasolver`, so
# the clone must be on the *environment* PYTHONPATH (sys.path doesn't reach children).
os.environ["PYTHONPATH"] = os.pathsep.join(
    filter(None, [str(PKASOLVER), os.environ.get("PYTHONPATH", "")]))

import yaml  # noqa: E402
from rdkit import Chem, RDLogger  # noqa: E402

RDLogger.DisableLog("rdApp.*")

from pharmpipe.prep.protonate import (  # noqa: E402
    PHYSIOLOGICAL_PH,
    WeakAcidClass,
    largest_fragment,
    neutralize_weak_acids,
    protonated_mol,
    to_smiles,
)

log = logging.getLogger("protonate_ligands")

CATALOGUE = REPO / "catalogue"
CONFIG = REPO / "config" / "protonation.yaml"
OUT_NAME = "protonated_ligands.csv"
FIELDS = ["het_code", "smiles", "protonated_smiles", "ph", "n_pka_sites",
          "pka_values", "guard_neutralized", "method"]


def _load_weak_acid_guard(cfg_path: Path) -> list[WeakAcidClass]:
    """Compile the weak-acid guard classes from config; empty if absent/disabled.

    pkasolver over-deprotonates weak acids on poly-ionizable scaffolds; the guard
    re-protonates them at pH 7.4 unless genuinely acidic (see config/protonation.yaml).
    """
    if not cfg_path.exists():
        return []
    data = (yaml.safe_load(cfg_path.read_text(encoding="utf-8")) or {}).get(
        "weak_acid_guard", {})
    if not data.get("enabled", False):
        return []
    return [
        WeakAcidClass(
            name=cls["name"],
            anion=Chem.MolFromSmarts(cls["anion"]),
            exceptions=tuple(Chem.MolFromSmarts(s) for s in cls.get("exceptions", [])),
        )
        for cls in data.get("classes", [])
    ]


def _targets(slug: str | None) -> list[Path]:
    if slug:
        return [CATALOGUE / slug]
    return sorted(d for d in CATALOGUE.iterdir()
                  if d.is_dir() and (d / "unique_ligands.csv").exists())


def _read_existing(out_csv: Path) -> dict[str, dict]:
    if not out_csv.exists():
        return {}
    with out_csv.open(encoding="utf-8") as fh:
        return {r["het_code"]: r for r in csv.DictReader(fh)}


def _protonate_one(
    smiles: str, query_model, ph: float, guard: list[WeakAcidClass],
) -> tuple[str, int, str, str, str]:
    """Return (protonated_smiles, n_sites, pka_csv, guard_csv, method) for one SMILES."""
    from pkasolver.query import calculate_microstate_pka_values

    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return smiles, 0, "", "", "fallback:unparseable"
    mol = largest_fragment(mol)
    try:
        states = calculate_microstate_pka_values(mol, query_model=query_model)
    except Exception as exc:  # noqa: BLE001 — pkasolver edge cases must not abort the batch
        log.warning("pkasolver failed on %s: %s", smiles, exc)
        return to_smiles(mol), 0, "", "", f"fallback:{type(exc).__name__}"
    if not states:
        return to_smiles(mol), 0, "", "", "pkasolver:no_ionizable"
    prot = protonated_mol(mol, states, ph)
    neutralized: list[tuple[str, int]] = []
    if guard:
        prot, neutralized = neutralize_weak_acids(prot, guard)
    method = "pkasolver+weak_acid_guard" if neutralized else "pkasolver"
    pkas = ";".join(f"{s.pka:.2f}" for s in sorted(states, key=lambda s: s.pka))
    counts = Counter(name for name, _ in neutralized)
    guard_csv = ";".join(f"{cls}:{counts[cls]}" for cls in sorted(counts))
    return to_smiles(prot), len(states), pkas, guard_csv, method


def _process_target(slug_dir: Path, query_model, ph: float, force: bool,
                    guard: list[WeakAcidClass]) -> tuple[int, int]:
    rows_in = list(csv.DictReader((slug_dir / "unique_ligands.csv").open(encoding="utf-8")))
    out_csv = slug_dir / OUT_NAME
    existing = {} if force else _read_existing(out_csv)
    out_rows: list[dict] = []
    changed = reused = 0
    for row in rows_in:
        het, smi = row.get("het_code"), row.get("smiles")
        if not het or not smi:
            continue
        if het in existing and existing[het].get("protonated_smiles"):
            out_rows.append({k: existing[het].get(k, "") for k in FIELDS})
            reused += 1
            continue
        prot, n_sites, pkas, guard_csv, method = _protonate_one(
            smi, query_model, ph, guard)
        out_rows.append({"het_code": het, "smiles": smi, "protonated_smiles": prot,
                         "ph": ph, "n_pka_sites": n_sites, "pka_values": pkas,
                         "guard_neutralized": guard_csv, "method": method})
        changed += 1
        log.info("%s/%s: %s -> %s [%s]", slug_dir.name, het, smi, prot, method)
    with out_csv.open("w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=FIELDS)
        w.writeheader()
        w.writerows(out_rows)
    return changed, reused


def main(argv=None) -> int:
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--target", help="only this catalogue slug (default: all)")
    ap.add_argument("--ph", type=float, default=PHYSIOLOGICAL_PH)
    ap.add_argument("--force", action="store_true", help="recompute even cached HETs")
    args = ap.parse_args(argv)

    from pkasolver.query import QueryModel

    guard = _load_weak_acid_guard(CONFIG)
    log.info("weak-acid guard: %s",
             f"{len(guard)} classes" if guard else "disabled")
    log.info("loading pkasolver model ensemble …")
    query_model = QueryModel()

    total_changed = total_reused = 0
    for slug_dir in _targets(args.target):
        changed, reused = _process_target(slug_dir, query_model, args.ph, args.force,
                                          guard)
        print(f"{slug_dir.name}: {changed} protonated, {reused} reused -> {OUT_NAME}")
        total_changed += changed
        total_reused += reused
    print(f"\nDone: {total_changed} ligand(s) protonated at pH {args.ph}, "
          f"{total_reused} reused from cache.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
