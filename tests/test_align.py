"""Unit tests for the docked-seed feature-alignment core (Stage 4, offline, pure)."""

from __future__ import annotations

import numpy as np

from pharmpipe.features.conformers import generate_conformers
from pharmpipe.pharmacophore.align import (
    AlignRecord,
    _axial_mean_direction,
    _slot_direction,
    align_features,
    alignment_quality,
    compare_alignments,
    consolidate,
    direction_rigidity,
    seed_align,
)
from pharmpipe.pharmacophore.config import AlignmentConfig

# A rotation (90 deg about z) + translation used to make a rigid copy of a feature cloud.
_ROT = np.array([[0.0, -1.0, 0.0], [1.0, 0.0, 0.0], [0.0, 0.0, 1.0]])
_TRANS = np.array([10.0, -3.0, 2.0])


def _cloud(acc_dir=None):
    """A 4-feature cloud as (family, xyz, direction). ``acc_dir`` sets the Acceptor direction."""
    return [("Aromatic", np.array([0.0, 0.0, 0.0]), None),
            ("PosIonizable", np.array([3.0, 0.0, 0.0]), None),
            ("Acceptor", np.array([0.0, 4.0, 0.0]), acc_dir),
            ("Donor", np.array([0.0, 0.0, 5.0]), None)]


def _rigid_copy(cloud, rot=_ROT, trans=_TRANS):
    return [(fam, xyz @ rot.T + trans, None if d is None else d @ rot.T)
            for fam, xyz, d in cloud]


def _seed(cloud, lig):
    return [(fam, xyz, d, lig) for fam, xyz, d in cloud]


def test_align_recovers_known_rigid_transform():
    ref = _cloud()
    probe = _rigid_copy(ref)                       # a rotated+translated copy
    res = align_features(probe, ref, dist_tol=0.5, min_clique=3)
    assert res is not None
    assert res.n_matched == 4
    assert res.rmsd < 1e-6
    for (_, p, _), (_, r, _) in zip(probe, ref, strict=True):
        assert np.allclose(res.apply(p), r, atol=1e-5)


def test_align_greedy_fallback_still_recovers_transform():
    ref = _cloud()
    probe = _rigid_copy(ref)
    res = align_features(probe, ref, dist_tol=0.5, min_clique=3, max_nodes=1)
    assert res is not None and res.n_matched == 4 and res.rmsd < 1e-6


def test_align_rejects_below_min_clique():
    ref = _cloud()
    probe = [("Aromatic", np.array([0.0, 0.0, 0.0]), None),
             ("Donor", np.array([0.0, 0.0, 5.0]), None)]  # only 2 shared families
    assert align_features(probe, ref, dist_tol=0.5, min_clique=3) is None


def test_align_rejects_inconsistent_geometry():
    ref = _cloud()
    probe = [("Aromatic", np.array([0.0, 0.0, 0.0]), None),
             ("PosIonizable", np.array([9.0, 0.0, 0.0]), None),
             ("Acceptor", np.array([0.0, 1.0, 0.0]), None)]
    assert align_features(probe, ref, dist_tol=0.5, min_clique=3) is None


def test_directional_matching_penalises_flipped_acceptor():
    # Same positions, but the probe's acceptor points the OPPOSITE way (a "ring-flip"). With
    # directional matching on, the projected point no longer superposes -> higher RMSD than a
    # correctly-oriented probe; with it off, both are identical (position-only).
    ref = _cloud(acc_dir=np.array([0.0, 1.0, 0.0]))
    aligned = _rigid_copy(ref)                                  # acceptor dir rotated consistently
    flipped = _rigid_copy(_cloud(acc_dir=np.array([0.0, -1.0, 0.0])))  # opposite lone pair
    ka = align_features(aligned, ref, dist_tol=0.5, min_clique=3, use_directions=True)
    kf = align_features(flipped, ref, dist_tol=0.5, min_clique=3, use_directions=True)
    assert ka.rmsd < 1e-6                                       # correct orientation superposes
    assert kf.rmsd > ka.rmsd + 0.5                             # flipped one is penalised
    # positional-only: the flip is invisible
    pf = align_features(flipped, ref, dist_tol=0.5, min_clique=3, use_directions=False)
    assert pf.rmsd < 1e-6


