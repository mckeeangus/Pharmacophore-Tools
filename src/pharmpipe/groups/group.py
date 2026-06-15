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

from ..io import structures
from ..util.paths import (
    target_aligned_mol2_dir,
    target_catalogue_dir,
    target_structures_dir,
)
from . import pocket
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
        meta[row["pdb_id"]] = {
            "mapping": row.get("mapping", "unknown"),
            "accessions": [a for a in row.get("uniprot_accessions", "").split(";") if a],
        }
    return meta


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
        poses.append(Pose(
            pdb_id=row["pdb_id"],
            het_code=row["het_code"],
            chain=row["chain"],
            seqid=row["seqid"],
            aligned_mol2=aligned_dir / row["aligned_mol2"],
            mapping=meta.get("mapping", "unknown"),
            accessions=accs,
            organisms=sorted({acc_org.get(a, "") for a in accs if acc_org.get(a)}),
        ))
    return poses


# --- pocket verification -----------------------------------------------------

def _fingerprint_poses(slug: str, poses: list[Pose], cutoff: float) -> None:
    """Fingerprint each pose in its own native structure (cached mmCIF)."""
    by_pdb: dict[str, list[Pose]] = defaultdict(list)
    for p in poses:
        by_pdb[p.pdb_id].append(p)
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
    return clusters


# --- top-level ---------------------------------------------------------------

def group_target(slug: str, pdef: PocketDef, d: PocketDefaults,
                 teff: TargetEfficacy) -> GroupResult:
    poses = load_poses(slug)
    _fingerprint_poses(slug, poses, d.contact_angstrom)
    clusters = _assign_clusters(poses, pdef, d)
    for p in poses:
        p.efficacy = teff.call(p.het_code)
    return GroupResult(slug=slug, pdef=pdef, poses=poses, clusters=clusters,
                       expected_pockets=pdef.expected_pockets)


def status_counts(res: GroupResult) -> Counter:
    c: Counter = Counter()
    c["poses"] = len(res.poses)
    c["in_cells"] = sum(len(v) for v in res.cells.values())
    c["cells"] = len(res.cells)
    c["separate_state"] = len(res.separate_state)
    c["unknown"] = len(res.unknown)
    c["quarantined"] = len(res.quarantined)
    return c
