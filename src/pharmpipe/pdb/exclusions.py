"""Curation of bound ligands: drop crystallographic additives, keep real
ligands and genuine cofactors, and *flag* (keep + surface) borderline metals.

Philosophy (per CLAUDE.md): never silently drop something that might be a real
cofactor. Anything not on the additive/water lists is kept. Simple buffer salts
are excluded, but transition/alkaline-earth metals are kept AND flagged so a
human can review them (e.g. the catalytic Zn2+ in carbonic anhydrase, Ca2+ in
CavAb). Known organic cofactors (heme, FAD, NAD, ATP, ...) are kept outright.
"""

from __future__ import annotations

from dataclasses import dataclass

# --- Waters --------------------------------------------------------------
WATERS = {"HOH", "DOD", "WAT"}

# --- Definite crystallographic additives / buffers / cryo / salts --------
# Polyols & cryoprotectants
_CRYO = {
    "GOL", "EDO", "PEG", "PG4", "PGE", "1PE", "2PE", "P6G", "7PE", "12P", "15P",
    "PE3", "PE4", "PE5", "PE8", "PEU", "PG0", "PG5", "PG6", "EGL", "MPD", "BU3",
    "BU1", "MRD", "DOX", "DIO", "TRT", "SBT", "IPA", "MOH", "EOH", "ACN", "DMF",
    "DMS", "TFA", "MES", "SCN", "AZI",
}
# Buffers / weak-acid counter-ions
_BUFFER = {
    "EPE", "TRS", "BIS", "BTB", "MPO", "MOP", "PIN", "HED", "CXS", "TAU", "NHE",
    "CIT", "FLC", "TLA", "TAR", "MLA", "MLI", "MLT", "SIN", "ACY", "ACT", "FMT",
    "CAC", "IMD", "EEE", "POP", "PPV", "BCN", "B3P", "144",
}
# Inorganic salts / simple ions usually from the crystallisation liquor
_SALTS = {
    "SO4", "SUL", "PO4", "PI", "2HP", "3PO", "IPS", "NO3", "NO2", "NH4", "CL",
    "BR", "IOD", "FLO", "F", "NA", "K", "CS", "RB", "LI", "TL", "BF4", "PER",
    "BO4", "B", "BO3", "BEF", "ALF", "AF3", "VO4", "WO4", "MOO", "SE4",
}
# Reducing agents / thiols / misc small additives
_REDUCERS = {"BME", "DTT", "DTU", "DTV", "TCE", "MES", "EDT", "EDO", "OXE"}
# Detergents & lipids (common in GPCR / cryo-EM membrane-protein structures)
_DETERGENTS_LIPIDS = {
    "LMT", "LDA", "LDN", "BOG", "OGA", "BNG", "C8E", "C10", "F09", "P33", "PX4",
    "OLC", "OLA", "OLB", "OLE", "PLM", "MYR", "STE", "PEF", "PEE", "PEV", "PGV",
    "PCW", "PC1", "PC7", "PEH", "PGW", "LHG", "LMG", "LMN", "1N7", "CPS", "CHS",
    "DPC", "FOS", "12M", "13M", "MC3", "Y01", "D10", "D12", "DD9", "JEF", "UMQ",
    "SQU", "SQL", "CLR", "HEZ", "HEX", "HP6", "MES", "BCR", "L2P", "L3P", "L4P",
    "LI1", "PX2", "3PH", "PSC", "POV", "PEK", "DGA", "ACE", "ACT",
    "LPC", "LPE", "LPP", "LP3", "PX6", "PA", "PGT", "PIO", "PSF", "44E",
}
# Covalent glycosylation sugars (not ligands of interest) + common cryo sugars
_GLYCANS_SUGARS = {
    "NAG", "NDG", "BMA", "MAN", "FUC", "FUL", "GAL", "GLA", "GLC", "BGC", "SIA",
    "A2G", "NGA", "XYP", "XYS", "RAM", "SUC", "TRE", "MAL", "LAT", "FRU",
}
# Unknown / placeholder atoms & residues
_UNKNOWN = {"UNK", "UNL", "UNX", "DUM", "0KA"}

