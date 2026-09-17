# Pharmacophore tools

Three command-line tools for building and inspecting **ligand-based pharmacophore models** from a
set of molecules hypothesised or confirmed to bind a common target. They chain
together but each can be used independently:

1. **Molecule alignment** (`align-molecules`) — superpose a set of molecules on their shared
   pharmacophoric features, with no protein and no pre-existing common frame. Input a CSV of
   molecules (id, SMILES, optional ranking score — e.g. a virtual-screening output from DrugCLIP) or a
   multi-molecule SDF; output the aligned molecules.
2. **Pharmacophore construction** (`build-pharmacophore`) — build a Gaussian-KDE consensus
   pharmacophore from a set of aligned molecules (the output of tool 1, or aligned crystal
   poses). Output a `pharmacophore.csv` model.
3. **Pharmacophore visualisation** (`visualise-pharmacophore`) — render a `pharmacophore.csv`
   into a PyMOL session.

---

## Setup

```bash
pixi install -e dev          # core + cheminformatics + test/lint tooling
pixi run test                # pytest (offline unit tests)
pixi run lint                # ruff
pixi run setup-prep          # optional: provisions the 'prep' env for --pkasolver
```
---

## Quick start

A small nAChR example ships in [`examples/`](examples/README.md). Run the full chain:

```bash
pixi run align-molecules         --input examples/nachr_hits.csv --out out/align
pixi run build-pharmacophore     --input out/align/aligned_compounds.sdf --out out/model
pixi run visualise-pharmacophore --pharmacophore out/model/pharmacophore.csv --out out/viz \
    --compounds out/align/aligned_compounds.sdf --features out/model/features.csv
```

---

## The three tools

### 1. `align-molecules` — align molecules by pharmacophoric features

```bash
# From a ranked CSV — top 50 by score. A header with a `smiles` column is enough (mol_id/score
# optional, any order); a header-less `smiles,score` screen output or a bare SMILES list also works:
pixi run align-molecules --input hits.csv --out out/aligned

# From a multi-molecule SDF instead:
pixi run align-molecules --input molecules.sdf --out out/aligned
```

Writes `aligned_compounds.sdf` (feed to tool 2), `aligned_points.csv`, `alignment_manifest.csv`.

| Option | Effect |
|---|---|
| `--top-n N` | Align the top *N* molecules (by the CSV's score column; without one, input order is the rank). **Default 50** |
| `--seed ligand.sdf\|.mol2` | Optional holo co-crystal ligand. Default: seedless. |
| `--pkasolver` | Protonate the top-*N* aligned ligands to their pH-7.4 dominant microstate (pkasolver) before conformers are built. **Off by default** |
| `--config PATH` | Override `config/pharmacophore.yaml` (the `alignment:` block). |

Use `-h` or `help` for options.

### 2. `build-pharmacophore` — build a pharmacophore from aligned molecules

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
| `--smiles het_code,smiles.csv` | Bond orders for a heavy-atom mol2 directory (not needed for an SDF). |
| `--pkasolver` | Protonate `--smiles` to pH 7.4 (pkasolver), writing `protonated_ligands.csv` beside it. **Off by default** |
| `--config PATH` | Override `config/pharmacophore.yaml` (`density:`/`selection:`/`tolerance:`). |

Use `-h` or `help` for options.

### 3. `visualise-pharmacophore` — render a pharmacophore CSV

Reads a `pharmacophore.csv` and produces the visualisation suite in PyMOL.

```bash
pixi run visualise-pharmacophore \
    --pharmacophore out/model/pharmacophore.csv --out out/viz \
    --compounds out/aligned/aligned_compounds.sdf \   # optional overlay
    --features  out/model/features.csv                # optional: enables a support sweep
```

---