def test_two_feature_roll_irrelevant_admitted_only_when_enabled():
    # A genuine two-feature ligand: nothing lies off the two-point axis, so the one undetermined
    # DOF (roll about that axis) moves nothing. Placeable when two_feature is on, dropped when off.
    ref = [("PosIonizable", np.array([0.0, 0.0, 0.0]), None),
           ("Acceptor", np.array([5.5, 0.0, 0.0]), None)]
    probe = _rigid_copy(ref)
    assert align_features(probe, ref, dist_tol=0.5, min_clique=3) is None
    res = align_features(probe, ref, dist_tol=0.5, min_clique=3, two_feature=True)
    assert res is not None and res.n_matched == 2
    for (_, p, _), (_, r, _) in zip(probe, ref, strict=True):
        assert np.allclose(res.apply(p), r, atol=1e-5)   # the two features are placed exactly


def test_two_feature_directionality_determines_and_protects():
    # ref has only two families; the probe carries a THIRD (off-axis) feature the ref lacks, so
    # only two features can match and the probe has >2 features (roll-irrelevant does NOT apply).
    ref = [("PosIonizable", np.array([0.0, 0.0, 0.0]), None),
           ("Acceptor", np.array([5.5, 0.0, 0.0]), np.array([0.0, 1.0, 0.0]))]
    probe = _rigid_copy([("PosIonizable", np.array([0.0, 0.0, 0.0]), None),
                         ("Acceptor", np.array([5.5, 0.0, 0.0]), np.array([0.0, 1.0, 0.0])),
                         ("LumpedHydrophobe", np.array([0.0, 0.0, 7.0]), None)])
    # a directional acceptor supplies the third constraint point -> transform determined -> admit
    res = align_features(probe, ref, dist_tol=0.5, min_clique=3,
                         use_directions=True, two_feature=True)
    assert res is not None and res.n_matched == 2
    # without directionality this is a non-specific 2-of-3 match whose free roll would smear the
    # unmatched hydrophobe -> deliberately rejected even with two_feature on
    assert align_features(probe, ref, dist_tol=0.5, min_clique=3,
                          use_directions=False, two_feature=True) is None


def test_two_feature_never_downgrades_a_full_clique():
    ref = _cloud()
    res = align_features(_rigid_copy(ref), ref, dist_tol=0.5, min_clique=3, two_feature=True)
    assert res is not None and res.n_matched == 4      # the full clique still out-ranks any pair


def test_seed_align_folds_in_two_feature_ligand_when_enabled():
    # A minimal two-feature compound matching two of the seed frame's features is dropped under the
    # strict floor but folded in once two_feature is enabled (recovering two-point pharmacophores).
    ref = _cloud()
    seed = _seed(ref, "seedA")
    mini = _rigid_copy([("PosIonizable", np.array([3.0, 0.0, 0.0]), None),
                        ("Acceptor", np.array([0.0, 4.0, 0.0]), np.array([0.0, 1.0, 0.0]))])
    kw = dict(dist_tol=0.5, min_clique=3, membership_radius=1.5, max_align_rmsd=1.5,
              use_directions=True)
    off = seed_align(seed, [("mini", [mini])], **kw)
    on = seed_align(seed, [("mini", [mini])], two_feature=True, **kw)
    assert not {r.ligand_id: r for r in off.manifest}["mini"].aligned
    assert {r.ligand_id: r for r in on.manifest}["mini"].aligned


def test_axial_mean_does_not_cancel_opposite_normals():
    # Aromatic ring normals are sign-ambiguous: opposite faces must reinforce ONE axis, not cancel.
    up, down = np.array([0.0, 0.0, 1.0]), np.array([0.0, 0.0, -1.0])
    plain = np.mean([up, down], axis=0)
    assert np.linalg.norm(plain) < 1e-9                       # naive mean cancels to ~zero
    ax = _axial_mean_direction([up, down, up])
    assert ax is not None and abs(abs(ax[2]) - 1.0) < 1e-9    # axial mean recovers the z-axis
    # dispatcher: Aromatic -> axial, Donor -> plain (opposite donors DO cancel, correctly)
    assert _slot_direction("Aromatic", [up, down]) is not None
    assert _slot_direction("Donor", [up, down]) is None


