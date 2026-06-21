# Pharmacophore Construction Pipeline

Automated pharmacophore-model construction, generalised across diverse protein
classes (work targeting a JCIM publication).

**Where we are:** the **known-actives assembly is complete** for all 16 benchmark
targets (17 site-slugs — Nav1.7 is split into a VSD4 and a pore site) — every
experimentally-bound ligand is scraped from the PDB, filtered to the relevant site,
aligned, and partitioned into **cells = (verified pocket × efficacy sign)** with
curated provenance. The tracked result is `catalogue/` (see `catalogue/DATASETS.md`).
The project is now building **pharmacophore models** from those grouped active poses.

The longer-term flow (DrugCLIP virtual screening → GNINA docking → score
filtering) remains out of scope and is not built here.

## Environment (pixi)

Dependencies are managed with [pixi](https://pixi.sh); features are split so a
heavy/brittle dependency never blocks the rest:

- `core` — networking, config, tabular IO (`requests`, `pyyaml`, `pandas`, `tqdm`).
  RCSB is queried directly over `requests` (no `rcsbsearchapi` — its import-time
  network coupling is not HPC-portable).
- `chem` — cheminformatics & structure parsing (`rdkit`, `openbabel`, `gemmi`, `openpyxl`).
- `dev` — `pytest`, `ruff`.
- `viz` — `pymol-open-source`, isolated; only needed to bake `.pse` sessions.

Environments: `default` (core+chem), `dev` (+dev), `viz` (+viz).

```bash
pixi install -e dev          # core + chem + test/lint tooling
pixi run test                # pytest
pixi run lint                # ruff
```

## Pipeline stages

Each stage writes tracked deliverables under `catalogue/`. Run via pixi tasks:

| Stage | Task | Network? |
|---|---|---|
| 1 — scrape & catalogue | `pixi run scrape-pdb-ligands --config config/targets.yaml` | yes (login node) |
| 2 — site filter & align | `pixi run align-sites` (`build-sessions` to bake `.pse`) | yes (login node) |
| 3.3 — efficacy resolution | `pixi run resolve-efficacy` | yes (login node) |
| 3 — effect grouping | `pixi run -e viz group-effects` | no (offline) |

Curated scientific knowledge lives in `config/` (`targets.yaml`, `sites.yaml`,
`pockets.yaml`, `efficacy.yaml`), never in code. See `CLAUDE.md` for the
authoritative project rules, the target table, and per-stage detail.

## Outputs

- `catalogue/` (**tracked**) — the deliverable: per-target CSVs/JSON, `(pocket ×
  efficacy)` cells, pose datasets, PyMOL sessions, run summary, and curation
  provenance. Start at `catalogue/DATASETS.md`.
- `data/` (**gitignored**, large) — cached mmCIF and intermediate mol2.

## HPC / Gadi notes

- Compute nodes have no internet — run the network stages on a login/data-mover node.
- Keep `.pixi/` and `PIXI_CACHE_DIR` off the 10 GiB `/home`; use
  `/scratch/<project>/<user>` for repo+env and `/g/data` for reference data.
