# Pharmacophore construction — method

**Tool:** `pixi run build-pharmacophore --input aligned.sdf|mol2_dir --out DIR [--smiles het.csv]`

Build a **consensus pharmacophore** from a set of **already-aligned molecules** — the
`aligned_compounds.sdf` from `align-molecules`, or a directory of aligned crystal `*.mol2`
poses. The molecules must share one common frame. The model is **purely ligand-based**: no
receptor, no excluded volume. The primary output is a **`pharmacophore.csv`** — the interchange
that `visualise-pharmacophore` consumes.

## Input

- **An SDF of aligned molecules** (the common case — the output of `align-molecules`). Bonds and
  coordinates are intact, so features are perceived directly.
- **A directory of aligned `*.mol2`** (the crystal known-actives case). These are heavy-atom-only,
  so `--smiles het_code,smiles.csv` supplies bond orders (via RDKit
  `AssignBondOrdersFromTemplate`) and the pH-7.4 protonation is applied through the `prep` env.

## Method

### 1. Protonation to the pH-7.4 microstate (preprocessing)

Feature perception must see the real ionisation. The tool's **only** protonation source is
**pkasolver + the weak-acid guard**, and it is applied to exactly one input kind:

- **mol2 directory (crystal poses)** — `scripts/protonate_ligands.py` (the isolated `prep` env)
  predicts pKa with **pkasolver**, applies the weak-acid guard (below), and writes each HET's
  dominant pH-7.4 microstate to `protonated_ligands.csv`. `build-pharmacophore` **auto-overlays**
  that CSV when it sits beside `--smiles` (pH-7.4 states win; HETs without an entry keep the
  neutral SMILES), and the bond-order template (`AssignBondOrdersFromTemplate`) carries the
  formal charges onto the heavy-atom pose. If the CSV is absent the build falls back to neutral
  SMILES and warns.
- **SDF input (from `align-molecules`, or any DrugCLIP-derived SDF)** — **trusted as-is.** These
  poses already carry a protonation state, so **no pKa prediction is run on them** — pkasolver is
  never invoked on SDF input.

**Weak-acid guard.** pkasolver systematically *over-deprotonates* weak acids (phenols, alcohols,
amides, primary sulfonamides, amino-heteroaromatics) on poly-ionizable scaffolds, because
adjacent-charge / *ortho* H-bond effects are invisible to a graph GNN. A **general structural
prior** (`config/protonation.yaml`) re-protonates any weak-acid class (each an anion SMARTS +
genuinely-acidic exceptions) that survives the ladder walk as its conjugate base. It is purely
additive (never removes a proton), so it cannot disturb carboxylates/phosphates/amines.

### 2. Feature extraction (RDKit feature families)

`features/extract.py` (pure) perceives features per ligand: **Donor, Acceptor, Aromatic,
PosIonizable, NegIonizable, LumpedHydrophobe** (one centroid per hydrophobic group, not per
atom). Directional families also emit an orientation vector (donor D→H, acceptor lone-pair,
aromatic ring-normal).

**Feature hierarchy (co-atom resolution).** RDKit tags some atoms with two families at once
(a protonated amine N is `PosIonizable`+`Donor`; a carboxylate O is `NegIonizable`+`Acceptor`),
which double-counts one atom. `features.feature_hierarchy` (config, ordered) resolves **only
truly redundant** ionizable pairs, **per ligand, keyed on the shared atom** (higher subsumes
lower), and fires **only for co-incident atoms** — so genuine dual roles are kept
(`Donor`+`Acceptor` hydroxyls; `Aromatic`+`Acceptor`/`Donor` ring heteroatoms). `Aromatic`+
`LumpedHydrophobe` is deliberately **not** collapsed — a ring is genuinely both. Every collapse
is logged in the JSON provenance and `model_summary.md`.

### 3. The consensus — a molecule-weighted Gaussian occupancy field (KDE)

This is the sole consensus strategy. In → aligned per-molecule feature points; out → consensus
features `(family, position, tolerance, optional direction)`.

