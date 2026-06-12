"""Site-filtering + alignment stage.

Take the curated ligands from the catalogue stage and keep only those that bind
at the *relevant* site of each model system (e.g. the orthosteric ACh site of
nAChR), then superpose every kept instance into a single per-target reference
frame so the bound poses can be compared directly and rendered together in a
PyMOL session.
"""
