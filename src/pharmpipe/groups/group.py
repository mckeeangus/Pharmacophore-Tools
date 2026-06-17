"""Stage 3 orchestration: verify pockets, annotate efficacy, partition cells.

Pure-ish coordinator — geometry comes from :mod:`pharmpipe.groups.pocket`,
knowledge from the config loaders, and structure IO from the shared helpers. The
output :class:`GroupResult` is everything the report / session writers need.

A *cell* is ``(verified pocket) x (efficacy sign)``: the unit a single
pharmacophore hypothesis will later be built from. Stage 3 produces cells and
stops; it does not cluster within them or build models.
"""

from __future__ import annotations

import csv
import json
import logging
from collections import Counter, defaultdict
from dataclasses import dataclass, field
from pathlib import Path

from ..io import mol2, structures
from ..pdb.rcsb import LigandInstance
from ..util import http
from ..util.paths import (
    ensure_dir,
    target_aligned_mol2_dir,
    target_catalogue_dir,
    target_grouped_mol2_dir,
    target_reference_pdb,
    target_structures_dir,
)
from . import pocket, realign
from .efficacy import EfficacyCall, TargetEfficacy
from .pockets import PocketDef, PocketDefaults

log = logging.getLogger("pharmpipe.groups.group")

QUARANTINED = "quarantined"
ASSIGNED = "assigned"


@dataclass
class Pose:
    """One representative bound-pose carried over from Stage 2."""
    pdb_id: str
    het_code: str
    chain: str
    seqid: str
    aligned_mol2: Path
    mapping: str = "unknown"            # primary | surrogate | unknown
    accessions: list[str] = field(default_factory=list)
    organisms: list[str] = field(default_factory=list)
    resolution: float | None = None     # structure resolution (representative pick)
    pocket_rmsd: float | None = None    # Stage-2 fit RMSD (tie-break)
    # filled by Stage 3
    fingerprint: frozenset[str] = frozenset()
    cluster_id: int = -1
    pocket: str | None = None          # verified pocket label (None if quarantined)
    pocket_status: str = QUARANTINED
    efficacy: EfficacyCall | None = None

    @property
    def label(self) -> str:
        return f"{self.pdb_id}_{self.het_code}_{self.chain}{self.seqid}"

    @property
    def cell(self) -> str | None:
        """The (pocket, efficacy) cell this pose belongs to, or None if it is not
        a reversible, pocket-assigned, efficacy-known binder."""
        if self.pocket is None or self.efficacy is None:
            return None
        if self.efficacy.is_separate_state or self.efficacy.is_unknown:
            return None
        return f"{self.pocket}__{self.efficacy.efficacy}"


@dataclass
class PocketCluster:
    cluster_id: int
    label: str | None
    status: str                        # assigned | quarantined
    pose_indices: list[int]
    consensus_residues: set[str]
    review: bool = False               # unexpected pocket worth a look


@dataclass
class GroupResult:
    slug: str
    pdef: PocketDef
    poses: list[Pose]
    clusters: list[PocketCluster]
    expected_pockets: list[str]

    @property
    def cells(self) -> dict[str, list[Pose]]:
        out: dict[str, list[Pose]] = defaultdict(list)
        for p in self.poses:
            if p.cell is not None:
                out[p.cell].append(p)
        return dict(sorted(out.items()))

    @property
    def separate_state(self) -> list[Pose]:
        return [p for p in self.poses if p.efficacy and p.efficacy.is_separate_state
                and p.pocket is not None]

    @property
    def unknown(self) -> list[Pose]:
        return [p for p in self.poses if p.efficacy and p.efficacy.is_unknown
                and p.pocket is not None]

    @property
    def quarantined(self) -> list[Pose]:
        return [p for p in self.poses if p.pocket is None]

    @property
    def pockets_found(self) -> list[str]:
        return sorted({c.label for c in self.clusters if c.label})


# --- loading -----------------------------------------------------------------

def _load_accession_organisms(slug: str) -> dict[str, str]:
    path = target_catalogue_dir(slug) / "resolved.json"
    if not path.exists():
        return {}
    data = json.loads(path.read_text(encoding="utf-8"))
    return {a["accession"]: a.get("organism_name", "") for a in data.get("accessions", [])}


def _load_structure_meta(slug: str) -> dict[str, dict]:
    path = target_catalogue_dir(slug) / "per_structure.csv"
    meta: dict[str, dict] = {}
    if not path.exists():
        return meta
    for row in csv.DictReader(path.open(encoding="utf-8")):
        try:
            resolution = float(row.get("resolution", "") or "nan")
        except ValueError:
            resolution = None
        meta[row["pdb_id"]] = {
            "mapping": row.get("mapping", "unknown"),
            "accessions": [a for a in row.get("uniprot_accessions", "").split(";") if a],
            "resolution": resolution,
        }
    return meta


