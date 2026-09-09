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

### 1. Protonation and stereochemistry from the docked pose

Each compound is taken to its dominant physiological microstate so that donor/acceptor and
±ionizable perception sees the real ionisation. The subtlety is that the DrugCLIP index
`smiles` column is **neutral** — embedding it directly gives an uncharged amine with no N–H,
so a protonatable nitrogen loses its cation *and* its H-bond donor. The correct pH-7.4 form is
instead carried by the **docked pose** (`<mol_id>_docked.sdf`), so the conformer template is
built from that pose, not the index SMILES:

1. **Protonation.** The docked pose's `protonated_smiles` (fixed at docking prep) supplies the
   pH-7.4 formal charges and hydrogens, so the amine is embedded as its real ammonium — restoring
   both the `PosIonizable` and the `Donor`.
2. **Stereochemistry, including the amine invertomer.** A protonated tertiary amine in a ring is
   a **locked stereocentre** — which face the proton sits on is a genuine diastereomer (the N⁺
   cannot invert without deprotonating), and the SMILES leaves it *unspecified*, so embedding it
   blind yields a **random mixture of both invertomers** whose N–H points to opposite faces.
   `features/conformers.py` therefore reads the configuration off the docked 3-D coordinates
   (`AssignStereochemistryFrom3D`) and enforces it during embedding (ETKDG v3 `enforceChirality`),
   so the ensemble is one diastereomer with a consistent N–H direction. This fixes the *chemistry*
   underlying the weakest geometric feature (the directional donor/acceptor); see
   `pharmacophore_construction.md` §Geometry.

The precedence is **docked pose → docked `protonated_smiles` (protonation only) → neutral index
SMILES** (the last is the honest fallback when a compound has no docked pose; protonation there
would need the `prep` env). A crystal `*.mol2` build instead uses the `prep`-env
pkasolver + weak-acid guard (`pharmacophore_construction.md` §Protonation).

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

A compound is **folded into the model only if** it has a clique of at least
`alignment.min_clique` (default **3**) correspondences — i.e. three of its features that each
**match a same-family feature in the reference** at a mutually consistent geometry — **and** the
resulting superposition clears `alignment.max_align_rmsd`. The `min_clique` match is the *entry
ticket*: once a compound is placed, **all** of its features (including any the reference does not
yet have) are pooled into the cloud the consensus is built from, so it can still introduce a new
feature family. But it must first earn placement by matching ≥3 reference features — because with
fewer than 3 it cannot be located in the frame at all (next). Dropped compounds are recorded
`aligned=False` in `alignment_manifest.csv`.

#### Why the minimum is three features (not a heuristic)

The `min_clique = 3` floor is a **mathematical necessity of the rigid superposition**, not a
tunable quality cut-off. A rigid-body transform in 3-D has **six degrees of freedom** (3
translational + 3 rotational). Counting matched-point constraints against those DOF:

- **1 correspondence** fixes translation but leaves the molecule free to rotate about that point
  — **3 rotational DOF unconstrained**.
- **2 correspondences** fix translation and the axis between the two points, but the molecule can
  still **spin about that axis** — **1 rotational DOF unconstrained**; an infinite family of
  placements satisfies the match equally.
- **3 non-collinear correspondences** are the first case that fully determines all six DOF,
  giving a unique (least-squares / Kabsch) overlay.

So three is the smallest number of matched features from which a molecule can be *placed at all*;
below it the pipeline would have to invent the unconstrained rotation, and any feature
coordinates it then contributed would be artefacts. The gate therefore filters on
**placeability** — a precondition for contributing geometric evidence — not on activity.

This coincides with the field's canonical unit: three features plus their three pairwise
distances define a rigid triangle, the **smallest arrangement with a genuine 3-D shape** — the
basis of 3-point pharmacophore fingerprints and the minimum overlay in the standard engines
(Catalyst/HypoGen, Phase, LigandScout). It is also where the hypothesis becomes **discriminative**:
a two-point relationship (e.g. "a cation and an acceptor ~5 Å apart") is satisfied by a large
fraction of drug-like molecules and carries little selective information; the third point adds the
angular constraint that makes the arrangement specific. Relaxing to two was tested and behaves
exactly as the theory predicts — it admits non-specific two-point matches that, measured on the
target's own key geometry (e.g. the nicotinic cation–acceptor distance), compress and weaken the
consensus at every search depth. The **honest boundary**: ≥3 is a hard geometric floor; where a
formal pharmacophore is genuinely two-point, the *principled* relaxation is not `min_clique = 2`
(which readmits underdetermined non-directional pairs) but **counting a directional feature's
projected orientation point toward the minimum** — a cation + a *directional* acceptor already
supplies ≥3 constraint points and is well-posed, so orientation, not a weaker threshold, is what
would license a two-feature match.

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
