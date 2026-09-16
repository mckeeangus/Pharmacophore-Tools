"""Load a DrugCLIP -> GNINA docked screening set as an aligned active set (Stage 4, IO edge).

Input is a directory of GNINA ``<mol_id>_docked.sdf`` files (each ONE compound with several
docked poses, poses already in GNINA rank order within the file) plus a DrugCLIP rank index
CSV (``entity_id,mol_id,library_name,smiles,drugclip_score,vina_docking_score``). The
compounds are all docked into the same receptor frame, so the poses are already mutually
aligned — exactly the contract the density builder expects, no superposition step needed.

Unlike the catalogue mol2 (heavy-atom-only, needing a SMILES template to recover bonds),
the docked SDFs already carry bond orders **and** a per-record ``protonated_smiles`` (the
pH-7.4 microstate fixed at docking prep). So there is no protonation subprocess here: we
assign bond orders/charges from that embedded template onto each pose exactly as the mol2
loader does — giving ionisation-correct donor/acceptor/ionizable perception — and fall back
to a direct sanitized read of the record, then skip (recording the reason).

Selection is rank-driven:

* ``top_n_hits`` — take this many compounds, highest ``drugclip_score`` first.
* ``top_n_poses`` — for each compound take this many poses (default 1), chosen by **binding
  quality** (``pose_score``, default ``cnnaffinity``; optional ``max_vina`` clash filter),
  **not** the raw SDF order. GNINA writes poses in ``CNNscore`` order, but ``CNNscore`` ranks
  physically-clashing poses highly (poses ≥3 are majority Vina-positive), which scatters the
  ensemble — so ``CNNaffinity`` / ``minimizedAffinity`` pick better poses (see the method doc).

Each pose is loaded as an **independent observation** with ligand_id ``<mol_id>__p<k>``.
This matters because the density builder keys molecule-weighting and support on ligand_id:
with the default one pose per hit, the unit of evidence is the compound; taking >1 pose lets
a compound's alternative placements count as separate observations (documented in the model's
source metadata and ``docked_manifest.csv`` so the choice is never hidden).
"""

from __future__ import annotations

import csv
import logging
import math
from dataclasses import dataclass
from pathlib import Path

from rdkit import Chem
from rdkit.Chem import AllChem

from .load import LoadReport, _connectivity_only

log = logging.getLogger("pharmpipe.features.dock_load")

DOCKED_SUFFIX = "_docked.sdf"


@dataclass(frozen=True)
class DockHit:
    """One ranked compound from the DrugCLIP index."""

    mol_id: str
    rank: int          # 1-based rank by score (1 = best)
    score: float
    smiles: str        # index-level SMILES (fallback template)


@dataclass(frozen=True)
class PoseRecord:
    """Provenance for one loaded pose (one row of ``docked_manifest.csv``)."""

    ligand_id: str        # <mol_id>__p<gnina_rank>
    mol_id: str
    rank: int             # the compound's DrugCLIP rank
    gnina_rank: int       # 1-based pose index within the SDF (GNINA CNNscore order)
    selected_rank: int    # 1-based order after the quality selection
    score: float          # the compound's DrugCLIP score
    pose_metric: str      # the per-pose score poses were selected by
    pose_value: float     # this pose's value of that metric
    method: str           # template | direct


# Per-pose GNINA scores usable to select poses by binding quality. Each maps to the
# SDF tag and whether a HIGHER value is better (GNINA writes poses in CNNscore order,
# but CNNscore ranks physically-clashing poses highly — CNNaffinity / minimizedAffinity
# discriminate quality better).
POSE_METRICS: dict[str, tuple[str, bool]] = {
    "cnnscore":    ("CNNscore", True),           # pose-quality classifier [0,1], higher better
    "cnnaffinity": ("CNNaffinity", True),        # predicted pK, higher better
    "cnn_vs":      ("CNN_VS", True),             # CNNscore x CNNaffinity, higher better
    "vina":        ("minimizedAffinity", False),  # kcal/mol, LOWER (more negative) better
}


