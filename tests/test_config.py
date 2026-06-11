"""Config loading + mol2 instance naming (offline)."""

from pharmpipe.config import load_config
from pharmpipe.io.mol2 import instance_filename
from pharmpipe.pdb.rcsb import LigandInstance
from pharmpipe.util.paths import CONFIG_DIR


def test_load_targets_yaml():
    cfg = load_config(CONFIG_DIR / "targets.yaml")
    slugs = {t.slug for t in cfg.targets}
    assert {"ca2", "cdk2", "esr1", "cavab", "net_slc6a2"} <= slugs
    assert cfg.search.organism_policy == "human_preferred"
    assert cfg.search.extract_mode in ("all_instances", "representative")


def test_surrogates_parsed():
    cfg = load_config(CONFIG_DIR / "targets.yaml")
    nachr = next(t for t in cfg.targets if t.slug == "nachr_a4b2")
    assert any("AChBP" in s.name for s in nachr.surrogates)
    assert all(s.kind == "surrogate" for s in nachr.surrogates)


def test_instance_filename():
    inst = LigandInstance(pdb_id="1A42", comp_id="BZU", auth_asym_id="A",
                          auth_seq_id="555")
    assert instance_filename(inst) == "1A42_BZU_A555.mol2"