def _load_smiles(slug: str) -> dict[str, str]:
    path = target_catalogue_dir(slug) / "unique_ligands.csv"
    if not path.exists():
        return {}
    return {row["het_code"].upper(): row.get("smiles", "")
            for row in csv.DictReader(path.open(encoding="utf-8"))}


def load_poses(slug: str) -> list[Pose]:
    """Reconstruct the Stage-2 representative poses from the tracked catalogue."""
    sf = target_catalogue_dir(slug) / "site_filter.csv"
    if not sf.exists():
        return []
    aligned_dir = target_aligned_mol2_dir(slug)
    struct_meta = _load_structure_meta(slug)
    acc_org = _load_accession_organisms(slug)

    poses: list[Pose] = []
    for row in csv.DictReader(sf.open(encoding="utf-8")):
        if row["status"] != "kept" or not row.get("aligned_mol2"):
            continue
        meta = struct_meta.get(row["pdb_id"], {})
        accs = meta.get("accessions", [])
        try:
            prmsd = float(row.get("pocket_rmsd", "") or "nan")
        except ValueError:
            prmsd = None
        poses.append(Pose(
            pdb_id=row["pdb_id"],
            het_code=row["het_code"],
            chain=row["chain"],
            seqid=row["seqid"],
            aligned_mol2=aligned_dir / row["aligned_mol2"],
            mapping=meta.get("mapping", "unknown"),
            accessions=accs,
            organisms=sorted({acc_org.get(a, "") for a in accs if acc_org.get(a)}),
            resolution=meta.get("resolution"),
            pocket_rmsd=prmsd,
        ))
    return poses


# --- pocket verification -----------------------------------------------------

def _verify_pockets(slug: str, poses: list[Pose], pdef: PocketDef,
                    cutoff: float) -> None:
    """Fingerprint each pose in its own native structure, and (for multi-pocket
    targets) re-align it onto the reference by a whole-assembly fit so distinct
    pockets land at their true subunit interfaces (sets ``pose.aligned_mol2``)."""
    by_pdb: dict[str, list[Pose]] = defaultdict(list)
    for p in poses:
        by_pdb[p.pdb_id].append(p)

    realign_on, ref_model, smiles, out_dir, cfg = _realign_setup(slug, pdef)
    for pdb_id, group in by_pdb.items():
        cif = target_structures_dir(slug) / f"{pdb_id}.cif"
        if not cif.exists():
            log.warning("[%s] native structure %s missing; poses quarantined", slug, pdb_id)
            continue
        st = structures.read_structure(cif)
        index = pocket.ContactIndex.from_structure(st, max_radius=cutoff)
        for p in group:
            res = pocket.find_ligand(index.model, p.het_code, p.chain, p.seqid)
            if res is not None:
                p.fingerprint = index.fingerprint(res, cutoff=cutoff)
        if realign_on:
            _realign_group(slug, pdb_id, group, index.model, ref_model, st,
                           smiles, out_dir, cfg)


def _realign_setup(slug: str, pdef: PocketDef):
    """Prepare reference + output dir for global re-alignment, or disable it."""
    if not pdef.realign_global:
        return False, None, {}, None, None
    ref_path = target_reference_pdb(slug)
    if not ref_path.exists():
        log.warning("[%s] reference.pdb missing; cannot realign globally", slug)
        return False, None, {}, None, None
    ref_model = structures.read_structure(ref_path)[0]
    out_dir = ensure_dir(target_grouped_mol2_dir(slug))
    for old in out_dir.glob("*.mol2"):
        old.unlink()
    return True, ref_model, _load_smiles(slug), out_dir, http.HttpConfig()


def _realign_group(slug, pdb_id, group, model, ref_model, st, smiles, out_dir, cfg) -> None:
    transform = realign.global_transform(ref_model, model)
    if transform is None:
        log.warning("[%s] %s: global fit failed; keeping Stage-2 frame", slug, pdb_id)
        return
    for p in group:
        res = pocket.find_ligand(model, p.het_code, p.chain, p.seqid)
        if res is None:
            continue
        realign.apply_transform(res, transform)
        inst = LigandInstance(pdb_id=p.pdb_id, comp_id=p.het_code,
                              auth_asym_id=p.chain, auth_seq_id=str(p.seqid))
        er = mol2.extract_instance(st, inst, out_dir, cfg, smiles.get(p.het_code.upper(), ""))
        if er.ok and er.out_path is not None:
            p.aligned_mol2 = er.out_path
        else:
            log.warning("[%s] realign mol2 failed for %s: %s", slug, p.label, er.message)


