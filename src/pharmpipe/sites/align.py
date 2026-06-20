"""Superpose bound-ligand instances into a per-target reference frame.

Strategy (per CLAUDE.md decision: *binding-site-local* superposition). The fit is
optimised for the geometry of the residues that actually line the pocket — that
constancy is what makes overlaid poses comparable for pharmacophore building, and
it is where naive single-pass fits drift on low-identity surrogates.

  1. A reference structure defines the site via an ``anchor`` residue (the
     reference ligand or catalytic ion). Reference pocket = polymer residues whose
     Calpha lies within ``pocket_shell`` of the anchor; we keep their backbone
     atoms and each residue's Calpha distance to the anchor.
  2. For each candidate instance we first do a sequence-aware *global* fit of the
     candidate's principal pocket chain onto the reference chain (gemmi). This is
     only an initialiser: it fixes the gross orientation and the right subunit even
     across mutants/surrogates.
  3. We then run an *iterative pocket-local refinement* (ICP). Each iteration
     re-pairs reference pocket residues to the nearest candidate residue (capture
     radius ``refine_pair_radius``), then re-superposes on the paired backbone
     atoms (N, CA, C, O) — weighting each residue by a Gaussian on its Calpha
     distance to the anchor (``anchor_weight_sigma``) so the *immediate* binding
     site dominates. Re-pairing + re-fitting converges to the locally-optimal
     binding-site overlay even when the backbone genuinely differs (surrogates).
  4. An instance is kept only if the pocket fit is good (enough matched residues,
     low RMSD) AND, after transformation, the ligand centroid lands within
     ``cutoff`` of the anchor — i.e. it genuinely binds where the reference
     ligand binds. Off-site poses (wrong site, wrong protein, allosteric) fail
     one of these tests and are dropped (and reported).
"""

from __future__ import annotations

import logging
import math
from dataclasses import dataclass

import gemmi

from ..pdb.rcsb import LigandInstance
from .config import SiteDef

log = logging.getLogger("pharmpipe.sites.align")

_BACKBONE = ("N", "CA", "C", "O")


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
class PocketResidue:
    chain: str
    seqid: int
    ca: gemmi.Position
    backbone: dict[str, gemmi.Position]   # name -> pos for present N, CA, C, O
    dist_anchor: float                    # CA distance to the anchor centroid


@dataclass
class PocketCA:                           # kept for backward-compatible callers
    chain: str
    seqid: int
    pos: gemmi.Position


@dataclass
class SiteReference:
    site: SiteDef
    structure: gemmi.Structure
    anchor_atoms: list[gemmi.Position]
    anchor_centroid: gemmi.Position
    pocket_res: list[PocketResidue]   # reference pocket residues (backbone) near anchor
    ref_chain: str                    # chain richest in pocket Calpha (for global fit)

    @property
    def pocket(self) -> list[PocketCA]:
        return [PocketCA(pr.chain, pr.seqid, pr.ca) for pr in self.pocket_res]


def _backbone(res: gemmi.Residue) -> dict[str, gemmi.Position]:
    out: dict[str, gemmi.Position] = {}
    for atom in res:
        if atom.name in _BACKBONE and atom.name not in out:
            out[atom.name] = atom.pos
    return out


def _find_anchor_residues(model: gemmi.Model, anchor_het: str) -> list[gemmi.Residue]:
    out = []
    for chain in model:
        for res in chain:
            if res.name.upper() == anchor_het:
                out.append(res)
    return out


