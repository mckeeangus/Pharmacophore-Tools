"""Unit tests for Stage 3 — pure logic, no network or structure IO."""

from __future__ import annotations

import json
from pathlib import Path

from pharmpipe.groups import pocket, resolve
from pharmpipe.groups.efficacy import EfficacyCall, load_efficacy
from pharmpipe.groups.group import Pose, representative_poses
from pharmpipe.groups.pockets import load_pockets

# --- geometry / clustering ---------------------------------------------------

def test_overlap_metrics():
    a = frozenset({"A1", "A2", "A3", "A4"})
    b = frozenset({"A1", "A2"})
    assert pocket.jaccard(a, b) == 2 / 4
    # overlap coefficient rescues a small set nested in a larger one
    assert pocket.overlap_coefficient(a, b) == 1.0


def test_cluster_separates_distinct_pockets():
    site1 = frozenset({f"R{i}" for i in range(10)})
    site1b = frozenset({f"R{i}" for i in range(1, 11)})        # overlaps site1
    site2 = frozenset({f"Q{i}" for i in range(10)})            # disjoint
    labels = pocket.cluster_fingerprints([site1, site1b, site2])
    assert labels[0] == labels[1]          # same pocket
    assert labels[2] != labels[0]          # distinct pocket


def test_cluster_orders_by_size():
    big = [frozenset({f"R{i}" for i in range(8)}) for _ in range(3)]
    small = [frozenset({f"Q{i}" for i in range(8)})]
    labels = pocket.cluster_fingerprints(big + small)
    # largest cluster is id 0
    assert labels[:3] == [0, 0, 0]
    assert labels[3] == 1


def test_consensus_residues():
    fps = [frozenset({"A1", "A2", "A3"}), frozenset({"A1", "A2", "B9"})]
    # require >50%: only residues contacted by both poses survive
    cons = pocket.consensus_residues(fps, [0, 1], frac=0.75)
    assert cons == {"A1", "A2"}


# --- config: efficacy --------------------------------------------------------

def test_efficacy_default_and_overrides():
    ec = load_efficacy()
    cdk2 = ec.get("cdk2")
    # control target default applies to an unlisted ligand
    assert cdk2.call("ZZZ").efficacy == "negative"
    # ATP is routed to separate-state (cofactor)
    assert cdk2.call("ATP").is_separate_state
    # multi-effect target: unlisted ligand is unknown, not defaulted
    esr1 = ec.get("esr1")
    assert esr1.call("ZZZ").is_unknown
    assert esr1.call("EST").efficacy == "positive"
    assert esr1.call("OHT").efficacy == "negative"


def test_efficacy_unknown_target_resolves():
    ec = load_efficacy()
    teff = ec.get("does_not_exist")
    assert teff.call("ABC").is_unknown


# --- config: pockets ---------------------------------------------------------

def test_pockets_markers_and_collapse():
    pc = load_pockets()
    gaba = pc.get("gaba_a")
    assert gaba.primary_label == "orthosteric"
    assert gaba.label_for_markers({"DZP"}) == "bzd_site"
    assert gaba.label_for_markers({"ABU"}) is None      # orthosteric has no marker
    nachr = pc.get("nachr_a4b2")
    assert nachr.collapse_to_primary is True


def test_nachr_accessory_marker_defined():
    nachr = load_pockets().get("nachr_a4b2")
    # NS9283 (NSE) is the diagnostic marker of the accessory PAM site.
    assert nachr.label_for_markers({"NSE"}) == "accessory"
    assert "accessory" in nachr.expected_pockets


