# Pharmacophore Construction Pipeline

Automated pharmacophore-model construction, generalised across diverse protein
classes (work targeting a JCIM publication).

The intended downstream flow is: **DrugCLIP** virtual screening → ligand prep →
**GNINA** docking → distance/score filtering → RDKit feature extraction →
clustering → pharmacophore model. That downstream pipeline is **not in scope
yet**.

**Current stage:** assemble a curated set of experimentally-bound ligands from
the PDB to feed pharmacophore construction (the `pharmpipe.pdb` +
`pharmpipe.catalogue` stages).

## Environment (pixi)

Dependencies are managed with [pixi](https://pixi.sh). Features are split so a
heavy/brittle dependency never blocks the rest:

- `core` — networking, config, tabular IO (`requests`, `pyyaml`, `pandas`,
  `tqdm`, `rcsbsearchapi`).
- `chem` — cheminformatics & structure parsing (`rdkit`, `openbabel`, `gemmi`,
  `openpyxl`).
- `dev` — `pytest`, `ruff`.

Environments: `default` (core + chem) and `dev` (core + chem + dev).

```bash
pixi install                # default env
pixi install -e dev         # with test/lint tooling
```

## Run the PDB ligand scrape

```bash
pixi run scrape-pdb-ligands --config config/targets.yaml
```

This resolves & verifies each target's UniProt accession(s), queries RCSB for
ligand-bound structures, curates ligands (drops additives/buffers, keeps genuine
cofactors), writes the catalogue under `catalogue/`, and extracts bound-pose
ligands as mol2 under `data/targets/<slug>/ligands/mol2/`.

### Outputs

- `catalogue/` (**tracked**) — per-target CSVs, `ligand_catalogue.md`, optional
  `.xlsx`, and a run summary. This is the deliverable.
- `data/` (**gitignored**, large) — cached mmCIF structures and extracted mol2.

## HPC / Gadi notes

- Compute nodes have no internet — run the scrape on a login/data-mover node.
- Keep `.pixi/` and `PIXI_CACHE_DIR` off the 10 GiB `/home`; use
  `/scratch/<project>/<user>` for repo+env and `/g/data` for reference data.

## Layout

See `CLAUDE.md` for the authoritative repository layout and project rules.
