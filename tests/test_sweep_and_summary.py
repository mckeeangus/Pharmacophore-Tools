"""Tests for the occupancy-sweep cluster helper and the model_summary tables — offline.

Covers the pure ``_read_clusters`` from ``scripts/pymol_pharmacophore.py`` (imported
without PyMOL) and the ``_write_summary`` Merged-away / Support / Occupancy output.
"""

from __future__ import annotations

import importlib.util
from pathlib import Path

from pharmpipe.features.load import LoadReport
from pharmpipe.pharmacophore.build import BuildResult, MergeRecord
from pharmpipe.pharmacophore.model import Pharmacophore, PharmacophoreFeature
from pharmpipe.pharmacophore.run import _write_summary

REPO = Path(__file__).resolve().parents[1]


def _load_script(name: str):
    """Import a repo ``scripts/*.py`` by path (PyMOL import is guarded, so this works)."""
    spec = importlib.util.spec_from_file_location(name, REPO / "scripts" / f"{name}.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


# --- occupancy-sweep cluster helper ----------------------------------------------------

def test_read_clusters_occupancy_uncapped_and_min_size(tmp_path):
    mod = _load_script("pymol_pharmacophore")
    csv_path = tmp_path / "features.csv"
    csv_path.write_text(
        "family,ligand_id,x,y,z,cluster,kept\n"
        "Donor,L1,0,0,0,0,1\n"
        "Donor,L2,2,0,0,0,1\n"
        "Donor,L1,1,0,0,0,1\n"       # L1 gives 2 points -> 3 points / 2 ligands = 1.5
        "Acceptor,L3,10,0,0,1,0\n",  # lone point -> dropped by min_cluster_size=2
        encoding="utf-8")

    clusters = mod._read_clusters(str(csv_path), min_cluster_size=2)
    assert len(clusters) == 1                       # the singleton Acceptor is dropped
    (c,) = clusters
    assert c["family"] == "Donor"
    assert abs(c["occ"] - 1.5) < 1e-9               # occupancy > 1, uncapped
    assert abs(c["x"] - 1.0) < 1e-9                 # centroid of x = (0+2+1)/3


# --- model_summary tables --------------------------------------------------------------

def test_summary_reports_merged_away_and_uncapped_occupancy(tmp_path):
    kept = PharmacophoreFeature("Donor", 0.0, 0.0, 0.0, radius=2.2,
                                n_points=20, n_ligands=14, support=1.0, label="Donor 1")
    record = MergeRecord(dropped_family="Acceptor", dropped_points=11, dropped_ligands=8,
                         dropped_support=0.69, dropped_cluster_label=3,
                         winner_family="Donor", winner_cluster_label=0,
                         winner_label="Donor 1")
    ph = Pharmacophore("cell", [kept],
                       metadata={"consensus_method": "kmeans", "representative_ligand": "L1"})
    result = BuildResult(pharmacophore=ph, assignments=[], merged_away=[record])
    report = LoadReport(by_method={"template": 14}, skipped=[])

    out = tmp_path / "model_summary.md"
    _write_summary(result, report, 14, out)
    text = out.read_text(encoding="utf-8")

    assert "## Merged away" in text
    assert "In favour of" in text and "Donor 1" in text
    assert "Occupancy" in text and "Mean support" not in text
    assert "1.43" in text          # kept Donor 1: 20 / 14, uncapped
    assert "1.38" in text          # merged Acceptor: 11 / 8, uncapped
