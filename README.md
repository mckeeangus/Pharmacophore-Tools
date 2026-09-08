# Pharmacophore tools

Three command-line tools for building and inspecting **ligand-based pharmacophore models**,
generalised across diverse protein classes (work targeting a JCIM publication). They chain
together — **align → build → visualise** — but each stands alone:

1. **Molecule alignment** (`align-molecules`) — superpose a set of molecules on their shared
   pharmacophoric features, with no protein and no pre-existing common frame. Input a DrugCLIP
   output CSV or a multi-molecule SDF; output the aligned molecules.
2. **Pharmacophore construction** (`build-pharmacophore`) — build a Gaussian-KDE consensus
   pharmacophore from a set of aligned molecules (the output of tool 1, or aligned crystal
   poses). Output a `pharmacophore.csv` model.
3. **Pharmacophore visualisation** (`visualise-pharmacophore`) — render a `pharmacophore.csv`
   into a PyMOL session + snapshot and a support-cutoff sweep.

Everything runs through [**pixi**](https://pixi.sh); scientific choices live in `config/`,
never in code. Methodology is documented in
[`docs/molecule_alignment.md`](docs/molecule_alignment.md) and
[`docs/pharmacophore_construction.md`](docs/pharmacophore_construction.md).

---

## Setup

```bash
pixi install -e dev          # core + cheminformatics + test/lint tooling
pixi run test                # pytest (offline unit tests)
pixi run lint                # ruff
```

Dependencies are split into pixi *features* so a heavy/brittle one never blocks the rest:
`core` (config/tabular IO), `chem` (`rdkit`, `openbabel`, `gemmi`), `ph4` (`scipy`,
`matplotlib`), `dev` (`pytest`, `ruff`), `viz` (`pymol-open-source`, for tool 3), `prep` (an
isolated `pkasolver` stack for pH-7.4 protonation). Environments: `default` (core+chem+ph4),
`dev`, `viz`, `prep`.

---

## The three tools

### 1. `align-molecules` — align molecules by pharmacophoric features

Embeds a conformer ensemble per molecule and **iteratively superposes them on their shared
features** — matching on the *relative intra-molecular distances* between features
(correspondence graph → cliques → Kabsch), with EM refinement and orientation-aware H-bond
matching. Protein-free and **seedless by default**. Method:
[`docs/molecule_alignment.md`](docs/molecule_alignment.md).

```bash
# From a DrugCLIP output CSV (mol_id,…,smiles,…,drugclip_score) — align the top 100 by score:
pixi run align-molecules --input hits.csv --out out/aligned --top-n 100

# From a multi-molecule SDF instead:
pixi run align-molecules --input molecules.sdf --out out/aligned
```

Writes `aligned_compounds.sdf` (feed to tool 2), `aligned_points.csv`, `alignment_manifest.csv`.

| Option | Effect |
|---|---|
| `--top-n N` | Align the top *N* molecules (by score for a CSV; default 100). |
| `--seed frame.sdf` | Advanced: use an explicit 3-D frame (crystal ligand / docked poses) instead of the seedless start. Generally less effective — a bad pose can bias the consensus. |
| `--config PATH` | Override `config/pharmacophore.yaml` (the `alignment:` block). |

### 2. `build-pharmacophore` — build a pharmacophore from aligned molecules

Takes **aligned molecules** — the `aligned_compounds.sdf` from tool 1, or a directory of aligned
crystal `*.mol2` — and builds the consensus: molecule-weighted Gaussian-KDE occupancy field →
peaks → support-filtered features. **Purely ligand-based** (no receptor, no excluded volume).
Method: [`docs/pharmacophore_construction.md`](docs/pharmacophore_construction.md).

```bash
# From aligned molecules (the usual chain from tool 1):
pixi run build-pharmacophore --input out/aligned/aligned_compounds.sdf --out out/model

# From a directory of aligned crystal mol2 (needs bond orders + protonation):
pixi run build-pharmacophore --input aligned_mol2_dir --out out/model --smiles ligands.csv
```

Writes **`pharmacophore.csv`** (the interchange for tool 3), plus `pharmacophore.json`
(canonical), `model_summary.md`, `features.csv`, `representative_ligand.sdf`, per-family PNGs.

| Option | Effect |
|---|---|
| `--smiles het_code,smiles.csv` | Bond orders for a heavy-atom mol2 directory (not needed for an SDF). A `protonated_ligands.csv` beside it is auto-used for pH-7.4 states (pkasolver + weak-acid guard); SDF input is trusted as-is. |
| `--config PATH` | Override `config/pharmacophore.yaml` (`density:`/`selection:`/`tolerance:`). |

> A cell with fewer than `selection.min_ligands` (10) molecules is skipped — below that the
> consensus is too sparse to trust.

### 3. `visualise-pharmacophore` — render a pharmacophore CSV

Reads a `pharmacophore.csv` and produces the visualisation suite in PyMOL (runs the `viz` env
under the hood).

```bash
pixi run visualise-pharmacophore \
    --pharmacophore out/model/pharmacophore.csv --out out/viz \
    --compounds out/aligned/aligned_compounds.sdf \   # optional overlay
    --features  out/model/features.csv                # optional: enables the support sweep
```

Writes `pharmacophore.pse` + `.png` (the kept model) and, with `--features`,
`pharmacophore_sweep.pse` + `.png` (the support-cutoff sweep across 20 states).

### The full chain

```bash
pixi run align-molecules       --input hits.csv --out out/aligned --top-n 100
pixi run build-pharmacophore   --input out/aligned/aligned_compounds.sdf --out out/model
pixi run visualise-pharmacophore --pharmacophore out/model/pharmacophore.csv --out out/viz \
    --compounds out/aligned/aligned_compounds.sdf --features out/model/features.csv
```

---

## Reconstructed findings

`results/` holds the tools run end-to-end over the DrugCLIP→GNINA hit sets of the 11 targets
that have a crystal known-actives ground truth. Each `results/<target>/` carries that target's
tool outputs (aligned molecules, `pharmacophore.csv`, summary, plots, PyMOL session), and
[`results/RECONSTRUCTION.md`](results/RECONSTRUCTION.md) scores every model against its crystal
and literature references (feature-family recall + frame-independent internal geometry). Headline:
the ligand-based align→build pipeline reproduces the experimentally- and literature-derived
pharmacophores at the family level across all 11 targets, and geometrically for the pose-invariant
features. Regenerate with `pixi run python scripts/reconstruct_findings.py`.

---

## Repository layout

```
scripts/           the three tools + build_pharmacophores.py (catalogue batch) + protonate_ligands.py
src/pharmpipe/      features/ (perception) · pharmacophore/ (alignment, KDE, model, io, viz) · io/ · prep/ · util/
config/             pharmacophore.yaml (the tools' knobs) + curated scientific config
docs/               the two methodology docs + method_animation/ (an animated walkthrough)
results/            reconstructed findings (tool outputs per target + RECONSTRUCTION.md)
catalogue/          the curated crystal known-actives set + its pharmacophore models (tracked)
archive/            the former research pipeline + screening evaluation (see below)
```

### The archived research pipeline

The known-actives assembly pipeline (PDB scrape → site alignment → effect grouping) and the
DrugCLIP screening evaluation are **archived** under `archive/` — kept accessible and runnable,
out of the main path. The scripts run directly, e.g.:

```bash
pixi run python archive/scripts/group_effects.py --config config/targets.yaml
pixi run python archive/scripts/seed_necessity_all.py --report-only
```

Their library modules remain under `src/pharmpipe/{pdb,sites,groups,catalogue,screening}` (inert
to the three tools). `CLAUDE.md` documents the full research history and the target catalogue.

---

## Outputs & data

- `results/`, `catalogue/`, `docs/` (**tracked**) — the tool outputs, crystal catalogue, and docs.
- `data/` (**gitignored**, large) — cached structures, organised docked screening sets, scratch.
- The DrugCLIP source compound library (`molecule_library/`, ~48 GB) is gitignored; see
  [`docs/molecule_library.md`](docs/molecule_library.md).

## HPC / Gadi notes

- Compute nodes have no internet — run any networked step (the archived scrape/align/efficacy
  stages, docking) on a login/data-mover node. The three tools are offline.
- Keep `.pixi/` and `PIXI_CACHE_DIR` off the 10 GiB `/home`; use `/scratch/<project>/<user>`
  for repo+env and `/g/data` for reference data (and the compound library).