ADDITIVES = (_CRYO | _BUFFER | _SALTS | _REDUCERS | _DETERGENTS_LIPIDS
             | _GLYCANS_SUGARS | _UNKNOWN)

# --- Genuine cofactors: ALWAYS keep --------------------------------------
_HEMES = {"HEM", "HEC", "HEA", "HEB", "HEO", "HAS", "DHE", "HE5", "HNI", "HCO",
          "COH", "HIF", "1CP", "HDD", "VEA", "SRM", "MH0", "6HE", "VOV"}
_FLAVINS = {"FAD", "FMN", "FDA", "RBF", "FNS"}
_NICOTINAMIDES = {"NAD", "NAI", "NAP", "NDP", "NAJ", "NAH", "NHD", "NDC"}
_NUCLEOTIDE_LIGANDS = {  # matter for kinases etc. (e.g. CDK2)
    "ATP", "ADP", "AMP", "ANP", "ACP", "AGS", "APC", "ADX",
    "GTP", "GDP", "GMP", "GNP", "GSP", "GCP",
    "UTP", "UDP", "CTP", "CDP", "TTP",
}
_OTHER_COFACTORS = {
    "COA", "ACO", "CMC", "SAM", "SAH", "SFG", "PLP", "PMP", "PNS", "TPP", "TDP",
    "TPW", "BTN", "BTI", "B12", "COB", "CNC", "B1Z", "MQ7", "U10", "UQ1", "PQQ",
    "F43", "MGD", "2MD", "MTE", "LPA", "THG", "THF", "BH4", "H4B", "GSH", "BCT",
    "F42", "FFO", "MDO", "PEB", "BLA",
}
# Iron-sulfur & metal clusters (keep — biological cofactors)
_METAL_CLUSTERS = {"SF4", "FES", "FS4", "F3S", "CLF", "CLP", "CFM", "ICS", "WCC",
                   "CUA", "CUB", "OEC", "0OD"}

COFACTORS = (_HEMES | _FLAVINS | _NICOTINAMIDES | _NUCLEOTIDE_LIGANDS
             | _OTHER_COFACTORS | _METAL_CLUSTERS)

# --- Borderline single metal ions: keep AND flag for review --------------
# (Transition + alkaline-earth + heavy metals. Often catalytic cofactors, but
#  sometimes just from the liquor — surface them rather than guess.)
BORDERLINE_METALS = {
    "ZN", "FE", "FE2", "FE3", "3NI", "NI", "CO", "3CO", "CU", "CU1", "CU3",
    "MN", "MN3", "MO", "MOS", "W", "V", "CD", "HG", "AU", "AU3", "AG", "PT",
    "PD", "CR", "PB", "MG", "CA", "SR", "BA", "BS3", "YB", "SM", "GD", "EU",
    "TB", "Y1", "CE", "LA", "OS", "IR", "RU", "RH", "RE", "TE",
}


@dataclass
class LigandDecision:
    comp_id: str
    keep: bool
    category: str       # water | additive | cofactor | metal | ligand
    flagged: bool       # surfaced for human review even if kept
    reason: str


def classify(comp_id: str,
             extra_exclude: set[str] | None = None,
             extra_keep: set[str] | None = None) -> LigandDecision:
    """Classify a single HET code. Per-target overrides take precedence."""
    cid = comp_id.upper()
    extra_keep = {c.upper() for c in (extra_keep or set())}
    extra_exclude = {c.upper() for c in (extra_exclude or set())}

    if cid in extra_keep:
        return LigandDecision(cid, True, "ligand", False, "kept by per-target override")
    if cid in extra_exclude:
        return LigandDecision(cid, False, "additive", False, "excluded by per-target override")
    if cid in WATERS:
        return LigandDecision(cid, False, "water", False, "water")
    if cid in COFACTORS:
        return LigandDecision(cid, True, "cofactor", False, "recognised biological cofactor")
    if cid in BORDERLINE_METALS:
        return LigandDecision(cid, True, "metal", True,
                              "metal ion — kept but flagged (may be cofactor or additive)")
    if cid in ADDITIVES:
        return LigandDecision(cid, False, "additive", False,
                              "crystallographic additive / buffer / cryo / detergent")
    return LigandDecision(cid, True, "ligand", False, "ligand of interest")
