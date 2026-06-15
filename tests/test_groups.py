"""Unit tests for Stage 3 — pure logic, no network or structure IO."""

from __future__ import annotations

from pharmpipe.groups import pocket
from pharmpipe.groups.efficacy import load_efficacy
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


def test_every_target_has_pocket_and_efficacy_config():
    pc = load_pockets()
    ec = load_efficacy()
    slugs = ["nachr_a4b2", "esr1", "hiv1_protease", "adrb2", "cdk2", "ca2",
             "ache", "cavab", "cox2", "hmgcr", "gaba_a", "net_slc6a2"]
    for slug in slugs:
        assert pc.get(slug).primary_label              # defined (non-empty)
        assert ec.get(slug).slug == slug