def _pocket_near(model: gemmi.Model, ref_atoms: list[gemmi.Position],
                 anchor_centroid: gemmi.Position, shell: float) -> list[PocketResidue]:
    """Polymer residues whose Calpha is within `shell` of any of `ref_atoms`."""
    pocket: list[PocketResidue] = []
    for chain in model:
        for res in chain.get_polymer():
            ca = res.get_ca()
            if ca is None:
                continue
            if _min_dist(ca.pos, ref_atoms) <= shell:
                pocket.append(PocketResidue(chain.name, res.seqid.num, ca.pos,
                                            _backbone(res), ca.pos.dist(anchor_centroid)))
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
    best_pocket: list[PocketResidue] = []
    for res in candidates:
        atoms = _positions(res)
        pocket = _pocket_near(model, atoms, _centroid(atoms), site.pocket_shell_angstrom)
        if len(pocket) > len(best_pocket):
            best_res_atoms, best_pocket = atoms, pocket
    if not best_pocket:
        log.warning("[%s] anchor %s in %s has no protein pocket",
                    site.slug, site.anchor_het, site.reference_pdb)
        return None

    # Chain contributing the most pocket Calpha -> reference chain for the global fit.
    counts: dict[str, int] = {}
    for pr in best_pocket:
        counts[pr.chain] = counts.get(pr.chain, 0) + 1
    ref_chain = max(counts, key=counts.get)

    return SiteReference(
        site=site,
        structure=st,
        anchor_atoms=best_res_atoms,
        anchor_centroid=_centroid(best_res_atoms),
        pocket_res=best_pocket,
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


def _candidate_pocket_residues(model: gemmi.Model, t_global: gemmi.Transform,
                               ref: SiteReference, site: SiteDef
                               ) -> list[tuple[gemmi.Residue, gemmi.Position]]:
    """Candidate polymer residues whose Calpha (under the global fit) lands near the
    pocket — the working set for ICP, so distant chains cannot mis-pair."""
    limit = site.pocket_shell_angstrom + site.refine_pair_radius_angstrom
    out: list[tuple[gemmi.Residue, gemmi.Position]] = []
    for chain in model:
        for r in chain.get_polymer():
            ca = r.get_ca()
            if ca is not None and _apply(t_global, ca.pos).dist(ref.anchor_centroid) <= limit:
                out.append((r, ca.pos))
    return out


def _pocket_ca_rmsd(ref: SiteReference, cand_ca: list[gemmi.Position],
                    t: gemmi.Transform, site: SiteDef) -> tuple[float | None, int]:
    """Unweighted Calpha RMSD over reference pocket residues that have a candidate
    Calpha within ``match_distance`` after transform `t` (comparable to the old
    metric, used for the keep/reject thresholds)."""
    moved = [_apply(t, ca) for ca in cand_ca]
    sq, n = 0.0, 0
    for pr in ref.pocket_res:
        d = min((pr.ca.dist(m) for m in moved), default=1e9)
        if d <= site.match_distance_angstrom:
            sq += d * d
            n += 1
    return ((sq / n) ** 0.5 if n else None), n


def _refine_local(ref: SiteReference,
                  cand_res: list[tuple[gemmi.Residue, gemmi.Position]],
                  t_init: gemmi.Transform, site: SiteDef
                  ) -> tuple[gemmi.Transform | None, float | None, int]:
    """Iterative closest-point refinement of the binding-site overlay (see module
    docstring): re-pair pocket residues each iteration, then re-superpose on
    anchor-weighted backbone atoms. Returns (transform, pocket RMSD, n_pocket) or
    (None, None, 0) if correspondence is too thin to fit."""
    if not cand_res:
        return None, None, 0
    sigma = site.anchor_weight_sigma_angstrom
    cand_ca = [ca for _, ca in cand_res]
    t = t_init
    for _ in range(max(1, site.refine_iterations)):
        moved = [_apply(t, ca) for ca in cand_ca]
        fixed: list[gemmi.Position] = []
        moving: list[gemmi.Position] = []
        weights: list[float] = []
        for pr in ref.pocket_res:
            best_i, best_d = -1, site.refine_pair_radius_angstrom
            for i, mp in enumerate(moved):
                d = pr.ca.dist(mp)
                if d < best_d:
                    best_d, best_i = d, i
            if best_i < 0:
                continue
            w = math.exp(-(pr.dist_anchor / sigma) ** 2) if sigma > 0 else 1.0
            cres = cand_res[best_i][0]
            if site.use_backbone:
                cand_bb = _backbone(cres)
                for name, pos in pr.backbone.items():
                    q = cand_bb.get(name)
                    if q is not None:
                        fixed.append(pos)
                        moving.append(q)
                        weights.append(w)
            else:
                fixed.append(pr.ca)
                moving.append(cand_ca[best_i])
                weights.append(w)
        if len(fixed) < 3:                       # degenerate -> let caller fall back
            return None, None, 0
        t = gemmi.superpose_positions(fixed, moving, weights).transform
    rmsd, n_pocket = _pocket_ca_rmsd(ref, cand_ca, t, site)
    return t, rmsd, n_pocket


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

    # 2) Iterative pocket-local refinement (ICP) seeded by the global fit. Restrict
    #    the working set to candidate residues near the pocket so distant chains
    #    cannot accidentally pair, then re-pair + re-fit on weighted backbone atoms.
    cand_res = _candidate_pocket_residues(model, t_global, ref, site)
    transform, rmsd, n_pocket = _refine_local(ref, cand_res, t_global, site)
    if transform is None:                       # too little pocket correspondence
        transform, rmsd, n_pocket = t_global, glob.rmsd, 0

    lig_in_ref = [_apply(transform, p) for p in lig_atoms]
    centroid_dist = _centroid(lig_in_ref).dist(ref.anchor_centroid)

    if n_pocket < site.min_pocket_atoms:
        status = "no_pocket"
    elif rmsd is None or rmsd > site.max_pocket_rmsd_angstrom:
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
