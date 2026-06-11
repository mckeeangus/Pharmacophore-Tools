"""Curation logic: additives dropped, cofactors kept, metals flagged."""

from pharmpipe.pdb import exclusions


def test_water_excluded():
    d = exclusions.classify("HOH")
    assert not d.keep and d.category == "water"


def test_common_additives_excluded():
    for cid in ["GOL", "EDO", "SO4", "PO4", "ACT", "DMS", "MES", "TRS", "FMT",
                "CL", "NA", "K", "PEG", "PG4", "LMT", "PX4", "NAG"]:
        d = exclusions.classify(cid)
        assert not d.keep, f"{cid} should be excluded"


def test_cofactors_kept():
    for cid in ["HEM", "FAD", "NAD", "ATP", "ADP", "SF4", "PLP", "COA"]:
        d = exclusions.classify(cid)
        assert d.keep and d.category == "cofactor", f"{cid} should be a kept cofactor"


def test_catalytic_metals_kept_and_flagged():
    # Zn (carbonic anhydrase), Ca (CavAb), Fe — kept but surfaced for review.
    for cid in ["ZN", "CA", "FE", "MN", "CU"]:
        d = exclusions.classify(cid)
        assert d.keep and d.flagged and d.category == "metal", f"{cid} should be flagged"


def test_drug_like_ligand_kept():
    d = exclusions.classify("STI")  # imatinib
    assert d.keep and d.category == "ligand"


def test_per_target_overrides():
    assert not exclusions.classify("ATP", extra_exclude={"ATP"}).keep
    assert exclusions.classify("GOL", extra_keep={"GOL"}).keep
