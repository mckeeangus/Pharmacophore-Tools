"""Unit tests for the docked-seed feature-alignment core (Stage 4, offline, pure)."""

from __future__ import annotations

import numpy as np

from pharmpipe.features.conformers import generate_conformers
from pharmpipe.pharmacophore.align import (
    align_features,
    consolidate,
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
    good_pts = [xyz for fam, xyz, d, lig in res.points if lig == "good"]
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
    assert [(f, tuple(np.round(x, 6)), lig) for f, x, d, lig in r1.points] == \
           [(f, tuple(np.round(x, 6)), lig) for f, x, d, lig in r2.points]
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
        for fam, xyz, _d, _lig in res.points:
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
