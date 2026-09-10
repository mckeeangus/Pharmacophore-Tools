# CLAUDE.md — Pharmacophore tools

Persistent project context for Claude Code. Read fully before acting.

## What this repo is

Three command-line tools for **ligand-based pharmacophore modelling**, over a shared engine.
They chain **align → build → visualise** but each stands alone. The repo is **offline** and
**purely ligand-based** (no receptor, no excluded volume). Everything runs through **pixi**;
scientific choices live in `config/`, never in code.

> The crystal known-actives research pipeline (PDB scrape → site-align → group), the curated
> catalogue, and the **results derived with these tools** (DrugCLIP reconstruction + screening
> evaluation) live in a **separate repository** — this repo was split out to hold just the tools.
> Do not re-add that research code here.

## The three tools

1. **`align-molecules`** (`scripts/align_molecules.py`) — superpose molecules by their shared
   pharmacophoric features: conformer ensembles (ETKDG+MMFF, energy-windowed) → feature-clique
   matching on **relative intra-molecular distances** (correspondence graph → Bron–Kerbosch →
   Kabsch) → EM refinement (re-selects each compound's best conformer) → orientation-aware H-bond
   matching. **Seedless by default.** Input a DrugCLIP output CSV (`mol_id,…,smiles,…,
   drugclip_score`) or a multi-molecule SDF; output `aligned_compounds.sdf` (+ points CSV +
   manifest). Method: `docs/molecule_alignment.md`.
2. **`build-pharmacophore`** (`scripts/build_pharmacophore.py`) — molecule-weighted Gaussian-KDE
   consensus from aligned molecules (the SDF from tool 1, or a directory of aligned crystal
   `*.mol2`): occupancy field → peaks → support-filtered features. Output **`pharmacophore.csv`**
   (the interchange), plus `pharmacophore_model.json` (canonical), `model_summary.md`,
   `features.csv`, `representative_ligand.sdf`, per-family PNGs. Method:
   `docs/pharmacophore_construction.md`.
3. **`visualise-pharmacophore`** (`scripts/visualise_pharmacophore.py`) — render a
   `pharmacophore.csv` to a PyMOL session/snapshot + a 20-state support-cutoff sweep (drives
   `scripts/pymol_pharmacophore.py` in the `viz` env).

**Interchange CSV** (`pharmacophore/io.py` `write_model_csv`/`read_model_csv`): one row per
feature — `family,label,x,y,z,radius,n_points,n_ligands,support,dx,dy,dz` (feature rows only).

## Key behaviours & optimised defaults (in `config/pharmacophore.yaml`)

- **`--top-n` = 50** — the depth that best matched the known-actives models; ≥100 dilutes.
- **`alignment.min_clique` = 3** — a compound is folded in only if ≥3 of its features match the
  reference (same family + mutually distance-consistent) within `max_align_rmsd` (1.5 Å). This is
  the geometric minimum for a determined rigid 3-D superposition, not a tunable heuristic — see the
  "Why ≥3 features" section in `docs/molecule_alignment.md`. Dropped compounds are recorded
  `aligned=False` in `alignment_manifest.csv`.
- **`alignment.energy_window` = 10 kcal/mol** — bioactive-conformer window (standard range; above
  MMFF's ~1–2 kcal/mol noise).
- **`--seed ligand.sdf|.mol2`** — optional holo co-crystal ligand. It **bootstraps** the frame
  (anchors the growing pass, then is dropped before EM so the model reflects the aligned molecules
  alone) and, in protein coordinates, positions the output in the binding site. This was the
  best-performing seed mode in testing. Default is seedless.
- **`use_directions` on** — H-bond donor/acceptor orientation fit via projected points.
- **`selection.min_ligands` = 10** — no longer a hard skip: below it the build **still runs** but
  warns the consensus is weak / the model provisional.
- **Construction**: molecule-weighted KDE, peak watershed, `occupancy_floor` + support floor
  (`min_support_fraction` 0.5, hard-membership within `membership_radius` 1.5 Å), density-quantile
  tolerance, cross-family overlap merge (`merge_radius` 1.0, `merge_exempt_pairs`
  Donor+Acceptor / Aromatic+LumpedHydrophobe). Deterministic.

## Protonation (pH 7.4)

- **SDF input is trusted as-is** — DrugCLIP-derived SDFs carry their protonation; no pKa
  prediction is run on them.
- **Crystal `*.mol2` input**: `build-pharmacophore` auto-uses a `protonated_ligands.csv` (pkasolver
  + weak-acid guard, from `pixi run -e prep protonate-ligands`) found beside `--smiles`; else falls
  back to the neutral SMILES with a warning. pkasolver lives in the isolated `prep` env (pinned
  2021-era stack), invoked only when you run that step.

## Code layout

- `src/pharmpipe/features/` — `extract.py` (pure feature perception → `FeaturePoint`/`FeatureTable`,
  with the co-atom feature hierarchy), `load.py` (mol2/SMILES loading, protonation map),
  `conformers.py` (ensembles), `dock_load.py` (DrugCLIP index + docked SDF readers).
- `src/pharmpipe/pharmacophore/` — `align.py` (clique alignment + `seed_align`), `density.py` (KDE
  consensus), `build.py` (shared primitives: tolerance, merge, representative pick), `model.py`
  (`Pharmacophore` schema), `io.py` (JSON/CSV/PML/SDF), `viz.py` (matplotlib), `run.py`
  (orchestration: `build_from_molecules` / `build_from_directory` / `build_from_seed_alignment`),
  `config.py`.
- `src/pharmpipe/prep/` — pkasolver ladder-walk protonation. `src/pharmpipe/util/` — paths, http.

## Operating rules

- **pixi only.** Run via `pixi run <task>` / `pixi run python …`; never a bare ambient `python`,
  never conda `base`. Add deps with `pixi add` into the right feature (`core`/`chem`/`ph4`/`dev`/
  `viz`/`prep`); pip-only packages go in that feature's `pypi-dependencies`.
- **Config, not code.** No hardcoded scientific decisions or silent defaults that encode one.
- **Quality**: small pure functions, IO at the edges, typed dataclasses, low duplication.
- Keep it **offline** and dependency-compartmentalised (a heavy/brittle dep must not block the rest).

## Code quality

Prefer low cyclomatic complexity, low duplication (reuse the io/parse/path helpers), explicit typed
contracts, testability (pure core, IO at edges), modularity, Pythonic structures. Avoid hidden
assumptions, hardcoded domain knowledge, and unnecessary coupling.
