"""PDB / RCSB / UniProt querying and bound-ligand extraction.

Modules:
    uniprot    — resolve & verify target -> UniProt accession(s).
    rcsb       — RCSB Search API queries for ligand-bound structures.
    exclusions — maintained additive/buffer exclusion list & cofactor keep-list.
    ligands    — curation of bound ligands (apply exclusions, flag borderline).
"""
