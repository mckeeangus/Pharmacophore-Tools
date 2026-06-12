"""Sites config loads, applies defaults, and covers every scrape target."""

from __future__ import annotations

from pharmpipe.config import load_config
from pharmpipe.sites.config import load_sites
from pharmpipe.util.paths import CONFIG_DIR


def test_sites_load_and_defaults():
    sites = load_sites()
    cox2 = sites.get("cox2")
    assert cox2 is not None
    assert cox2.reference_pdb == "5KIR"
    assert cox2.anchor_het == "RCX"
    # defaults applied when no per-site override
    assert cox2.cutoff_angstrom == 8.0
    assert cox2.min_pocket_atoms == 8


def test_numeric_anchor_kept_as_string():
    # HMG-CoA reductase anchor '117' must survive YAML as a string HET code.
    site = load_sites().get("hmgcr")
    assert site.anchor_het == "117"


def test_every_target_has_a_site():
    cfg = load_config(CONFIG_DIR / "targets.yaml")
    sites = load_sites()
    missing = [t.slug for t in cfg.targets if sites.get(t.slug) is None]
    assert not missing, f"targets without a site definition: {missing}"
