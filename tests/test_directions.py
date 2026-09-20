"""Regression test: a build-from-molecules run must populate feature directions — offline.

The align -> build chain feeds ``build-pharmacophore`` an aligned SDF, which builds via
``build_from_molecules``. Directions (dx,dy,dz in the interchange CSV, the viz arrows) must be
carried into the consensus features; a prior regression left every direction ``None`` on this path.
"""

from __future__ import annotations

from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Geometry import Point3D

from pharmpipe.features.load import LoadReport
from pharmpipe.pharmacophore.config import load_pharmacophore_config
from pharmpipe.pharmacophore.io import read_model_csv
from pharmpipe.pharmacophore.run import _consensus_direction, build_from_molecules


def test_consensus_direction_concentration():
    # agreeing vectors -> R ~ 1 (a direction is well defined); an isotropic scatter -> R ~ 0
    # (no direction — the freely-rotating-hydroxyl case the threshold is meant to drop).
    _, r_tight = _consensus_direction("Donor", [(0.0, 0.0, 1.0)] * 5)
    assert r_tight > 0.99
    iso = [(1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1)]
    _, r_scatter = _consensus_direction("Donor", iso)
    assert r_scatter < 0.01
    # aromatic normals are folded to a hemisphere, so opposite faces reinforce rather than cancel
    _, r_axis = _consensus_direction("Aromatic", [(0.0, 0.0, 1.0), (0.0, 0.0, -1.0)])
    assert r_axis > 0.99


def _pyridine(offset: float):
    """Pyridine (aromatic + acceptor N, explicit H), translated from a fixed embedded pose."""
    mol = Chem.AddHs(Chem.MolFromSmiles("c1ccncc1"))
    AllChem.EmbedMolecule(mol, randomSeed=1)
    conf = mol.GetConformer()
    for i in range(mol.GetNumAtoms()):
        p = conf.GetAtomPosition(i)
        conf.SetAtomPosition(i, Point3D(p.x + offset, p.y, p.z))
    return mol


def test_build_from_molecules_populates_directions(tmp_path):
    molecules = [(f"m{i}", _pyridine(0.1 * i)) for i in range(6)]  # within membership radius
    cfg = load_pharmacophore_config(None)
    res = build_from_molecules(molecules, LoadReport(), tmp_path, cfg,
                               source={"n_ligands": len(molecules)}, name="t")
    assert res is not None
    directional = {"Donor", "Acceptor", "Aromatic"}
    with_dir = [f for f in res.pharmacophore.features
                if f.family in directional and f.direction is not None]
    assert with_dir, "no directional feature carried a direction"
    for f in with_dir:
        assert abs(sum(c * c for c in f.direction) - 1.0) < 1e-6  # unit vector
        # a reported direction carries its concentration R in (0, 1] (aligned pyridines -> high)
        assert f.direction_r is not None and 0.0 < f.direction_r <= 1.0

    # the direction AND its R must survive into the interchange CSV (the viz reads dx,dy,dz,dr)
    back = read_model_csv(tmp_path / "pharmacophore.csv")
    assert any(f.direction is not None and f.direction_r is not None for f in back.features)