def test_marker_override_pulls_pose_from_collapsed_primary():
    """A marker HET whose geometry merges with the primary pocket is still placed
    at its curated secondary site (the nAChR accessory-vs-orthosteric case)."""
    from pharmpipe.groups.group import _assign_clusters
    from pharmpipe.groups.pockets import PocketDef, PocketDefaults

    shared = {f"R{i}" for i in range(8)}                    # one geometric cluster
    poses = [
        Pose("1AAA", "ACH", "A", "1", Path("a.mol2"), fingerprint=frozenset(shared)),
        Pose("2BBB", "NCT", "A", "1", Path("b.mol2"), fingerprint=frozenset(shared)),
        Pose("3CCC", "XRS", "A", "1", Path("c.mol2"), fingerprint=frozenset(shared)),
        # NS9283 shares the orthosteric aromatic box, so it merges into cluster 0…
        Pose("4NZB", "NSE", "A", "1", Path("d.mol2"), fingerprint=frozenset(shared)),
    ]
    pdef = PocketDef(slug="nachr_a4b2", primary_label="orthosteric",
                     collapse_to_primary=True, expected_pockets=["orthosteric", "accessory"],
                     markers={"accessory": ["NSE"]})
    clusters = _assign_clusters(poses, pdef, PocketDefaults())
    by_het = {p.het_code: p.pocket for p in poses}
    assert by_het["ACH"] == "orthosteric"
    assert by_het["NCT"] == "orthosteric"
    # …but the curator marker overrides it back out of the primary pocket.
    assert by_het["NSE"] == "accessory"
    assert {c.label for c in clusters} == {"orthosteric", "accessory"}


def test_every_target_has_pocket_and_efficacy_config():
    pc = load_pockets()
    ec = load_efficacy()
    slugs = ["nachr_a4b2", "esr1", "hiv1_protease", "adrb2", "cdk2", "ca2",
             "ache", "cavab", "cox2", "hmgcr", "gaba_a", "net_slc6a2"]
    for slug in slugs:
        assert pc.get(slug).primary_label              # defined (non-empty)
        assert ec.get(slug).slug == slug


def test_adrb2_collapsed_gaba_realign_flags():
    pc = load_pockets()
    assert pc.get("adrb2").collapse_to_primary is True
    assert pc.get("gaba_a").realign_global is True
    assert pc.get("nachr_a4b2").realign_global is False


# --- Stage 3.3: ChEMBL resolution (pure logic) -------------------------------

def test_action_type_to_sign():
    assert resolve._sign_from_actions({"AGONIST"}) == ("positive", "high")
    assert resolve._sign_from_actions({"ANTAGONIST"}) == ("neutral", "high")
    assert resolve._sign_from_actions({"INHIBITOR"}) == ("negative", "high")
    # conflicting subtype mechanisms -> unknown, never crossed
    assert resolve._sign_from_actions({"AGONIST", "ANTAGONIST"})[0] == "unknown"
    # unmapped action -> unknown
    assert resolve._sign_from_actions({"MODULATOR (UNSPECIFIED)"})[0] == "unknown"


def test_het_inchikey_index_offline(tmp_path):
    base = tmp_path / "rcsb_chemcomp"
    base.mkdir()
    (base / "x.json").write_text(json.dumps({
        "chem_comp": {"id": "ABC"},
        "rcsb_chem_comp_descriptor": {"InChIKey": "AAAAAAAAAAAAAA-BBBBBBBBBB-N"},
    }), encoding="utf-8")
    idx = resolve.build_het_inchikey_index(cache_dir=tmp_path)
    assert idx["ABC"] == "AAAAAAAAAAAAAA-BBBBBBBBBB-N"


# --- representative de-duplication -------------------------------------------

def _pose(pdb, het, res, rmsd=1.0):
    return Pose(pdb_id=pdb, het_code=het, chain="A", seqid="1",
                aligned_mol2=Path(f"{pdb}_{het}.mol2"), resolution=res, pocket_rmsd=rmsd)


def test_representative_poses_picks_best_resolution():
    poses = [_pose("AAAA", "LIG", 2.5), _pose("BBBB", "LIG", 1.4), _pose("CCCC", "OTH", 3.0)]
    reps = representative_poses(poses)
    by_het = {p.het_code: p for p in reps}
    assert len(reps) == 2                       # one per HET
    assert by_het["LIG"].pdb_id == "BBBB"       # best (lowest) resolution wins


# --- resolved CSV merge (fallback below curated config) ----------------------

def test_resolved_fallback_below_config():
    ec = load_efficacy()
    teff = ec.get("net_slc6a2")
    teff.resolved = {"ZZZ": EfficacyCall("negative", "reversible", source="chembl (high)")}
    # curated entry still wins
    assert teff.call("COC").efficacy == "negative" and "chembl" not in teff.call("COC").source
    # an otherwise-unknown het is filled from the resolved map
    assert teff.call("ZZZ").efficacy == "negative"
    assert "chembl" in teff.call("ZZZ").source
