"""Extract bound-pose ligand instances and write them as mol2 for PyMOL.

We use the *actual deposited instance coordinates* (the bound pose — what matters
for pharmacophore work), NOT the idealised CCD coordinates. Bond orders are
assigned by matching the instance against a template:

  1. the chem-component SMILES (RDKit ``AssignBondOrdersFromTemplate``), else
  2. the CCD ``*_ideal.sdf`` graph, else
  3. OpenBabel geometry-based perception (logged as a fallback).

RDKit cannot write mol2, so the final structure is handed to OpenBabel to emit
the mol2 file.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass
from pathlib import Path

import gemmi
from openbabel import pybel
from rdkit import Chem, RDLogger
from rdkit.Chem import AllChem

from ..pdb.rcsb import LigandInstance
from ..util import http
from ..util.paths import ensure_dir

log = logging.getLogger("pharmpipe.mol2")
# OpenBabel + RDKit are chatty on stderr; quiet them (we log our own fallbacks).
pybel.ob.obErrorLog.SetOutputLevel(0)
RDLogger.DisableLog("rdApp.*")

CCD_IDEAL_URL = "https://files.rcsb.org/ligands/download/{comp_id}_ideal.sdf"


@dataclass
class ExtractResult:
    instance: LigandInstance
    out_path: Path | None
    status: str            # template | ccd | openbabel_fallback | failed
    message: str = ""

    @property
    def ok(self) -> bool:
        return self.status != "failed"


def instance_filename(inst: LigandInstance) -> str:
    chain = inst.auth_asym_id or "_"
    seq = inst.auth_seq_id or "0"
    return f"{inst.pdb_id}_{inst.comp_id}_{chain}{seq}.mol2"


# --- locate the bound residue in the parsed structure --------------------

def find_residue(st: gemmi.Structure, inst: LigandInstance) -> gemmi.Residue | None:
    if len(st) == 0:
        return None
    model = st[0]
    # First pass: match chain + residue number + comp id.
    for chain in model:
        if chain.name != inst.auth_asym_id:
            continue
        for res in chain:
            if res.name == inst.comp_id and str(res.seqid.num) == inst.auth_seq_id:
                return res
    # Fallback: ignore chain id (auth/label mismatches) but keep it unique.
    matches = [res for chain in model for res in chain
               if res.name == inst.comp_id and str(res.seqid.num) == inst.auth_seq_id]
    return matches[0] if len(matches) == 1 else None


# --- minimal PDB block for one residue (relies on the element column) ----

def _hetatm_line(serial: int, atom: gemmi.Atom, resname: str, chain: str,
                 resseq: str) -> str:
    name = atom.name[:4]
    elem = atom.element.name.upper()
    namefield = f" {name:<3}" if len(elem) == 1 and len(name) < 4 else f"{name:<4}"
    pos = atom.pos
    try:
        seq_int = int("".join(c for c in resseq if c.isdigit()) or "0")
    except ValueError:
        seq_int = 0
    return (
        f"HETATM{serial:>5} {namefield}{' '}{resname[:3]:>3} {chain[:1] or 'A'}"
        f"{seq_int:>4}    "
        f"{pos.x:8.3f}{pos.y:8.3f}{pos.z:8.3f}"
        f"{atom.occ:6.2f}{atom.b_iso:6.2f}"
        f"          {elem:>2}  "
    )


def residue_to_pdb_block(res: gemmi.Residue, inst: LigandInstance) -> str:
    lines = []
    serial = 1
    seen_names: set[str] = set()
    for atom in res:
        # Keep the first occurrence per atom name -> a single clean conformer
        # (gemmi marks "no altloc" as '\x00', so we dedupe by name rather than
        # filtering on the altloc letter).
        if atom.name in seen_names:
            continue
        seen_names.add(atom.name)
        lines.append(_hetatm_line(serial, atom, inst.comp_id,
                                  inst.auth_asym_id, inst.auth_seq_id))
        serial += 1
    lines.append("END")
    return "\n".join(lines) + "\n"


# --- templates -----------------------------------------------------------

def _ccd_template(comp_id: str, cfg: http.HttpConfig) -> Chem.Mol | None:
    sdf = http.get_text(CCD_IDEAL_URL.format(comp_id=comp_id), cfg,
                        category="ccd_ideal", cache_key=f"ideal:{comp_id}",
                        allow_404=True)
    if not sdf:
        return None
    mol = Chem.MolFromMolBlock(sdf, sanitize=True)
    return mol


def _write_mol2_from_rdkit(mol: Chem.Mol, title: str, out_path: Path) -> None:
    # The pose carries real 3D coordinates; mark the conformer 3D so OpenBabel
    # doesn't warn about a "2D" molecule with non-zero Z.
    if mol.GetNumConformers():
        mol.GetConformer().Set3D(True)
    molblock = Chem.MolToMolBlock(mol, kekulize=True)
    obmol = pybel.readstring("mol", molblock)
    obmol.title = title
    obmol.write("mol2", str(out_path), overwrite=True)


def _write_mol2_from_pdb(pdb_block: str, title: str, out_path: Path) -> None:
    obmol = pybel.readstring("pdb", pdb_block)
    obmol.title = title
    obmol.write("mol2", str(out_path), overwrite=True)


# --- main entry point ----------------------------------------------------

def extract_instance(st: gemmi.Structure, inst: LigandInstance, out_dir: Path,
                     cfg: http.HttpConfig, smiles: str = "") -> ExtractResult:
    out_path = ensure_dir(out_dir) / instance_filename(inst)
    title = f"{inst.pdb_id}_{inst.comp_id}_{inst.auth_asym_id}{inst.auth_seq_id}"

    res = find_residue(st, inst)
    if res is None:
        return ExtractResult(inst, None, "failed", "residue instance not located")
    pdb_block = residue_to_pdb_block(res, inst)

    rdmol = Chem.MolFromPDBBlock(pdb_block, sanitize=False, proximityBonding=True,
                                 removeHs=False)

    # 1) SMILES template
    if rdmol is not None and smiles:
        template = Chem.MolFromSmiles(smiles)
        if template is not None:
            try:
                fixed = AllChem.AssignBondOrdersFromTemplate(template, rdmol)
                _write_mol2_from_rdkit(fixed, title, out_path)
                return ExtractResult(inst, out_path, "template",
                                     "bond orders from chem-comp SMILES")
            except (ValueError, Chem.AtomValenceException):
                pass

    # 2) CCD ideal-SDF template
    if rdmol is not None:
        ccd = _ccd_template(inst.comp_id, cfg)
        if ccd is not None:
            try:
                fixed = AllChem.AssignBondOrdersFromTemplate(ccd, rdmol)
                _write_mol2_from_rdkit(fixed, title, out_path)
                return ExtractResult(inst, out_path, "ccd",
                                     "bond orders from CCD ideal template")
            except (ValueError, Chem.AtomValenceException):
                pass

    # 3) OpenBabel geometry-based perception (fallback)
    try:
        _write_mol2_from_pdb(pdb_block, title, out_path)
        log.info("OpenBabel fallback for %s", title)
        return ExtractResult(inst, out_path, "openbabel_fallback",
                             "no template matched; OpenBabel perception")
    except Exception as exc:  # noqa: BLE001
        return ExtractResult(inst, None, "failed", f"openbabel error: {exc}")