def test_slot_direction_aromatic_output_is_stable_under_flips():
    # A consensus ring normal must be recoverable whatever each contributor's perceived sign.
    base = np.array([0.3, 0.0, 0.95])
    base /= np.linalg.norm(base)
    flipped = [base if i % 2 else -base for i in range(6)]
    md = _slot_direction("Aromatic", flipped)
    assert md is not None and abs(abs(float(np.dot(md, base))) - 1.0) < 1e-6


def test_aromatic_axial_matching_penalises_ring_plane_mismatch():
    # cation + aromatic + acceptor, all three matched. With aromatic_axial on, a probe whose ring
    # plane is tilted vs the reference aligns worse (higher RMSD) than one whose ring plane matches;
    # the sign of the normal is irrelevant (opposite ring faces are the same axis).
    ref = [("PosIonizable", np.array([0.0, 0.0, 0.0]), None),
           ("Aromatic", np.array([5.0, 0.0, 0.0]), np.array([0.0, 0.0, 1.0])),
           ("Acceptor", np.array([0.0, 5.0, 0.0]), None)]
    aligned = [("PosIonizable", np.array([0.0, 0.0, 0.0]), None),
               ("Aromatic", np.array([5.0, 0.0, 0.0]), np.array([0.0, 0.0, -1.0])),  # opposite face
               ("Acceptor", np.array([0.0, 5.0, 0.0]), None)]
    tilted = [("PosIonizable", np.array([0.0, 0.0, 0.0]), None),
              ("Aromatic", np.array([5.0, 0.0, 0.0]), np.array([0.0, 0.8, 0.6])),     # tilted plane
              ("Acceptor", np.array([0.0, 5.0, 0.0]), None)]
    ka = align_features(aligned, ref, dist_tol=0.5, min_clique=3,
                        use_directions=True, aromatic_axial=True)
    kt = align_features(tilted, ref, dist_tol=0.5, min_clique=3,
                        use_directions=True, aromatic_axial=True)
    assert ka.rmsd < 1e-6                       # opposite-face normal is treated as the same axis
    assert kt.rmsd > ka.rmsd + 0.3              # a genuinely tilted ring plane is penalised
    # with axial matching off, the ring normal does not enter the fit at all
    off = align_features(tilted, ref, dist_tol=0.5, min_clique=3,
                         use_directions=True, aromatic_axial=False)
    assert off.rmsd < 1e-6


def test_consolidate_merges_within_radius_and_means_direction():
    pts = [("A", np.array([0.0, 0.0, 0.0]), np.array([1.0, 0.0, 0.0])),
           ("A", np.array([0.5, 0.0, 0.0]), np.array([1.0, 0.0, 0.0])),
           ("A", np.array([5.0, 0.0, 0.0]), None)]
    ref = consolidate(pts, radius=1.0)
    assert len(ref) == 2                            # two clusters: {0,0.5} and {5}
    near = next(r for r in ref if np.linalg.norm(r[1]) < 1.0)
    assert np.allclose(near[2], [1.0, 0.0, 0.0])    # mean unit direction


def test_seed_align_pools_and_updates():
    ref = _cloud()
    seed = _seed(ref, "seedA")
    good = _rigid_copy(ref)
    junk = [("Aromatic", np.array([100.0, 0.0, 0.0]), None),
            ("Donor", np.array([100.0, 0.0, 5.0]), None)]
    lone = [[("Aromatic", np.array([0.0, 0.0, 0.0]), None)]]
    res = seed_align(seed, [("good", [junk, good]), ("dropped", lone)],
                     dist_tol=0.5, min_clique=3, membership_radius=1.5)
    by_lig = {r.ligand_id: r for r in res.manifest}
    assert by_lig["seedA"].source == "seed"
    assert by_lig["good"].aligned and by_lig["good"].n_matched == 4
    assert not by_lig["dropped"].aligned
    assert "good" in res.transforms and "dropped" not in res.transforms
    good_pts = [xyz for fam, xyz, d, lig, rigid in res.points if lig == "good"]
    assert good_pts and all(np.linalg.norm(p) < 8.0 for p in good_pts)


