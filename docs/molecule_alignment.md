# Molecule alignment — method

**Tool:** `pixi run align-molecules --input hits.csv|mols.sdf --out DIR [--top-n 100] [--seed frame.sdf]`

Align a set of molecules to each other **by their shared pharmacophoric features**, with no
protein and no pre-existing common frame. The output is the set of molecules superposed into
one frame plus their pooled feature points — ready for `build-pharmacophore`.

The guiding idea: a pharmacophore *is* the set of **relative distances between features within
each molecule**. A docked or crystal conformation only supplies a *starting frame*; the
alignment matches on those internal distances, so the result is frame-independent chemistry.
Across the targets with a known-actives ground truth this recovers the same models the crystal
poses give (see `results/RECONSTRUCTION.md`).

## Input

Auto-detected by extension:

- a **DrugCLIP output CSV** — a rank index with `mol_id,…,smiles,…,drugclip_score` columns.
  The top `--top-n` compounds by score are aligned; a blank score column keeps input order.
- a **multi-molecule SDF** — each record a compound; molecule order is the rank, the title
  (or `mol<i>`) is the id, and the connectivity/SMILES is read from the record.

The molecules need **only 2-D/connectivity information** — 3-D coordinates are generated
internally. (`--seed` is the exception: it supplies a 3-D frame; see below.)

## Method

### 1. Protonation to the pH-7.4 microstate

Each compound is taken to its dominant physiological microstate so that donor/acceptor and
±ionizable perception sees the real ionisation. Docked SDFs carry a per-record
`protonated_smiles` (used directly, offline); otherwise protonation runs in the `prep` env
(pkasolver + the weak-acid guard — see `pharmacophore_construction.md` §Protonation). This is
the same protonation the construction tool uses, so the two stages agree on chemistry.

### 2. Conformer ensembles (energy-filtered)

`features/conformers.py` embeds a conformer ensemble per compound (ETKDG v3 + MMFF), prunes by
RMSD, and **discards high-energy conformers up front** (`alignment.energy_window` — a strained
conformer is unlikely to be the bioactive one). The bioactive conformer must be *in* the
ensemble for the alignment to find it: rigid ligands need few conformers, flexible ligands need
larger ensembles (the classic "bioactive conformer must be present" failure mode).

### 3. Feature-clique alignment (the core, pure)

`pharmacophore/align.py` superposes one compound onto the growing model by matching feature
cliques:

1. **Correspondence graph** — a node for each same-family feature pair (one feature in the
   model, one in the compound); an **edge** between two nodes whose *intra-molecular distances
   agree* within `alignment.dist_tol`. A clique in this graph is a set of feature
   correspondences that are mutually distance-consistent — i.e. the same rigid sub-arrangement
   in both molecules.
2. **Maximal cliques** via **Bron–Kerbosch** (greedy-bounded for large graphs).
3. **Kabsch** superposition for each clique; keep the one maximising `(matched features, −RMSD)`.

A compound is **folded into the model only if** its best clique shares at least
`alignment.min_clique` feature types **and** clears `alignment.max_align_rmsd` — the key
quality gate, since a poor fit would otherwise corrupt the running consensus. Dropped compounds
are recorded `aligned=False` in `alignment_manifest.csv`.

### 4. Incremental growth + EM refinement

The model is built incrementally: initialise the frame, then align compound *k*, update the
model (running mean of matched feature points), align compound *k+1*, update, … After the
growing pass, an **EM refinement** (`alignment.em_iterations`, `em_tol`) re-aligns *every*
compound to the current full consensus and recomputes the feature centres to a fixed point.

The re-alignment **re-selects each compound's best conformer against the improved consensus** —
this is the refinement of choice (over torsional relaxation): it removes the effect of a
sub-optimal *discrete* conformer chosen early **without distorting any structure**. A rigid
compound that cannot move is simply left at its best available conformer; the `max_align_rmsd`
gate still drops true outliers.

### 5. Initialisation — seedless (default) or seeded

The frame is initialised in one of three ways, all feeding the *same* iterative alignment:

- **Seedless** (default, recommended) — from the top-ranked compound's lowest-energy conformer.
- **`--seed frame.sdf`** (advanced) — an arbitrary 3-D frame (a crystal ligand or docked poses).

**A seed is generally *not* necessary for correct geometry.** The shared *rigid cores* impose
enough mutual distance constraint that the consensus locks onto the right shape from any
reasonable start; the seed only affects convergence speed, and a poor seed pose can actively
bias the frame. On the ground-truth targets, seedless matches or beats a docked seed in 10/11
(the lone exception being a metal-coordination target with few rigid multi-feature cores). A
seed remains supported for cases where a trusted bioactive frame is available.

### 6. Directional (orientation-aware) matching

With `alignment.use_directions` (default on), feature perception emits an **orientation vector**
per directional family — Donor D→H, Acceptor lone-pair (from the heavy neighbours, so it flips
sign for a ring-flipped nitrogen), Aromatic ring-normal. The clique superposition then fits, for
each matched donor/acceptor, a **projected point** (feature centre + `projected_length` Å along
its vector) *jointly with the centres* — the standard LigandScout/Catalyst device that turns
orientation into a positional target — so a wrongly-oriented match no longer superposes cleanly
and is penalised by RMSD. The consensus `direction` field is populated from the aligned points.

## Outputs (in `--out`)

- **`aligned_compounds.sdf`** — the aligned molecules (best conformer each). Feed this straight
  to `build-pharmacophore`.
- **`aligned_points.csv`** — the pooled per-molecule feature points in the common frame.
- **`alignment_manifest.csv`** — per-compound provenance: rank, whether it aligned, clique size,
  RMSD.

## Knobs

All in `config/pharmacophore.yaml` under `alignment:` — `dist_tol`, `min_clique`,
`max_align_rmsd`, `energy_window`, `em_iterations`, `em_tol`, `seed_k`, `use_directions`,
`projected_length`. These are scientific choices and live in config, never in code.

## Limits (honest)

- **Coverage** — compounds sharing fewer than `min_clique` feature types with the model are
  dropped; the manifest reports aligned/total.
- **Conformer sampling** — flexible targets need larger ensembles; if the bioactive conformer is
  absent from the ensemble the alignment cannot find it.
- **Directional acceptors** — the one soft spot; a docked ring-flip propagates into the
  consensus acceptor orientation. The pose-invariant cation/aromatic/hydrophobe anchors are
  robust.

---

*Provenance:* this method was developed and benchmarked on the DrugCLIP→GNINA nAChR set and
generalised across the 11 ground-truth targets. The full research write-up (seed-necessity,
directional, geometry-limit studies) is preserved in `archive/` and the combined historical
method note `catalogue/pharmacophore_method.md`.