def _parse_score(raw: str | None) -> float:
    """Index score as a float; a blank/unparseable cell sorts last (-inf)."""
    try:
        return float(raw) if raw not in (None, "") else float("-inf")
    except (TypeError, ValueError):
        return float("-inf")


def read_rank_index(index_csv: Path, score_column: str = "drugclip_score") -> list[DockHit]:
    """Read the DrugCLIP index into ``DockHit``s ranked by ``score_column`` (desc).

    The sort is stable, so ties keep the file's own order; rank is 1-based over the sorted
    list. Rows without a ``mol_id`` are skipped.
    """
    rows: list[tuple[str, float, str]] = []
    with index_csv.open(encoding="utf-8") as fh:
        for row in csv.DictReader(fh):
            mol_id = (row.get("mol_id") or "").strip()
            if not mol_id:
                continue
            rows.append((mol_id, _parse_score(row.get(score_column)),
                         (row.get("smiles") or "").strip()))
    rows.sort(key=lambda r: r[1], reverse=True)  # stable: ties keep input order
    return [DockHit(mol_id=m, rank=i, score=s, smiles=smi)
            for i, (m, s, smi) in enumerate(rows, start=1)]


def _record_smiles(raw: Chem.Mol, fallback: str | None) -> str | None:
    """Template SMILES for a pose: its own pH-7.4 microstate, else neutral, else index."""
    for tag in ("protonated_smiles", "original_smiles"):
        if raw.HasProp(tag):
            smi = raw.GetProp(tag).strip()
            if smi:
                return smi
    return fallback or None


def read_protonated_smiles(docked_dir: Path, mol_id: str) -> str | None:
    """A compound's pH-7.4 ``protonated_smiles`` from its docked SDF (first record), or None.

    Lets the seed-alignment build reuse the microstate fixed at docking prep for compounds
    that happen to be docked — offline, no prep-env round-trip.
    """
    sdf = docked_dir / f"{mol_id}{DOCKED_SUFFIX}"
    if not sdf.exists():
        return None
    for raw in Chem.SDMolSupplier(str(sdf), sanitize=False, removeHs=True):
        return None if raw is None else _record_smiles(raw, None)
    return None


def _pose_from_record(raw: Chem.Mol, smiles: str | None) -> tuple[Chem.Mol | None, str]:
    """Return ``(mol, method)`` for one SDF record; method is ``template`` | ``direct`` | ``fail``.

    Mirrors ``load.load_pose`` but works on an in-memory record (which already carries a 3D
    conformer and bond orders): prefer transferring the template's bond orders/charges,
    fall back to a direct sanitize of the record.
    """
    if smiles:
        ref = Chem.MolFromSmiles(smiles)
        if ref is not None:
            try:
                mol = AllChem.AssignBondOrdersFromTemplate(ref, _connectivity_only(raw))
                Chem.SanitizeMol(mol)
                return mol, "template"
            except Exception:  # noqa: BLE001 — fall through to the direct read
                pass
    try:
        mol = Chem.Mol(raw)
        Chem.SanitizeMol(mol)
        return mol, "direct"
    except Exception:  # noqa: BLE001
        return None, "fail"


def _pose_value(raw: Chem.Mol, tag: str) -> float:
    """A per-pose GNINA score off an SDF tag; NaN when absent/unparseable."""
    if raw.HasProp(tag):
        try:
            return float(raw.GetProp(tag))
        except (TypeError, ValueError):
            return math.nan
    return math.nan


