"""Superpose bound-ligand instances into a per-target reference frame.

Strategy (per CLAUDE.md decision: *binding-site-local* superposition):

  1. A reference structure defines the site via an ``anchor`` residue (the
     reference ligand or catalytic ion). Reference pocket = polymer Calpha atoms
     within ``pocket_shell`` of the anchor.
  2. For each candidate instance we first do a sequence-aware *global* fit of the
     candidate's principal pocket chain onto the reference chain (gemmi), which
     establishes a rough frame + correspondence even across mutants/surrogates.
  3. We then *refine* using only pocket atoms: reference pocket Calpha are paired
     by spatial proximity (post-global) to candidate Calpha, and we re-superpose
     on just those pairs. This yields the tightest possible overlay of the actual
     binding site, which is what matters for comparing poses.
  4. An instance is kept only if the pocket fit is good (enough matched atoms,
     low RMSD) AND, after transformation, the ligand centroid lands within
     ``cutoff`` of the anchor — i.e. it genuinely binds where the reference
     ligand binds. Off-site poses (wrong site, wrong protein, allosteric) fail
     one of these tests and are dropped (and reported).
"""

from __future__ import annotations

import logging
from dataclasses import dataclass

import gemmi

from ..pdb.rcsb import LigandInstance
from .config import SiteDef

log = logging.getLogger("pharmpipe.sites.align")


# --- small geometry helpers ----------------------------------------------

def _positions(res: gemmi.Residue) -> list[gemmi.Position]:
    return [atom.pos for atom in res]


def _centroid(positions: list[gemmi.Position]) -> gemmi.Position:
    n = len(positions)
    x = sum(p.x for p in positions) / n
    y = sum(p.y for p in positions) / n
    z = sum(p.z for p in positions) / n
    return gemmi.Position(x, y, z)


def _apply(t: gemmi.Transform, p: gemmi.Position) -> gemmi.Position:
    q = t.apply(p)
    return gemmi.Position(q.x, q.y, q.z)


def _min_dist(p: gemmi.Position, others: list[gemmi.Position]) -> float:
    return min((p.dist(o) for o in others), default=float("inf"))


# --- reference --------------------------------------------------------------

@dataclass
class PocketCA:
    chain: str
    seqid: int
    pos: gemmi.Position


@dataclass
class SiteReference:
    site: SiteDef
    structure: gemmi.Structure
    anchor_atoms: list[gemmi.Position]
    anchor_centroid: gemmi.Position
    pocket: list[PocketCA]          # reference pocket Calpha (any chain) near anchor
    ref_chain: str                  # chain richest in pocket Calpha (for global fit)


def _find_anchor_residues(model: gemmi.Model, anchor_het: str) -> list[gemmi.Residue]:
    out = []
    for chain in model:
        for res in chain:
            if res.name.upper() == anchor_het:
                out.append(res)
    return out


def _pocket_near(model: gemmi.Model, ref_atoms: list[gemmi.Position],
                 shell: float) -> list[PocketCA]:
    """Polymer Calpha atoms within `shell` of any of `ref_atoms`."""
    pocket: list[PocketCA] = []
    for chain in model:
        poly = chain.get_polymer()
        for res in poly:
            ca = res.get_ca()
            if ca is None:
                continue
            if _min_dist(ca.pos, ref_atoms) <= shell:
                pocket.append(PocketCA(chain.name, res.seqid.num, ca.pos))
    return pocket


def build_reference(st: gemmi.Structure, site: SiteDef) -> SiteReference | None:
    if len(st) == 0:
        return None
    model = st[0]
    candidates = _find_anchor_residues(model, site.anchor_het)
    if not candidates:
        log.warning("[%s] anchor %s not found in reference %s",
                    site.slug, site.anchor_het, site.reference_pdb)
        return None

    # Pick the anchor copy with the richest surrounding pocket (the canonical site).
    best_res, best_pocket = None, []
    for res in candidates:
        atoms = _positions(res)
        pocket = _pocket_near(model, atoms, site.pocket_shell_angstrom)
        if len(pocket) > len(best_pocket):
            best_res, best_pocket = res, pocket
    if best_res is None or not best_pocket:
        log.warning("[%s] anchor %s in %s has no protein pocket",
                    site.slug, site.anchor_het, site.reference_pdb)
        return None

    anchor_atoms = _positions(best_res)
    # Chain contributing the most pocket Calpha -> reference chain for the global fit.
    counts: dict[str, int] = {}
    for pc in best_pocket:
        counts[pc.chain] = counts.get(pc.chain, 0) + 1
    ref_chain = max(counts, key=counts.get)

    return SiteReference(
        site=site,
        structure=st,
        anchor_atoms=anchor_atoms,
        anchor_centroid=_centroid(anchor_atoms),
        pocket=best_pocket,
        ref_chain=ref_chain,
    )


# --- per-instance alignment -------------------------------------------------

