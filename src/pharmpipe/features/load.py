"""Load aligned ligand poses (mol2) into RDKit molecules (Stage 4, IO edge).

Our catalogue mol2 files are heavy-atom-only with Gasteiger charges (written by
OpenBabel). RDKit's direct mol2 reader is lossy on them — it fails to kekulize
aromatic rings and, without explicit hydrogens, misses H-bond donors. So the
loader prefers a **SMILES-template** path: read the mol2 connectivity, reduce it to
a clean single-bond graph, then transfer the correct bond orders from the ligand's
SMILES via ``AssignBondOrdersFromTemplate``. It falls back to a direct sanitized
read, and finally skips (with a recorded reason) — so one bad pose never aborts a
build. SMILES come from the target's ``unique_ligands.csv`` keyed by HET code.
"""

from __future__ import annotations

import csv
import logging
from dataclasses import dataclass, field
from pathlib import Path

from rdkit import Chem
from rdkit.Chem import AllChem

log = logging.getLogger("pharmpipe.features.load")


@dataclass
class LoadReport:
    """Per-pose load outcome, so coverage is auditable."""

    by_method: dict[str, int] = field(default_factory=dict)
    skipped: list[tuple[str, str]] = field(default_factory=list)  # (ligand_id, reason)

    def record(self, method: str) -> None:
        self.by_method[method] = self.by_method.get(method, 0) + 1

    def skip(self, ligand_id: str, reason: str) -> None:
        self.skipped.append((ligand_id, reason))


def het_from_filename(path: Path) -> str | None:
    """Pose files are ``<PDB>_<HET>_<chain><seqid>.mol2`` -> HET is field 2."""
    parts = path.stem.split("_")
    return parts[1] if len(parts) >= 3 else None


def read_smiles_map(unique_ligands_csv: Path) -> dict[str, str]:
    """HET code -> SMILES, from a Stage-1 ``unique_ligands.csv``."""
    out: dict[str, str] = {}
    if not unique_ligands_csv.exists():
        return out
    with unique_ligands_csv.open(encoding="utf-8") as fh:
        for row in csv.DictReader(fh):
            het, smi = row.get("het_code"), row.get("smiles")
            if het and smi:
                out[het] = smi
    return out


def read_protonation_map(protonated_csv: Path) -> dict[str, str]:
    """HET code -> pH-7.4 protonated SMILES, from ``protonated_ligands.csv``.

    Produced by ``scripts/protonate_ligands.py``. Uses the ``protonated_smiles``
    column, falling back per-HET to the neutral ``smiles`` column when protonation was
    unavailable. The template path (``AssignBondOrdersFromTemplate``) carries the
    template's formal charges onto the pose, so a protonated template yields a pose with
    the correct charges/H-count for donor/acceptor/ionizable perception.
    """
    out: dict[str, str] = {}
    if not protonated_csv.exists():
        return out
    with protonated_csv.open(encoding="utf-8") as fh:
        for row in csv.DictReader(fh):
            het = row.get("het_code")
            smi = row.get("protonated_smiles") or row.get("smiles")
            if het and smi:
                out[het] = smi
    return out


def _connectivity_only(raw: Chem.Mol) -> Chem.Mol:
    """Strip bond orders / aromatic + charge flags so a template match is clean."""
    rw = Chem.RWMol(raw)
    for bond in rw.GetBonds():
        bond.SetBondType(Chem.BondType.SINGLE)
        bond.SetIsAromatic(False)
    for atom in rw.GetAtoms():
        atom.SetIsAromatic(False)
        atom.SetFormalCharge(0)
        atom.SetNoImplicit(False)
    return rw.GetMol()


def load_pose(path: Path, smiles: str | None) -> tuple[Chem.Mol | None, str]:
    """Return ``(mol, method)``; method is ``template`` | ``direct`` | ``fail``."""
    if smiles:
        ref = Chem.MolFromSmiles(smiles)
        raw = Chem.MolFromMol2File(str(path), removeHs=True, sanitize=False)
        if ref is not None and raw is not None:
            try:
                mol = AllChem.AssignBondOrdersFromTemplate(ref, _connectivity_only(raw))
                Chem.SanitizeMol(mol)
                return mol, "template"
            except Exception:  # noqa: BLE001 — fall through to the direct reader
                pass
    mol = Chem.MolFromMol2File(str(path), removeHs=False, sanitize=True)
    if mol is not None:
        return mol, "direct"
    return None, "fail"


def load_directory(input_dir: Path, smiles_map: dict[str, str] | None = None,
                   ) -> tuple[list[tuple[str, Chem.Mol]], LoadReport]:
    """Load every ``*.mol2`` in a directory into ``(ligand_id, mol)`` pairs.

    ``smiles_map`` (HET -> SMILES) enables the high-fidelity template path; without
    it the loader uses the direct reader only. ``ligand_id`` is the file stem.
    """
    smiles_map = smiles_map or {}
    molecules: list[tuple[str, Chem.Mol]] = []
    report = LoadReport()
    for path in sorted(input_dir.glob("*.mol2")):
        ligand_id = path.stem
        het = het_from_filename(path)
        mol, method = load_pose(path, smiles_map.get(het or ""))
        if mol is None:
            report.skip(ligand_id, method)
            log.warning("could not load %s", path.name)
            continue
        report.record(method)
        molecules.append((ligand_id, mol))
    return molecules, report