def test_seed_align_rmsd_gate_rejects_poor_fit():
    ref = _cloud()
    seed = _seed(ref, "seedA")
    distorted = _rigid_copy(ref)
    distorted[2] = (distorted[2][0], distorted[2][1] + np.array([2.0, 0.0, 0.0]), None)
    strict = seed_align(seed, [("d", [distorted])],
                        dist_tol=2.0, min_clique=3, membership_radius=1.5, max_align_rmsd=0.5)
    loose = seed_align(seed, [("d", [distorted])],
                       dist_tol=2.0, min_clique=3, membership_radius=1.5, max_align_rmsd=None)
    assert not {r.ligand_id: r for r in strict.manifest}["d"].aligned
    assert {r.ligand_id: r for r in loose.manifest}["d"].aligned


def test_seed_align_is_deterministic():
    ref = _cloud()
    seed = _seed(ref, "seedA")
    compounds = [("a", [_rigid_copy(ref)]),
                 ("b", [_rigid_copy(ref, trans=np.array([2.0, 1.0, -1.0]))])]
    kw = dict(dist_tol=0.5, min_clique=3, membership_radius=1.5, max_align_rmsd=1.5)
    r1 = seed_align(seed, compounds, **kw)
    r2 = seed_align(seed, compounds, **kw)
    assert [(f, tuple(np.round(x, 6)), lig) for f, x, d, lig, rg in r1.points] == \
           [(f, tuple(np.round(x, 6)), lig) for f, x, d, lig, rg in r2.points]
    assert [(m.ligand_id, m.aligned, m.n_matched) for m in r1.manifest] == \
           [(m.ligand_id, m.aligned, m.n_matched) for m in r2.manifest]


def test_em_converges_and_is_deterministic():
    ref = _cloud()
    seed = _seed(ref, "seedA")
    compounds = [("a", [_rigid_copy(ref)]),
                 ("b", [_rigid_copy(ref, trans=np.array([1.0, 2.0, -1.0]))]),
                 ("c", [_rigid_copy(ref, rot=np.eye(3), trans=np.array([0.5, 0.0, 0.0]))])]
    kw = dict(dist_tol=0.5, min_clique=3, membership_radius=1.5, max_align_rmsd=1.5)
    r1 = seed_align(seed, compounds, em_iterations=5, em_tol=0.05, **kw)
    r2 = seed_align(seed, compounds, em_iterations=5, em_tol=0.05, **kw)
    assert r1.convergence, "EM should record at least one iteration"
    assert r1.convergence[-1][1] < 0.05
    assert r1.convergence[-1][1] <= r1.convergence[0][1] + 1e-9
    assert [c[:2] for c in r1.convergence] == [c[:2] for c in r2.convergence]


def test_seedless_recovers_same_consensus_as_correct_seed():
    ref = _cloud()
    compounds = [(f"m{i}", [_rigid_copy(ref, trans=np.array([0.3 * i, -0.2 * i, 0.1 * i]))])
                 for i in range(6)]
    kw = dict(dist_tol=0.5, min_clique=3, membership_radius=1.5, max_align_rmsd=2.0,
              em_iterations=8, em_tol=0.02)
    seeded = seed_align(_seed(ref, "seed"), compounds, **kw)
    seedless = seed_align(_seed(compounds[0][1][0], "m0"), compounds, **kw)

    def internal(res):
        pts = {}
        for fam, xyz, _d, _lig, _rigid in res.points:
            pts.setdefault(fam, []).append(xyz)
        c = {f: np.mean(v, axis=0) for f, v in pts.items()}
        return float(np.linalg.norm(c["Aromatic"] - c["PosIonizable"]))
    assert abs(internal(seeded) - internal(seedless)) < 0.5