@dataclass
class AlignedInstance:
    instance: LigandInstance
    status: str            # kept | off_site | poor_fit | no_pocket | not_found | align_error
    transform: gemmi.Transform | None = None
    centroid_distance: float | None = None
    pocket_rmsd: float | None = None
    n_pocket: int = 0
    message: str = ""

    @property
    def kept(self) -> bool:
        return self.status == "kept"


def _get_polymer(model: gemmi.Model, chain_name: str) -> gemmi.ResidueSpan | None:
    for chain in model:
        if chain.name == chain_name:
            return chain.get_polymer()
    return None


def _principal_chain(model: gemmi.Model, lig_atoms: list[gemmi.Position],
                     shell: float) -> str | None:
    """Polymer chain with the most Calpha near the ligand."""
    counts: dict[str, int] = {}
    for chain in model:
        for res in chain.get_polymer():
            ca = res.get_ca()
            if ca is not None and _min_dist(ca.pos, lig_atoms) <= shell:
                counts[chain.name] = counts.get(chain.name, 0) + 1
    return max(counts, key=counts.get) if counts else None


def find_residue(model: gemmi.Model, inst: LigandInstance) -> gemmi.Residue | None:
    for chain in model:
        if chain.name != inst.auth_asym_id:
            continue
        for res in chain:
            if res.name == inst.comp_id and str(res.seqid.num) == inst.auth_seq_id:
                return res
    matches = [res for chain in model for res in chain
               if res.name == inst.comp_id and str(res.seqid.num) == inst.auth_seq_id]
    return matches[0] if len(matches) == 1 else None


def align_instance(st: gemmi.Structure, inst: LigandInstance,
                   ref: SiteReference) -> AlignedInstance:
    site = ref.site
    if len(st) == 0:
        return AlignedInstance(inst, "not_found", message="empty structure")
    model = st[0]

    res = find_residue(model, inst)
    if res is None:
        return AlignedInstance(inst, "not_found", message="ligand instance not located")
    lig_atoms = _positions(res)

    # 1) Global, sequence-aware fit of the principal pocket chain onto the reference.
    principal = _principal_chain(model, lig_atoms, site.pocket_shell_angstrom)
    if principal is None:
        return AlignedInstance(inst, "no_pocket", message="no protein near ligand")
    cand_poly = _get_polymer(model, principal)
    ref_poly = _get_polymer(ref.structure[0], ref.ref_chain)
    if cand_poly is None or ref_poly is None:
        return AlignedInstance(inst, "no_pocket", message="missing polymer chain")

    try:
        glob = gemmi.calculate_superposition(ref_poly, cand_poly,
                                             gemmi.PolymerType.PeptideL,
                                             gemmi.SupSelect.CaP)
    except Exception as exc:  # noqa: BLE001
        return AlignedInstance(inst, "align_error", message=f"global fit failed: {exc}")
    t_global = glob.transform

    # 2) Pair reference pocket Calpha to candidate Calpha by proximity (post-global),
    #    then refine the fit on just those pocket atoms.
    cand_ca: list[gemmi.Position] = []           # original (pre-transform) candidate Calpha
    cand_ca_in_ref: list[gemmi.Position] = []    # same atoms moved into the reference frame
    for chain in model:
        for r in chain.get_polymer():
            ca = r.get_ca()
            if ca is not None:
                cand_ca.append(ca.pos)
                cand_ca_in_ref.append(_apply(t_global, ca.pos))

    fixed: list[gemmi.Position] = []
    moving: list[gemmi.Position] = []
    for pc in ref.pocket:
        best_i, best_d = -1, site.match_distance_angstrom
        for i, q in enumerate(cand_ca_in_ref):
            d = pc.pos.dist(q)
            if d <= best_d:
                best_d, best_i = d, i
        if best_i >= 0:
            fixed.append(pc.pos)
            moving.append(cand_ca[best_i])

    n_pocket = len(fixed)
    if n_pocket >= site.min_pocket_atoms:
        local = gemmi.superpose_positions(fixed, moving)
        transform, rmsd = local.transform, local.rmsd
    else:
        # Not enough pocket correspondence -> fall back to the global fit, low confidence.
        transform, rmsd = t_global, glob.rmsd

    lig_in_ref = [_apply(transform, p) for p in lig_atoms]
    centroid_dist = _centroid(lig_in_ref).dist(ref.anchor_centroid)

    if n_pocket < site.min_pocket_atoms:
        status = "no_pocket"
    elif rmsd > site.max_pocket_rmsd_angstrom:
        status = "poor_fit"
    elif centroid_dist > site.cutoff_angstrom:
        status = "off_site"
    else:
        status = "kept"

    return AlignedInstance(inst, status, transform=transform,
                           centroid_distance=centroid_dist, pocket_rmsd=rmsd,
                           n_pocket=n_pocket)


def transform_residue(res: gemmi.Residue, t: gemmi.Transform) -> None:
    """Move a residue's atoms into the reference frame (in place)."""
    for atom in res:
        atom.pos = _apply(t, atom.pos)