1. **Pool points, weight by molecule not by point.** Per feature type, each point is weighted by
   `1/(points that molecule contributes to the type)`, so the unit of evidence is the **distinct
   molecule**, not a molecule that happens to present the feature many times.
2. **Accumulate into a Gaussian-smoothed voxel occupancy field** (voxel/bandwidth ~1.0–1.5 Å).
3. **Extract every local maximum** (no fixed *k*); assign points to the nearest peak (a proximity
   watershed).
4. **Keep a peak** only if its basin's summed molecule weight clears the `occupancy_floor` **and**
   its **support ≥ `min_support_fraction` (0.5)**. Support is a **hard-membership count** —
   distinct ligands with a feature point within `density.membership_radius` (1.5 Å) of the peak
   centre ÷ total ligands — so a far basin outlier cannot inflate it. This is the main
   feature-selection gate.
5. **Collapse each kept basin to one feature**: position = the **peak-local density-weighted
   centroid** (basin voxels *within `membership_radius` of the peak*, so a diffuse tail can't drag
   the centre off the true maximum); tolerance = a **density-quantile core** (`tolerance.quantile`
   0.75 of the field mass, clamped `[1,3]` Å); direction = the mean of the aligned points'
   orientation vectors.

### 4. Cross-family overlap merge

To keep one feature per region, overlapping features from *different* families are merged — the
dominant one (more points, then support) wins, at a fixed 1 Å centre-to-centre cutoff
(`density.merge_radius`) — **except `density.merge_exempt_pairs`**: `Donor`+`Acceptor` and
`Aromatic`+`LumpedHydrophobe` are compatible co-located roles the literature keeps distinct, so
a bidentate hydroxyl's acceptor is not deleted into its donor. `model_summary.md` records every
above-floor removal ("Merged away … in favour of X") and every below-floor cluster.

### 5. Minimum-ligands gate

A cell with **fewer than `selection.min_ligands` (= 10)** aligned molecules is **skipped** and any
prior model for it removed. Below ~10 the ensemble is too sparse to be consensual — a 0.5-support
feature would rest on a couple of ligands. This is the single knob trading target coverage for
per-model robustness.

## No excluded volume

Excluded-volume spheres mark receptor atoms lining the pocket that no ligand reaches — they can
**only** come from a protein structure. These tools are purely ligand-based, so the model and the
`pharmacophore.csv` contain **feature rows only**. (Retained crystal known-actives models in
`catalogue/` were built by the earlier research pipeline *with* excluded volume, so their stored
JSON still carries `ExcludedVolume` rows — historical, not produced by this tool.)

## Outputs (in `--out`)

- **`pharmacophore.csv`** — the primary interchange, one row per feature:
  `family,label,x,y,z,radius,n_points,n_ligands,support,dx,dy,dz` (`dx,dy,dz` = orientation
  vector, blank when none). Feed this to `visualise-pharmacophore`.
- **`pharmacophore.json`** — the canonical, lossless model (schema `pharmpipe.pharmacophore/v1`),
  including provenance (feature-hierarchy collapses, merges, representative ligand).
- **`model_summary.md`** — human-readable summary + the merge / below-floor tables.
- **`features.csv`** — every raw feature point with its cluster id and kept flag (enables the
  support sweep in visualisation and lets you judge clustering quality).
- **`representative_ligand.sdf`** — a real input ligand with clean bond orders, best fit to the
  model (the visual scaffold).
- **`raw_features_<family>.png`** — per-family 3-D scatter of the raw points.

## Knobs

All in `config/pharmacophore.yaml`: feature families/colours, `feature_hierarchy`, `density`
(voxel/bandwidth, `occupancy_floor`, `membership_radius`, `merge_radius`, `merge_exempt_pairs`),
`selection` (`min_ligands`, `min_support_fraction`, `min_cluster_size`), `tolerance`. All
scientific choices; none in code. The build is **deterministic** (fixed grid, no seeding).

---

*Provenance:* the full research write-up (protonation study, feature-hierarchy rationale,
density-field derivation, support-sweep design) is the combined historical note
`catalogue/pharmacophore_method.md`; the reconstructed cross-target evaluation is
`results/RECONSTRUCTION.md`.