def test_generate_conformers_returns_energy_window():
    cfg = AlignmentConfig(n_conformers=16, max_confs=8)
    out = generate_conformers("c1ccncc1CC[NH3+]", cfg)   # a small flexible cation
    assert out is not None
    mol, cids, energies = out
    assert 1 <= len(cids) <= cfg.max_confs
    assert mol.GetNumConformers() >= len(cids)
    assert set(energies) == set(cids)
    assert all(0.0 <= e <= cfg.energy_window + 1e-6 for e in energies.values())


def test_conformer_features_perceive_directions():
    from pharmpipe.features.extract import conformer_features, feature_factory

    cfg = AlignmentConfig(n_conformers=4, max_confs=2)
    mol, cids, _ = generate_conformers("c1ccncc1", cfg)      # pyridine: aromatic + acceptor N
    fac = feature_factory("base")
    feats = conformer_features(mol, fac, ["Aromatic", "Acceptor"], [], conf_id=cids[0])
    fams = {f for f, _, _ in feats}
    assert "Acceptor" in fams and "Aromatic" in fams
    acc = next(d for f, _, d in feats if f == "Acceptor")
    assert acc is not None and abs(np.linalg.norm(acc) - 1.0) < 1e-6   # unit lone-pair vector


def test_generate_conformers_bad_smiles():
    assert generate_conformers("not_a_smiles", AlignmentConfig()) is None


def test_write_aligned_sdf_applies_transform_and_tags(tmp_path):
    from rdkit import Chem
    from rdkit.Chem import AllChem

    from pharmpipe.pharmacophore.io import write_aligned_sdf

    mol = Chem.AddHs(Chem.MolFromSmiles("c1ccncc1"))
    AllChem.EmbedMolecule(mol, randomSeed=1)
    trans = np.array([10.0, 0.0, 0.0])
    out = write_aligned_sdf([(mol, 0, _ROT, trans, {"mol_id": "x", "drugclip_rank": 1})],
                            tmp_path / "aligned.sdf")
    got = [m for m in Chem.SDMolSupplier(str(out), removeHs=False) if m is not None]
    assert len(got) == 1
    assert got[0].GetProp("mol_id") == "x" and got[0].GetProp("drugclip_rank") == "1"
    orig_c = mol.GetConformer().GetPositions().mean(0)
    new_c = got[0].GetConformer().GetPositions().mean(0)
    assert abs((new_c - (orig_c @ _ROT.T + trans))[0]) < 1e-3


# --- seed-vs-seedless quality comparison (pure) ------------------------------

def _manifest(aligned_rmsds, n_dropped=0, n_matched=4, with_seed=True):
    """A manifest: one seed row, ``len(aligned_rmsds)`` aligned rows, ``n_dropped`` dropped rows."""
    rows = []
    if with_seed:
        rows.append(AlignRecord("seed0", "seed", 0, -1, 0, float("nan"), True))
    for i, r in enumerate(aligned_rmsds):
        rows.append(AlignRecord(f"h{i}", "aligned", 5, 0, n_matched, r, True))
    for j in range(n_dropped):
        rows.append(AlignRecord(f"d{j}", "aligned", 5, -1, 0, float("nan"), False))
    return rows


def test_alignment_quality_ignores_seed_rows_and_drops():
    q = alignment_quality("seed", _manifest([0.5, 1.0, 1.5], n_dropped=1, n_matched=6))
    assert q.n_attempted == 4 and q.n_aligned == 3      # seed row excluded; 1 drop counted
    assert q.coverage == 0.75
    assert q.median_rmsd == 1.0                          # median over aligned rmsds
    assert q.mean_matched == 6.0


def test_alignment_quality_empty_is_safe():
    q = alignment_quality("seedless", _manifest([], n_dropped=0))
    assert q.n_aligned == 0 and q.coverage == 0.0
    assert q.median_rmsd != q.median_rmsd                # NaN when nothing aligned


def test_compare_coverage_dominates_when_seed_drops_compounds():
    seed = alignment_quality("seed", _manifest([0.8] * 20, n_dropped=10))    # 20/30
    seedless = alignment_quality("seedless", _manifest([1.0] * 29, n_dropped=1))  # 29/30
    assert compare_alignments(seed, seedless).winner == "seedless"


