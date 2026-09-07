# Pharmacophore Construction Pipeline

Automated pharmacophore-model construction, generalised across diverse protein classes
(work targeting a JCIM publication). Two things this repo does, from the command line:

1. **Build a pharmacophore** from a set of **already-aligned ligands** (a Gaussian-KDE
   consensus over their pharmacophoric features).
2. **Align ligands to each other by their pharmacophoric features** — no protein needed —
   from a ranked set of SMILES, and optionally build a pharmacophore from the result.

Everything runs through [**pixi**](https://pixi.sh); scientific choices live in `config/`,
never in code. This README has all you need to run the code; deeper detail is in
[`docs/tools.md`](docs/tools.md) (every mode + script) and
[`catalogue/pharmacophore_method.md`](catalogue/pharmacophore_method.md) (the method).

---

## Setup

```bash
pixi install -e dev          # core + cheminformatics + test/lint tooling
pixi run test                # pytest  (offline unit tests)
pixi run lint                # ruff
```

Dependencies are split into pixi *features* so a heavy/brittle one never blocks the rest:
`core` (config/tabular IO), `chem` (`rdkit`, `openbabel`, `gemmi`), `dev` (`pytest`,
`ruff`), `viz` (`pymol-open-source`, only for baking `.pse` sessions), `prep` (an isolated
`pkasolver` stack for pH-7.4 protonation). Environments: `default` (core+chem), `dev`,
`viz`, `prep`.

---

## Usage — the two key features

Both are one command: `pixi run build-pharmacophores …` (script:
`scripts/build_pharmacophores.py`). Every model directory it writes contains
`pharmacophore.json` (the model), `features.csv`, `model_summary.md`,
`pharmacophore.pml` + PNGs, and a representative-ligand SDF.

### 1. Build a pharmacophore from a set of aligned ligands

Give it a directory of **`*.mol2` poses that are already superposed into one common frame**
and a `het_code,smiles` CSV; it protonates them to their pH-7.4 microstate, builds the
consensus pharmacophore (molecule-weighted KDE occupancy field → peaks → support-filtered
features), and renders it.

```bash
pixi run build-pharmacophores \
    --input   path/to/aligned_mol2_dir \
    --out     path/to/output_dir \
    --smiles  path/to/ligands.csv          # columns: het_code,smiles
```

Useful options:

| Option | Effect |
|---|---|
| `--reference-pdb receptor.pdb` | Aligned receptor → adds excluded-volume markers to the model. |
| `--allow-unprotonated` | Skip pH-7.4 protonation (build from the given neutral SMILES). |
| `--no-render` | Skip the PyMOL `.pse`/`.png` render (faster; model files still written). |

> Protonation uses the isolated `prep` env; pass `--allow-unprotonated` if you don't have
> it set up. The mol2 must already be aligned — this mode does **not** superpose them.

### 2. Align ligands by their pharmacophoric features

Give it a directory containing a **rank index CSV** (`index_*.csv` with columns
`entity_id,mol_id,library_name,smiles,drugclip_score,…`, auto-detected). It embeds a
conformer ensemble per compound and **iteratively superposes them on their shared
pharmacophoric features** — matching on the *relative intra-molecular distances* between
features (correspondence graph → cliques → Kabsch), with EM refinement (re-selecting each
compound's best conformer) and orientation-aware H-bond matching. The recommended,
protein-free start is **`--seedless`** (the top-ranked compound's low-energy conformer is
the initial frame — a seed is optional and generally works less well).

```bash
# Align the top 100 ranked ligands and build a pharmacophore from them:
pixi run build-pharmacophores \
    --seed-docked path/to/ligand_dir \
    --out         path/to/output_dir \
    --top-hits    100 \
    --seedless

# Just emit the aligned ligands (no pharmacophore) — e.g. to run your own analysis:
pixi run build-pharmacophores \
    --seed-docked path/to/ligand_dir --out path/to/output_dir \
    --top-hits 100 --seedless --align-only
```

Outputs the **aligned compound set** (`aligned_compounds.sdf`, `aligned_points.csv`,
`alignment_manifest.csv`) and, unless `--align-only`, the pharmacophore model files.

Useful options:

| Option | Effect |
|---|---|
| `--seedless` | **Recommended.** No seed; frame = top compound's lowest-energy conformer. |
| `--seed frame.sdf` | Use an explicit 3D frame (a crystal ligand or docked poses) instead. Available but generally less effective — a bad seed pose can bias the consensus. |
| `--seed-k 5` | With a docked seed: how many top docked poses seed the frame. |
| `--align-only` | Stop after writing the aligned set; skip the KDE model. |
| `--reference-pdb receptor.pdb` | Aligned receptor → excluded-volume markers. |

> The directory needs only the `index_*.csv` (SMILES) for `--seedless`. Docked
> `<mol_id>_docked.sdf` files are needed only if you seed from docked poses. Tuning knobs
> (conformers, clique tolerance, EM, directional matching) live in
> `config/pharmacophore.yaml` under `alignment:`. All defaults are sensible.

---

## Other build modes

- `pixi run build-pharmacophores --catalogue` — build a model for every `(pocket ×
  efficacy)` cell of the curated known-actives catalogue (offline).
- `pixi run build-pharmacophores --target <slug>` — one catalogue target.
- `pixi run build-pharmacophores --docked-dir DIR --out DIR --top-hits N` — one consensus
  over a whole docked hit set (an alternative to the feature-alignment mode above).

See [`docs/tools.md`](docs/tools.md) for the full list of modes and the screening-evaluation
scripts.

---

## The known-actives pipeline (Stages 1–3, for the benchmark catalogue)

Assembling the curated benchmark set that the catalogue build draws on. Run via pixi tasks;
scientific knowledge lives in `config/` (`targets.yaml`, `sites.yaml`, `pockets.yaml`,
`efficacy.yaml`, `pharmacophore.yaml`).

| Stage | Task | Network? |
|---|---|---|
| 1 — scrape & catalogue | `pixi run scrape-pdb-ligands --config config/targets.yaml` | yes (login node) |
| 2 — site filter & align | `pixi run align-sites` (`build-sessions` to bake `.pse`) | yes (login node) |
| 3.3 — efficacy resolution | `pixi run resolve-efficacy` | yes (login node) |
| 3 — effect grouping | `pixi run -e viz group-effects` | no (offline) |
| 4 — pharmacophore construction | `pixi run build-pharmacophores --catalogue` | no (offline) |

`CLAUDE.md` is the authoritative project reference (rules, target table, per-stage detail).

---

## Outputs

- `catalogue/` (**tracked**) — the deliverable: the known-actives catalogue
  (`catalogue/DATASETS.md`), the built pharmacophore models, and the screening-evaluation
  reports + models (`catalogue/screening_eval/`).
- `data/` (**gitignored**, large) — cached structures, organised screening sets, scratch.
- The full DrugCLIP source compound library (`molecule_library/`, ~48 GB) is gitignored;
  see [`docs/molecule_library.md`](docs/molecule_library.md).

## HPC / Gadi notes

- Compute nodes have no internet — run the network stages (scrape/align/efficacy) and any
  docking on a login/data-mover node.
- Keep `.pixi/` and `PIXI_CACHE_DIR` off the 10 GiB `/home`; use `/scratch/<project>/<user>`
  for repo+env and `/g/data` for reference data (and the compound library).
