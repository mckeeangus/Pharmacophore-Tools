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

## Quick start

A small nAChR example ships in [`examples/`](examples/README.md). Run the full chain:

```bash
pixi run align-molecules         --input examples/nachr_hits.csv --out out/align
pixi run build-pharmacophore     --input out/align/aligned_compounds.sdf --out out/model
pixi run visualise-pharmacophore --pharmacophore out/model/pharmacophore.csv --out out/viz \
    --compounds out/align/aligned_compounds.sdf --features out/model/features.csv
```

`out/model/pharmacophore.csv` is the classic nicotinic 3-point model (cation + aromatic +
acceptor). (The example is deliberately small, so expect a "provisional model" warning — see
[`examples/README.md`](examples/README.md).)

---

## The three tools

### 1. `align-molecules` — align molecules by pharmacophoric features

Embeds a conformer ensemble per molecule and **iteratively superposes them on their shared
features** — matching on the *relative intra-molecular distances* between features
(correspondence graph → cliques → Kabsch), with EM refinement and orientation-aware H-bond
matching. Protein-free and **seedless by default**. Method:
[`docs/molecule_alignment.md`](docs/molecule_alignment.md).

```bash
# From a DrugCLIP output CSV (mol_id,…,smiles,…,drugclip_score) — align the top 50 by score:
pixi run align-molecules --input hits.csv --out out/aligned

# From a multi-molecule SDF instead:
pixi run align-molecules --input molecules.sdf --out out/aligned
```

Writes `aligned_compounds.sdf` (feed to tool 2), `aligned_points.csv`, `alignment_manifest.csv`.

| Option | Effect |
|---|---|
| `--top-n N` | Align the top *N* molecules (by score for a CSV; **default 50** — the depth that best matched the known-actives models; ≥100 dilutes). |
| `--seed ligand.sdf\|.mol2` | Optional holo co-crystal ligand. It **bootstraps** the frame (anchors the growing pass, then is dropped before EM so the model reflects the aligned molecules alone). If given in a protein's coordinates the output pharmacophore is positioned in that binding site. Default: seedless. |
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

Writes **`pharmacophore.csv`** (the interchange for tool 3), plus `pharmacophore_model.json`
(the canonical model + provenance), `model_summary.md`, `features.csv`,
`representative_ligand.sdf`, per-family PNGs.

| Option | Effect |
|---|---|
| `--smiles het_code,smiles.csv` | Bond orders for a heavy-atom mol2 directory (not needed for an SDF). See the optional protonation step below. |
| `--config PATH` | Override `config/pharmacophore.yaml` (`density:`/`selection:`/`tolerance:`). |

> A cell with fewer than `selection.min_ligands` (10) molecules still builds, but emits a
> **warning** that the consensus is weak and the model provisional — it is no longer skipped.

#### Optional: pH-7.4 protonation with pkasolver

Protonation is an **optional preprocessing step** for the crystal `*.mol2` path, and it is the
tool's only protonation source. Run it once to predict each ligand's dominant pH-7.4 microstate
with **pkasolver** (plus the weak-acid guard), writing `protonated_ligands.csv` beside your
`--smiles` file:

```bash
pixi run -e prep protonate-ligands            # -> <slug>/protonated_ligands.csv
```

`build-pharmacophore` then **auto-detects and uses** that file so donor/acceptor/±ionizable
perception sees the real ionisation. If it is absent, the build falls back to the neutral
`--smiles` and warns. SDF input (from `align-molecules`, or any DrugCLIP-derived SDF) already
carries its protonation and is trusted as-is — pkasolver is never run on it. pkasolver lives in
the isolated `prep` env (a pinned 2021-era stack), so it stays out of the way unless you invoke it.

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
pixi run align-molecules       --input hits.csv --out out/aligned
pixi run build-pharmacophore   --input out/aligned/aligned_compounds.sdf --out out/model
pixi run visualise-pharmacophore --pharmacophore out/model/pharmacophore.csv --out out/viz \
    --compounds out/aligned/aligned_compounds.sdf --features out/model/features.csv
```

---

## Repository layout

```
scripts/       align_molecules.py · build_pharmacophore.py · visualise_pharmacophore.py
               · pymol_pharmacophore.py (viz backend) · protonate_ligands.py (prep env)
src/pharmpipe/ features/ (perception + loaders) · pharmacophore/ (alignment, KDE, model,
               io, viz, run) · prep/ (pH-7.4 protonation) · util/
config/        pharmacophore.yaml (the tools' knobs) · protonation.yaml (weak-acid guard)
docs/          molecule_alignment.md · pharmacophore_construction.md · method_animation/
examples/      a small runnable nAChR example (see examples/README.md)
tests/         offline unit tests
```

Scientific choices live in `config/`, never in code. The tools are **offline** and **purely
ligand-based** (no receptor, no excluded volume).

## Research pipeline & derived results

This repo is just the tools. The crystal known-actives research pipeline (PDB scrape → site
alignment → effect grouping), the curated `catalogue/`, and the **results derived with these
tools** (the DrugCLIP reconstruction + screening evaluation) live in a **separate repository**.
Across the 11 targets with a crystal ground truth, the ligand-based align→build pipeline reproduced
the experimentally- and literature-derived pharmacophores at the family level, and geometrically
for the pose-invariant features (the directional acceptor is the one soft spot). The remaining
ceiling is receptor-mediated (metal/water/steric), which is out of scope for a ligand-only tool.

## Data note

`data/`, `.pixi/`, and any bulk inputs are gitignored. The tools read only what you pass on the
command line; nothing large is tracked here.