def _assign_clusters(poses: list[Pose], pdef: PocketDef,
                     d: PocketDefaults) -> list[PocketCluster]:
    fps = [p.fingerprint for p in poses]
    labels = pocket.cluster_fingerprints(
        fps, jaccard_min=d.jaccard_min, overlap_min=d.overlap_min,
        min_shared=d.min_shared_residues)
    for p, cid in zip(poses, labels, strict=True):
        p.cluster_id = cid

    members: dict[int, list[int]] = defaultdict(list)
    for i, cid in enumerate(labels):
        members[cid].append(i)

    clusters: list[PocketCluster] = []
    secondary_n = 0
    for cid in sorted(members, key=lambda c: -len(members[c])):
        idx = members[cid]
        big_enough = len(idx) >= d.min_pocket_poses
        het_set = {poses[i].het_code.upper() for i in idx}
        consensus = pocket.consensus_residues(fps, idx)

        if not big_enough and not (pdef.collapse_to_primary and len(idx) > 1):
            label, status, review = None, QUARANTINED, False
        elif cid == 0 or pdef.collapse_to_primary:
            label, status, review = pdef.primary_label, ASSIGNED, False
        else:
            marker_label = pdef.label_for_markers(het_set)
            if marker_label:
                label, status, review = marker_label, ASSIGNED, False
            else:
                secondary_n += 1
                label, status, review = f"secondary_{secondary_n}", ASSIGNED, True

        for i in idx:
            poses[i].pocket = label
            poses[i].pocket_status = status
        clusters.append(PocketCluster(cid, label, status, idx, consensus, review))
    _apply_marker_overrides(poses, clusters, pdef, fps)
    return clusters


def _apply_marker_overrides(poses: list[Pose], clusters: list[PocketCluster],
                            pdef: PocketDef, fps: list[frozenset[str]]) -> None:
    """Place a pose at a curated secondary site when geometry cannot separate it.

    A HET listed as a ``marker_het`` for a secondary pocket is, by curator
    knowledge, a diagnostic of that site. Usually the site is also a distinct
    geometric cluster and is named at the cluster level. But some secondary sites
    share their contact residues with the primary pocket (e.g. the nAChR accessory
    alpha4(+)/alpha4(-) interface reuses the orthosteric aromatic box), so contact
    fingerprints merge them; under ``collapse_to_primary`` the pose would then be
    mislabelled as primary. This per-pose override reassigns only such marker poses
    (those whose current label differs from their marker label) into a dedicated
    cluster, leaving non-marker poses — and already-correct marker clusters — alone.
    """
    moved: dict[str, list[int]] = defaultdict(list)
    for i, p in enumerate(poses):
        mlabel = pdef.label_for_markers({p.het_code.upper()})
        if mlabel and p.pocket != mlabel:
            p.pocket = mlabel
            p.pocket_status = ASSIGNED
            moved[mlabel].append(i)
    if not moved:
        return
    moved_all = {i for idx in moved.values() for i in idx}
    for c in clusters:
        c.pose_indices = [i for i in c.pose_indices if i not in moved_all]
    clusters[:] = [c for c in clusters if c.pose_indices]
    next_id = max((c.cluster_id for c in clusters), default=-1) + 1
    for label, idx in sorted(moved.items()):
        consensus = pocket.consensus_residues(fps, idx)
        clusters.append(PocketCluster(next_id, label, ASSIGNED, idx, consensus, review=False))
        next_id += 1


# --- top-level ---------------------------------------------------------------

def group_target(slug: str, pdef: PocketDef, d: PocketDefaults,
                 teff: TargetEfficacy) -> GroupResult:
    poses = load_poses(slug)
    _verify_pockets(slug, poses, pdef, d.contact_angstrom)
    clusters = _assign_clusters(poses, pdef, d)
    for p in poses:
        p.efficacy = teff.call(p.het_code)
    return GroupResult(slug=slug, pdef=pdef, poses=poses, clusters=clusters,
                       expected_pockets=pdef.expected_pockets)


def _rep_key(p: Pose) -> tuple:
    return (p.resolution if p.resolution is not None else 1e9,
            p.pocket_rmsd if p.pocket_rmsd is not None else 1e9, p.pdb_id)


def representative_poses(poses: list[Pose]) -> list[Pose]:
    """One pose per HET code: best resolution, then tightest fit, then PDB id."""
    best: dict[str, Pose] = {}
    for p in poses:
        key = p.het_code.upper()
        if key not in best or _rep_key(p) < _rep_key(best[key]):
            best[key] = p
    return [best[k] for k in sorted(best)]


def status_counts(res: GroupResult) -> Counter:
    c: Counter = Counter()
    c["poses"] = len(res.poses)
    c["in_cells"] = sum(len(v) for v in res.cells.values())
    c["cells"] = len(res.cells)
    c["separate_state"] = len(res.separate_state)
    c["unknown"] = len(res.unknown)
    c["quarantined"] = len(res.quarantined)
    return c