def _select_poses(raws: list[tuple[int, Chem.Mol]], pose_score: str, top_n_poses: int,
                  max_vina: float | None) -> list[tuple[int, Chem.Mol, float]]:
    """Choose the best ``top_n_poses`` records of one compound by binding quality.

    ``raws`` is ``(gnina_rank, record)`` in SDF (CNNscore) order. Optionally drops poses whose
    Vina ``minimizedAffinity`` exceeds ``max_vina`` (a clash filter), then ranks the rest by
    ``pose_score`` (``POSE_METRICS``) and returns ``(gnina_rank, record, metric_value)`` for the
    top ``top_n_poses``. NaN metric values sort last, and the SDF order breaks ties (stable).
    """
    tag, higher_better = POSE_METRICS[pose_score]
    scored = [(gr, raw, _pose_value(raw, tag)) for gr, raw in raws]
    if max_vina is not None:
        vina_tag = POSE_METRICS["vina"][0]
        scored = [t for t in scored
                  if not (_pose_value(t[1], vina_tag) > max_vina)]  # keep NaN (unknown) poses

    def key(t: tuple[int, Chem.Mol, float]) -> float:
        if math.isnan(t[2]):
            return -math.inf if higher_better else math.inf
        return t[2]

    scored.sort(key=key, reverse=higher_better)  # stable: ties keep SDF order
    return scored[:max(top_n_poses, 0)]


def load_docked_set(
    docked_dir: Path, index_csv: Path, top_n_hits: int, top_n_poses: int = 1,
    score_column: str = "drugclip_score", pose_score: str = "cnnaffinity",
    max_vina: float | None = None,
) -> tuple[list[tuple[str, Chem.Mol]], LoadReport, list[PoseRecord]]:
    """Load the top-``top_n_hits`` compounds (best ``top_n_poses`` poses each) as poses.

    Compounds are taken in ``score_column`` (DrugCLIP) rank order. Within each compound the
    poses are selected by **binding quality** — ranked by ``pose_score`` (one of
    ``POSE_METRICS``: ``cnnaffinity`` default, ``cnnscore``, ``cnn_vs``, ``vina``) after an
    optional ``max_vina`` clash filter — rather than the raw SDF (CNNscore) order, because
    CNNscore ranks physically-clashing poses highly. Returns ``(molecules, report, manifest)``;
    ``ligand_id`` is ``<mol_id>__p<gnina_rank>`` so it always points at a specific SDF pose.
    A ranked compound whose SDF is missing is recorded (``no_sdf``) and skipped.
    """
    if pose_score not in POSE_METRICS:
        raise ValueError(f"pose_score must be one of {sorted(POSE_METRICS)}; got {pose_score!r}")
    hits = read_rank_index(index_csv, score_column)[:max(top_n_hits, 0)]
    molecules: list[tuple[str, Chem.Mol]] = []
    report = LoadReport()
    manifest: list[PoseRecord] = []
    for hit in hits:
        sdf = docked_dir / f"{hit.mol_id}{DOCKED_SUFFIX}"
        if not sdf.exists():
            report.skip(hit.mol_id, "no_sdf")
            log.warning("no docked SDF for ranked compound %s", hit.mol_id)
            continue
        raws = [(gr, raw) for gr, raw
                in enumerate(Chem.SDMolSupplier(str(sdf), sanitize=False, removeHs=True), 1)
                if raw is not None]
        for selected_rank, (gnina_rank, raw, value) in enumerate(
                _select_poses(raws, pose_score, top_n_poses, max_vina), start=1):
            ligand_id = f"{hit.mol_id}__p{gnina_rank}"
            mol, method = _pose_from_record(raw, _record_smiles(raw, hit.smiles))
            if mol is None:
                report.skip(ligand_id, method)
                continue
            report.record(method)
            molecules.append((ligand_id, mol))
            manifest.append(PoseRecord(ligand_id, hit.mol_id, hit.rank, gnina_rank,
                                       selected_rank, hit.score, pose_score, value, method))
    return molecules, report, manifest


def write_manifest(manifest: list[PoseRecord], path: Path) -> Path:
    """Write the per-pose provenance (rank, pose, scores, load method) to ``path``."""
    with path.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.writer(fh)
        writer.writerow(["ligand_id", "mol_id", "drugclip_rank", "gnina_rank",
                         "selected_rank", "drugclip_score", "pose_metric", "pose_value",
                         "method"])
        for r in manifest:
            score = "" if r.score == float("-inf") else f"{r.score:g}"
            value = "" if math.isnan(r.pose_value) else f"{r.pose_value:g}"
            writer.writerow([r.ligand_id, r.mol_id, r.rank, r.gnina_rank, r.selected_rank,
                             score, r.pose_metric, value, r.method])
    return path
