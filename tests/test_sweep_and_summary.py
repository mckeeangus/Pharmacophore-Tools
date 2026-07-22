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

def test_read_clusters_support_uses_membership_radius(tmp_path):
    mod = _load_script("pymol_pharmacophore")
    csv_path = tmp_path / "features.csv"
    csv_path.write_text(
        "family,ligand_id,x,y,z,cluster,kept\n"
        "Donor,L1,0,0,0,0,1\n"
        "Donor,L2,0.3,0,0,0,1\n"
        "Donor,L3,0,0.3,0,0,1\n"      # 3 ligands cluster tightly near the origin
        "Donor,L4,9,0,0,7,0\n"        # L4's only Donor point is far -> outside the radius
        "Acceptor,L1,10,0,0,1,0\n",   # lone Acceptor -> dropped by min_cluster_size=2
        encoding="utf-8")

    clusters = mod._read_clusters(str(csv_path), n_ligands=4, membership_radius=1.5,
                                  min_cluster_size=2)
    assert len(clusters) == 1                       # the two singletons are dropped
    (c,) = clusters
    assert c["family"] == "Donor"
    # L1/L2/L3 fall within 1.5 A of the centre; the far L4 point does not -> 3/4.
    assert abs(c["support"] - 0.75) < 1e-9


# --- model_summary tables --------------------------------------------------------------

def test_summary_reports_merged_away_and_uncapped_occupancy(tmp_path):
    kept = PharmacophoreFeature("Donor", 0.0, 0.0, 0.0, radius=2.2,
                                n_points=20, n_ligands=14, support=1.0, label="Donor 1")
    record = MergeRecord(dropped_family="Acceptor", dropped_points=11, dropped_ligands=8,
                         dropped_support=0.69, dropped_cluster_label=3,
                         winner_family="Donor", winner_cluster_label=0,
                         winner_label="Donor 1")
    ph = Pharmacophore("cell", [kept],
                       metadata={"consensus_method": "density", "representative_ligand": "L1"})
    result = BuildResult(pharmacophore=ph, assignments=[], merged_away=[record])
    report = LoadReport(by_method={"template": 14}, skipped=[])

    out = tmp_path / "model_summary.md"
    _write_summary(result, report, 14, 1.5, out)
    text = out.read_text(encoding="utf-8")

    assert "## Merged away" in text
    assert "In favour of" in text and "Donor 1" in text
    assert "Occupancy" in text and "Mean support" not in text
    assert "1.43" in text          # kept Donor 1: 20 / 14, uncapped
    assert "1.38" in text          # merged Acceptor: 11 / 8, uncapped