def test_compare_rmsd_breaks_a_coverage_tie():
    seed = alignment_quality("seed", _manifest([0.7] * 30))
    seedless = alignment_quality("seedless", _manifest([1.3] * 30))
    assert compare_alignments(seed, seedless).winner == "seed"          # equal coverage, tighter


def test_compare_within_margins_is_comparable():
    # seedless +1 (its bootstrap self-alignment) and a 0.05 A RMSD gap are both inside the margins.
    seed = alignment_quality("seed", _manifest([1.00] * 29))
    seedless = alignment_quality("seedless", _manifest([1.05] * 30))
    assert compare_alignments(seed, seedless).winner == "comparable"


def test_compare_ignores_match_count_inflation():
    # The degenerate-flip case: seedless matches MORE features but folds in FEWER compounds.
    # Coverage-first must still pick the seed (match count is deliberately not a tie-breaker).
    seed = alignment_quality("seed", _manifest([0.6] * 12, n_dropped=0, n_matched=6))
    seedless = alignment_quality("seedless", _manifest([0.6] * 8, n_dropped=4, n_matched=9))
    assert seedless.mean_matched > seed.mean_matched
    assert compare_alignments(seed, seedless).winner == "seed"


# --- direction rigidity (conformer-ensemble flexibility) ---------------------

def _conf(donor_dir, acc_dir=(0.0, 1.0, 0.0)):
    """One conformer cloud: a fixed aromatic + acceptor, and a Donor whose vector we vary to
    simulate a rotor (the O-H swinging between conformers)."""
    return [("Aromatic", np.array([0.0, 0.0, 0.0]), np.array([0.0, 0.0, 1.0])),
            ("Acceptor", np.array([2.0, 0.0, 0.0]), np.array(acc_dir, dtype=float)),
            ("Donor", np.array([0.0, 2.0, 0.0]), np.array(donor_dir, dtype=float))]


def test_direction_rigidity_flags_a_rotor_flexible_and_a_fixed_group_rigid():
    # Same feature centres across conformers (so superposition is identity); the Donor direction
    # swings widely (a free rotor) while the Acceptor/Aromatic directions are constant.
    clouds = [_conf(donor_dir=d) for d in
              [(0, 0, 1), (0, 1, 0), (1, 0, 0), (0, -1, 0), (-1, 0, 0)]]
    rigid = direction_rigidity(clouds, rigid_r=0.9)
    fams = [c[0] for c in clouds[0]]
    assert rigid[fams.index("Aromatic")] is True      # constant normal
    assert rigid[fams.index("Acceptor")] is True       # constant lone pair
    assert rigid[fams.index("Donor")] is False         # scattered -> flexible


def test_direction_rigidity_single_conformer_is_rigid():
    # No sampled rotational freedom -> a lone conformer's directions are determined (R = 1).
    rigid = direction_rigidity([_conf(donor_dir=(0, 0, 1))], rigid_r=0.9)
    assert all(r for r, c in zip(rigid, _conf((0, 0, 1)), strict=True) if c[2] is not None)


def test_direction_rigidity_marks_nondirectional_false():
    clouds = [[("LumpedHydrophobe", np.array([0.0, 0.0, 0.0]), None)]]
    assert direction_rigidity(clouds, rigid_r=0.9) == [False]


def test_seed_align_tags_points_with_rigidity():
    # A rigid probe (all directions constant across its 2 conformers) aligns and its emitted points
    # carry rigid=True for directional features.
    ref = _cloud(acc_dir=np.array([0.0, 1.0, 0.0]))
    seed = _seed(ref, "seedA")
    probe = _rigid_copy(ref)
    res = seed_align(seed, [("p", [probe, probe])], dist_tol=0.5, min_clique=3,
                     membership_radius=1.5, use_directions=True, direction_rigid_r=0.9)
    pts = [(fam, rigid) for fam, _x, d, lig, rigid in res.points if lig == "p" and d is not None]
    assert pts and all(rigid for _fam, rigid in pts)   # constant directions -> rigid
    # seed points are always rigid=False
    assert all(rigid is False for *_1, lig, rigid in res.points if lig == "seedA")
