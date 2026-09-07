# CLAUDE.md — Pharmacophore Construction Pipeline

Persistent project context and instructions for Claude Code. Read this fully at the
start of every session before acting.

## Project overview

This project builds an **automated pharmacophore-model construction pipeline**,
generalised across diverse protein classes (work targeting a JCIM publication).

The **known-actives assembly is complete** (Stages 1–3.4 below) for all **17 targets
/ 18 site-slugs** (Nav1.7 splits into a VSD4 and a pore slug): a curated set of
experimentally-bound PDB ligands, filtered to each system's relevant site, aligned
into one reference frame, and partitioned into **cells = (verified pocket × efficacy
sign)**. The tracked deliverable is `catalogue/` (start at `catalogue/DATASETS.md`);
the full target list with per-target flags is "Known-actives reference" below, and
the per-target counts are in `catalogue/run_summary.md`.

**The current stage is pharmacophore construction** from those grouped active poses
(see "Current stage" below). The longer-term flow — **DrugCLIP** virtual screening →
ligand prep → **GNINA** docking → score filtering — remains **out of scope**; do not
build or invoke DrugCLIP/GNINA.

Compute runs downstream on **Gadi (NCI)**, so everything must stay HPC-portable and
reproducible (see operating rules).

## Code quality

Hold all pipeline code to these standards; they override convenience.

**Prefer:** low cyclomatic complexity (small functions, early returns); low
duplication (reuse the IO/parse/path helpers); explicit typed contracts (dataclasses,
signatures, no surprising side effects); testability (pure functions; IO/network at
the edges); modularity (one module = one responsibility — geometry, annotation,
orchestration, visualisation stay separable); Pythonic structures (dataclasses,
comprehensions, `pathlib`, context managers).

**Avoid:** hidden assumptions (no silent defaults that encode a scientific decision;
no inferring meaning from incidental cues like a name substring); **hardcoded domain
knowledge** (efficacy signs, pocket/site identities, exclusions, anchors live in
versioned **config files**, not code logic); unnecessary coupling (depend on narrow
interfaces; a heavy/brittle dep must not block unrelated code).

## Environment & operating rules

Dependency management is **pixi**. Every session:

- Run Python and tooling through pixi (`pixi run python …` or a defined `pixi run
  <task>`). Never invoke a bare ambient `python`.
- Add deps with `pixi add <package>` into the right feature; for pip-only packages
  use that feature's `pypi-dependencies`. Never `pip install` globally.
- Do **not** use the conda `base` environment.
- Keep deps compartmentalised into **features** composed into **environments** sharing
  a common `core`, so a heavy/brittle dep never blocks the rest.

### HPC / Gadi portability (keep true even though we run locally now)

- **Compute nodes have no internet.** All network work (PDB/UniProt/ChEMBL
  downloads, `git`, `pixi install`) runs on a login/data-mover node — never in a
  standard compute job.
- **`/home` is capped at 10 GiB.** `.pixi/` and the pixi cache must not live there:
  on Gadi keep repo+env on `/scratch/<project>/<user>`, set `PIXI_CACHE_DIR` off
  `/home`, and put large reference data on `/g/data`.
- Be polite to external APIs: cap parallelism, add retries/backoff, cache everything
  so re-runs are offline-friendly.

## Repository layout

```
.
├── CLAUDE.md  README.md  pixi.toml / pixi.lock  pyproject.toml
├── config/                    # curated scientific knowledge (no domain facts in code)
│   ├── targets.yaml           #   targets + verified UniProt accessions + options
│   ├── sites.yaml             #   per-target relevant site (anchor, references)
│   ├── pockets.yaml           #   pocket naming, clustering thresholds, markers
│   ├── efficacy.yaml          #   efficacy signs + provenance, keyed by HET
│   └── pharmacophore.yaml     #   Stage-4 feature families, clustering, selection
├── src/pharmpipe/
│   ├── io/                    # structure & ligand parse/write (mmCIF, mol2)
│   ├── pdb/                   # RCSB/UniProt querying, ligand extraction
│   ├── catalogue/             # cataloguing/reporting (Stage 1)
│   ├── sites/                 # site filtering + alignment (Stage 2)
│   ├── groups/                # pocket verification + effect grouping (Stage 3)
│   ├── features/ clustering/ pharmacophore/   # pharmacophore construction (Stage 4)
│   ├── util/                  # http, paths
│   └── config.py  pipeline.py # config dataclasses + Stage-1 orchestration
├── scripts/                   # thin CLI wrappers (one per stage)
├── catalogue/                 # TRACKED deliverable (see catalogue/DATASETS.md)
├── data/                      # GITIGNORED, large (cached mmCIF + intermediate mol2)
└── tests/                     # offline unit tests
```

## Pipeline stages (status)

Each stage writes tracked deliverables under `catalogue/`. Run via pixi tasks
(`scrape-pdb-ligands` → `align-sites` → `resolve-efficacy` → `group-effects` →
`protonate-ligands` → `build-pharmacophores`; add `-e viz` to bake `.pse`). The
`protonate-ligands` prep step runs in the isolated `prep` env (`pixi run -e prep
protonate-ligands`) and is networked/one-off; the build itself is offline. The
downstream DrugCLIP→GNINA flow stays out of scope.

1. **Scrape & catalogue** (`pdb/`, `catalogue/`) — verified UniProt accessions, dated
   RCSB search, curated ligands (drop additives/buffers; keep cofactors), bound-pose
   mol2. Outputs: `unique_ligands.csv`, `per_structure.csv`, `resolved.json`,
   `ligand_catalogue.{md,xlsx}`. **Done.**
2. **Site filtering & alignment** (`sites/`, `config/sites.yaml`) — keep only poses at
   each system's relevant site, superpose into one reference frame, per-target `.pse`.
   Output: `site_filter.csv`. **Done.** The superposition is a sequence-aware global
   fit used only as an initialiser, then an **iterative pocket-local ICP refinement**
   (re-pair pocket residues each iteration; fit on anchor-weighted backbone atoms) so
   the geometry of the residues lining the pocket stays constant across structures —
   essential for low-identity surrogates. Knobs are in `config/sites.yaml` `defaults`
   (`refine_*`, `anchor_weight_sigma`, `use_backbone`); QC the overlay with
   `scripts/diag_alignment.py`. Rationale + before/after: `catalogue/realignment_report.md`.
3. **Effect grouping with pocket verification** (`groups/`, `config/{pockets,efficacy}.yaml`).
   **Done, offline** (cached structures + catalogue). Pocket identity is **geometric**
   (native contact fingerprints, chain-agnostic `RESNAME+authseqnum`, union-find
   clustering) so it is computed in code; pocket *names* and efficacy *signs* are
   curated config, never inferred. Poses partition into **cells = (pocket × efficacy)**;
   covalent/degrader/substrate ligands route to a `separate_state` track, and
   `unknown` efficacy + out-of-pocket `quarantine` poses are first-class review
   outputs, never force-bucketed. Outputs per target: `effect_groups.json`,
   `<slug>_stage3_report.md`, `groups/<pocket>__<efficacy>/`, `review/…`,
   `<slug>_grouped.pse`, `datasets/{all_poses,representative}/`; cross-target master
   `catalogue/datasets/`; run record `catalogue/run_summary.md`.
   - **3.3 — efficacy resolution** (`groups/resolve.py`, `realign.py`): `resolve-efficacy`
     (network) resolves previously-`unknown` ligands HET→InChIKey→ChEMBL parent→
     subtype-specific mechanism→sign into `stage3_efficacy_resolved.csv` (the loader's
     fallback tier). adrb2 collapses to one orthosteric pocket; GABA-A uses
     `realign_global` to place the benzodiazepine vs orthosteric sites at their true
     subunit interfaces. SERDs/degraders auto-route to `separate_state`; conflicting
     subtypes stay `unknown`.
   - **3.4 — literature efficacy curation**: where ChEMBL had no MoA, efficacy
     *direction* was read from each structure's primary publication and merged into
     `config/efficacy.yaml` as `source: literature` (98/158 worklist ligands). The
     **subtype rule** is enforced: ligands characterised only at a different subtype,
     wrong-target "mismatch" structures, and additives stay `unknown` → never enter
     cells. Allosteric vs orthosteric is separated **geometrically**, not from the
     `site` field — NS9283 (NSE) reuses the orthosteric aromatic box, so a per-pose
     marker override (`config/pockets.yaml` `accessory.marker_hets: [NSE]`) gives it
     its own `accessory__positive` cell. Provenance lives under `catalogue/curation/`
     (`efficacy_curation_README.md` + the batch-1/batch-2 traceability tables); the
     worklist is regenerable with `scripts/make_literature_worklist.py`.

4. **Pharmacophore construction** (`features/`, `clustering/`, `pharmacophore/`,
   `config/pharmacophore.yaml`) — ligand-based ensemble pharmacophore per cell.
   **Current stage**; see the dedicated section below. Output:
   `catalogue/<slug>/pharmacophores/<cell>/`.

**Efficacy provenance tiers** (highest first): `literature` > `prelabelled` >
`curated` > the `stage3_efficacy_resolved.csv` ChEMBL fallback. An explicit ligand
entry always beats the CSV; `unknown` is never defaulted away.

## Stage 4 — pharmacophore construction (current)

Builds a **ligand-based ensemble pharmacophore** per cell with a **single consensus
strategy — a Gaussian occupancy field (KDE)** whose peaks become features (RDKit
feature extraction à la TeachOpenCADD T009 feeds it). The build unit is one **cell** —
`catalogue/<slug>/groups/<pocket>__<efficacy>/`, mol2 poses already superposed in a
common frame, same pocket, same efficacy sign. One hypothesis per cell. The pipeline
is **general**: its real entry point takes *any* directory of aligned mol2 and emits a
model; the catalogue batch mode is a convenience over that.

Run: `pixi run build-pharmacophores --catalogue` (or `--target <slug>`, or
`--input DIR --out DIR --smiles ligands.csv`). Offline. Every model writes to the single
namespace `catalogue/<slug>/pharmacophores/<cell>/`.

**Docked screening sets (`--docked-dir`).** A second one-shot builds a hypothesis from a
**DrugCLIP → GNINA** virtual-screening hit set, treating the docked poses as one aligned
active set (all docked into the same receptor frame, so already superposed): `pixi run
build-pharmacophores --docked-dir DIR --out DIR --top-hits N [--top-poses n]
[--pose-score cnnaffinity] [--max-vina 0] [--reference-pdb receptor.pdb]`. The directory is
a folder of GNINA `<mol_id>_docked.sdf` files (one compound each, several docked poses) plus
a DrugCLIP rank `index_*.csv` (`mol_id,…,drugclip_score`, auto-detected or `--index`). It
takes the **top `N` compounds by DrugCLIP score** and the **best `n` poses of each (default
1)**, then runs the same build/summary/viz path as `--input`. **Pose selection is
quality-aware** (`--pose-score`, default `cnnaffinity`; also `vina`/`cnnscore`/`cnn_vs`, plus
`--max-vina` clash filter): GNINA writes poses in **`CNNscore`** order, but `CNNscore` ranks
physically-clashing poses highly (poses ≥3 are majority Vina-positive), so selecting by
**`CNNaffinity`** or **`minimizedAffinity`** instead is what recovers the correct model.
**Empirically (5KXI nAChR):** `--top-hits 20–30 --top-poses 1 --pose-score cnnaffinity`
recovers the full nicotinic **cation + aromatic + acceptor** 3-point pharmacophore with the
literature cation–acceptor distance (~5.0 Å); more poses add scatter, not signal, and
DrugCLIP score does **not** correlate with GNINA pose quality (they are complementary
filters, so docking cannot be skipped by trusting DrugCLIP rank). It is **offline with no protonation subprocess** — the
SDFs already carry each pose's pH-7.4 `protonated_smiles`, which is used as the
`AssignBondOrdersFromTemplate` template (falling back to a direct SDF read). **Each pose is
an independent observation** (ligand_id `<mol_id>__p<k>`), so support/molecule-weighting key
on the pose: at the default one pose/hit the unit of evidence is the compound; `--top-poses
>1` lets a compound's alternative placements count separately. Provenance (rank, pose, score,
load method per pose) is written to `docked_manifest.csv`; the loader is
`pharmpipe/features/dock_load.py` and the build core is shared via
`pharmpipe.pharmacophore.run.build_from_molecules`. Docked input dirs are gitignored bulk
input (like `data/`), not a tracked deliverable.

**Minimum-docking (`--seed-docked`).** A validation against the native 5KXI nicotine crystal
pose showed `--docked-dir` docks far more than needed and that its directional acceptor is
corrupted by a GNINA **ring-flip** (cation/aromatic land on the crystal, the acceptor lands
~3.5 Å off); DrugCLIP relevance and GNINA pose quality are **orthogonal**, and the model is
front-loaded. **Recommended recipe `--top-hits 100 --seed-k 5`:** `pixi run
build-pharmacophores --seed-docked DIR --out DIR --top-hits 100 [--seed-k 5]
[--reference-pdb receptor.pdb]` docks only the top-`seed_k` compounds, uses their poses as a
**bioactive-frame seed**, and incrementally aligns + folds in ranked compounds 6..100 by
**feature-clique matching** (correspondence graph on **relative intra-molecular feature
distances** → Bron–Kerbosch → Kabsch, `pharmacophore/align.py`) over a **conformer ensemble**
(`features/conformers.py`), updating the model (running mean) as it grows — no protein needed.
A compound is folded in only if its best clique RMSD clears `alignment.max_align_rmsd` (poor
fits dropped, recorded `aligned=False` in `alignment_manifest.csv`) — the key quality gate for
the incremental update. **Engine-agnostic seeding:** the seed poses are any docked SDFs (GNINA
now, **AutoDockFR** later — only the top-`seed_k` need SDFs, the rest embed from index SMILES;
the loader falls back to pose 1 when GNINA score tags are absent; see `docs/adfr_seeding.md`).
Ligands are protonated from their docked-SDF `protonated_smiles` when present (offline), else
via the `prep` env. On 5KXI it recovers the 3-point model with cation/aromatic **~1 Å from the
crystal nicotine** while docking five compounds, not the library. The **acceptor stays
low-confidence** (inherits the flip) and directional features are flagged `†` in
`model_summary.md`. Knobs live in `config/pharmacophore.yaml` `alignment:`; the 5KXI parameter
benchmark is `scripts/troubleshoot_seed_align.py` →
`catalogue/screening_eval/nachr_a4b2_positive/seed5_benchmark.md`.

**Generalised init + EM refinement.** The alignment is a general engine: the frame is initialised
**seedless** (`--seedless`, from the top-ranked compound's lowest-energy conformer — the
**recommended** default), from the docked top-`seed_k`, or from an arbitrary 3D-coordinate `--seed
PATH.sdf` (a crystal ligand or docked poses). A seed remains a supported option but **generally
works less effectively** than seedless — a docked/crystal frame can import a bad pose that biases
the consensus (seedless matches or beats a seed on 10/11 targets; see below). After the growing pass an **EM refinement** (`alignment.em_iterations`)
re-aligns every compound to the current consensus — **re-selecting each one's best conformer**, which
removes the effect of a sub-optimal discrete conformer chosen early — and recomputes the consensus
until the feature-centre shift < `alignment.em_tol`. High-energy conformers are discarded up front
(`alignment.energy_window`). `--align-only` emits just the **aligned compound set**
(`aligned_compounds.sdf` + `aligned_points.csv` + manifest) so the KDE can be re-run on it; the
default also runs the KDE. **Thesis result — the chemistry carries the geometry.** On nAChR, seedless recovers the 3-point model
with internal geometry matching the known-actives model as well as the crystal/docked seeds
(cation–aromatic Δ0.10 Å, aromatic–acceptor Δ0.03 Å), in one EM iteration
(`scripts/seed_necessity.py` → `.../nachr_a4b2_positive/seed_necessity.md`). **This generalises**:
across the **11 targets with a known-actives ground truth**, seedless matches or beats the docked
seed in **10/11** — and is *often strictly better* (on cdk2 the docked seed failed outright while
seedless recovered every family; a bad docked pose can actively bias the frame). So **a docked/crystal
seed is not necessary for correct geometry** — the shared *rigid cores* carry it; the seed only speeds
convergence (the lone exception, ca2, has few rigid multi-feature cores + an unmodelled metal feature).
Experiment: `scripts/seed_necessity_all.py` → `catalogue/screening_eval/seed_necessity_report.md`.

**Directional (orientation-aware) matching** (`alignment.use_directions`, default on). Perception
(`features/extract.py`) now emits an orientation vector per directional feature — Donor D→H,
Acceptor lone-pair (from the heavy neighbours, which distinguishes a ring-flipped nitrogen), and
Aromatic ring-normal. The superposition fits H-bond donor/acceptor **projected points** (centre +
`projected_length` Å along the vector) jointly with positions, so a feature must agree in
*orientation*, not just position; the consensus `direction` field is then populated from the aligned
points. On nAChR the acceptor's off-native distance improves modestly (1.54→1.41 Å, docked seed) —
small because seed-align + EM already place it well (~1.5 Å); the flip was far more damaging in the
`--docked-dir` full-consensus path, which is where directionality should matter most.
A/B: `scripts/directional_benchmark.py` → `.../nachr_a4b2_positive/directional_benchmark.md`.

**Method vs the crystal + literature pharmacophores** (`scripts/alignment_vs_reference.py` →
`catalogue/screening_eval/alignment_vs_reference.md`). The seedless alignment model scored against
both references across the 11 known-actives targets: **vs crystal (known-actives)** 5 MATCH /
6 PARTIAL / **0 MISMATCH** (families recovered in 11/11; geomD inflated only where the feature is
the directional acceptor); **vs literature** 9/9 MATCH-or-PARTIAL on family composition. So the
DrugCLIP alignment reproduces the experimentally- and literature-derived pharmacophores at the
family level everywhere, and geometrically for the pose-invariant features; the acceptor is the
one soft spot (directional).

**Orthogonality.** The DrugCLIP paths (`--docked-dir`, `--seed-docked`) are an *orthogonal
application layer* over the shared Stage-4 core: they reuse `build_density`/`io`/`viz` through
the same narrow interfaces and add nothing to the known-actives / catalogue build, whose
models are unchanged. The `alignment:` config block is additive and consumed only by
`--seed-docked`. The pipeline never invokes GNINA/DrugCLIP — docked SDFs are consumed as input.

**Library-wide screening evaluation** (`src/pharmpipe/screening/`, `config/screening.yaml`,
`config/literature_pharmacophores.yaml`). A DrugCLIP→GNINA deposit of ~18 targets (docked poses
+ per-target indexes) is organised into `data/screening/<key>/` by
`scripts/organise_screening.py` (curated PDB→slug crosswalk, each pairing validated by ≥99%
mol_id overlap; raw `out/`+`website_output/` gitignored). `scripts/evaluate_screening.py` then
builds **both** methods per target — full-docking over all poses and seed-alignment at the
config `alignment_depth` (=50, chosen by `scripts/eval_align_depth.py` against the known-actives
models) — and `compare.py` scores each vs the known-actives model + the literature by
feature-family recall + internal geometry (frame-independent). Tracked deliverable:
`catalogue/screening_eval/` (per-target models + `comparison_report.md`; the chemistry-vs-geometry
diagnosis is `geometry_limit_report.md`). Orthogonal to the catalogue build; scientific choices
(crosswalk, depth, literature features) live in config. The upstream **source library** DrugCLIP
screens against is `molecule_library/` (~18.6 M molecules, ~48 GB of vendor SDFs; **gitignored**
bulk input) — summarised in `docs/molecule_library.md` (+ `docs/molecule_library_manifest.csv`).
(An earlier swappable k-means
strategy and its `pharmacophores_density/` split have been **removed** — density/KDE is
the sole method. In/out contract: aligned per-molecule feature points in → consensus
features `(family, position, tolerance, optional direction)` out.)

**Modules** (pure core, IO at the edges):
- `pharmpipe/features` — `extract.py` (pure: feature factory → `FeaturePoint`/
  `FeatureTable`) + `load.py` (IO). The loader is the critical bit: our mol2 are
  heavy-atom-only, so RDKit's direct read misses donors / fails to kekulize. It
  prefers **SMILES-template** bond assignment (`AssignBondOrdersFromTemplate` on a
  connectivity-only graph; SMILES from the target's `unique_ligands.csv` keyed by HET)
  → falls back to a direct read → skips+logs. Per-pose coverage is recorded.
- `pharmpipe/pharmacophore` — `density.py` (the consensus strategy: molecule-weighted
  Gaussian occupancy field → peaks/watershed → occupancy-floor → membership-radius
  support → centroid/spread + cross-family merge + excluded volume), `build.py` (the
  shared, strategy-agnostic primitives density reuses: `feature_radius`, the cross-family
  overlap merge + `MergeRecord` bookkeeping, per-family labelling, representative-ligand
  pick), `model.py` (`Pharmacophore`, schema `pharmpipe.pharmacophore/v1`, optional
  per-feature `direction`, JSON round-trip), `io.py`, `viz.py` (matplotlib raw-feature
  3D plots), `config.py`, `run.py` (orchestration).

**Config** `config/pharmacophore.yaml` — feature families/colours, `feature_hierarchy`,
`density` knobs (voxel/bandwidth, occupancy floor, **`membership_radius`**, cross-family
`merge_radius`, excluded volume), selection (`min_ligands`, `min_support_fraction`,
`min_cluster_size`), tolerance model. All scientific choices; none in code.

**Feature hierarchy (co-atom resolution; §3.1 of the method doc).** RDKit tags some
atoms with two families at once (protonated amine N = `PosIonizable`+`Donor`; carboxylate
O = `NegIonizable`+`Acceptor`), which double-counts one atom and lets the redundant partner
win the support vote (the symptom: a `PosIonizable` pocket reporting `Donor`).
`features.feature_hierarchy` (ordered groups, config) resolves **only truly redundant**
ionizable pairs **at extraction, per ligand, keyed on the shared atom** (higher subsumes
lower); it fires **only for co-incident atoms** so genuine dual roles (`Donor`+`Acceptor`
hydroxyls, `Aromatic`+`Acceptor`/`Donor` ring heteroatoms) are kept. **`Aromatic`+`LumpedHydrophobe`
is deliberately NOT collapsed** — an aromatic ring is genuinely both aromatic and lipophilic,
and literature (Catalyst/HypoGen) reports a hydrophobic feature on rings, so both perceptions
are kept (and the pair is exempt from the overlap merge, below). It **never overrides a genuine
count** (the cross-family merge stays support/size-based). Each collapse is logged (`kept ← dropped` +
ligands) in the JSON provenance and `model_summary.md`.

**Method choices — density/KDE** (all in `config/pharmacophore.yaml`; full write-up in
`catalogue/pharmacophore_method.md`): features use RDKit **`LumpedHydrophobe`** (one
centroid per hydrophobic group, not per atom); a cell with **< `min_ligands` (10)** known
actives is **skipped and its output removed** (below ~10 poses the ensemble is too sparse to
trust — a 0.5-support feature rests on a couple of ligands; raised from 3 after a coverage/
quality review, which now builds 13 of the catalogue's cells). Per feature type, points are weighted by
**1/(points that molecule contributes to the type)** so the unit of evidence is the
**distinct molecule** (optional inverse-scaffold-frequency), a Gaussian-smoothed **voxel
occupancy field** (voxel/bandwidth ~1.0–1.5 Å) is built, and features are **all local
maxima** (no `k`) with proximity watershed. A peak survives only if its basin's summed
molecule weight ≥ **`occupancy_floor`** **and** its **support ≥ `min_support_fraction`
(0.5)**. **Support is a hard-membership count** — distinct ligands with a feature point
within **`density.membership_radius` (1.5 Å)** of the peak centre ÷ total ligands — so a
far basin outlier no longer inflates it (this is the main feature-selection gate; support
also drives the sweep). Feature **position = peak-local density-weighted centroid** (the
basin voxels *within `membership_radius` of the peak*, so a diffuse tail / neighbouring lobe
can't drag the centre off the true maximum — this recovered e.g. the esr1 aromatic A-ring,
support 0.31→1.00), **tolerance = density-quantile core** (still over the whole basin;
`tolerance.quantile`=0.75 of the field mass, clamped `[1,3]` Å; `rmsd` selectable),
**direction** plumbed but `None` until perception emits per-point vectors. Peak resolution
is decoupled via **`density.peak_bandwidth`** (a separate, sharper peak-detection field);
it defaults to `null` (= `bandwidth`) and is **off** because a sharper global field
fragments broad conserved sites below the basin `occupancy_floor` — re-enable only once the
floor/merge are split-robust. Then a **cross-family overlap merge** keeps one feature per region — dominant
(more points, then support) wins, **fixed 1 Å centre-to-centre cutoff** (`merge_radius:
1.0`; `null` = old geometric 1–3 Å) — **except `density.merge_exempt_pairs`** (`Donor`+`Acceptor`,
`Aromatic`+`LumpedHydrophobe`): compatible co-located roles literature keeps distinct, so a
bidentate OH's acceptor is **no longer** deleted into its donor (this recovers e.g. estradiol's
17β-OH acceptor and the β2 catechol acceptors). `model_summary.md`'s **"Merged away …
in favour of X"** table records every above-floor removal (a "Below the support/size
floor" table lists the rest, both with **`Support`** and an uncapped **`Occupancy`** =
points ÷ ligands). Finally **excluded-volume** grey spheres are added from
reference-receptor atoms lining the pocket that no ligand reaches (exempt from the merge).
**Deterministic** (fixed grid, no seeding). The tolerance radius is stored in the JSON —
**not** the PyMOL sphere size: the viz draws every ligand feature as a **fixed 1.25 Å-radius
mesh (wireframe) sphere plus an opaque centre pseudoatom** (`PH4_SPHERE_RADIUS`, a pure
display size), and **Excluded-Volume markers are part of the model but NOT drawn**. Each
model dir also carries a **`<cell>_sweep.pse`** support-cutoff sweep (all raw clusters
across 20 PyMOL states, support cutoff 0.05→1.00 using the same membership radius; baked
via `--render-sweeps`, and by the one-shot). Family colours: HBD/Donor pink, HBA/Acceptor
green, hydrophobic cyan, Aromatic yellow, PosIonizable red, NegIonizable orange,
ExcludedVolume grey.

**Protonation (pH 7.4) preprocessing** (§2 of the method doc): before the build,
`scripts/protonate_ligands.py` (pixi `prep` env) predicts pKa with **pkasolver** and
writes each HET's dominant pH-7.4 microstate to `catalogue/<slug>/protonated_ligands.csv`
(pure ladder-walk in `pharmpipe/prep/protonate.py`). The loader prefers it over the
neutral `unique_ligands.csv` SMILES, and `AssignBondOrdersFromTemplate` carries the
template's formal charges onto the pose — so donor/acceptor/±ionizable perception sees
the real ionisation, feeding feature perception. A **weak-acid guard**
(§2.1; `config/protonation.yaml`, applied by `neutralize_weak_acids`) corrects
pkasolver's documented blind spot — it systematically *over-deprotonates* weak acids
(O–H, N–H) on poly-ionizable scaffolds (phenols, alcohols, amides, primary sulfonamides,
amino-heteroaromatics) because adjacent-charge / *ortho* H-bond / macrostate effects are
invisible to a graph GNN (QupKake shares this and was rejected as no better for the cost).
The guard is a **general structural prior, not per-compound literature pKa**: config
defines weak-acid classes (each an anion SMARTS + genuinely-acidic exceptions) whose pKa
is well above 7.4; any that survive the ladder walk as their conjugate base are
re-protonated in the final microstate. It is purely additive (never removes a proton), so
it can't disturb carboxylates/phosphates/amines. Sulfonamides are neutralised to the
solution state (the CA2 Zn-bound-anion case is out of scope). Re-protonated sites are
logged per row (`guard_neutralized` column, `method=pkasolver+weak_acid_guard`). pkasolver
needs a pinned 2021-era stack (py3.10/torch1.11/PyG2.0.1, the `prep` env) and is vendored
under `external/` (gitignored); the `protonated_ligands.csv` outputs are the tracked deliverable.

**Outputs** per model dir (`catalogue/<slug>/pharmacophores/<cell>/`):
`pharmacophore.json` (canonical, method-stable; provenance includes the representative
ligand), `features.csv` (every raw point + cluster id + kept flag),
`representative_ligand.sdf` (a real cell ligand, clean bond orders, best fit to the
model — the visual scaffold), `raw_features_<family>.png` (per-family 3D scatter;
centre-marker area ∝ cluster population), `pharmacophore.pml`, `model_summary.md`.
Inspect a model in PyMOL with `pixi run -e viz pymol -cq scripts/pymol_pharmacophore.py
-- --pharmacophore … [--features … --compounds … --out …]` (defaults to the
representative ligand when `--compounds` is omitted).

**Respect the review tracks** — the batch modes build only `groups/` cells, never
`separate_state` / `unknown` / `quarantine`. Gate `surrogate`/`chimera`/`mismatch`
poses per the caveats in `catalogue/curation/efficacy_curation_README.md` before
pooling: a surrogate pose carries the surrogate's pocket geometry, and `mismatch`
poses are wrong-target structures the labels exclude but a geometry pipeline must drop
explicitly.

## Known-actives reference (Stages 1–3.4 complete)

Durable reference for the assembled set; UniProt hints were verified at scrape time
and recorded per target in `catalogue/<slug>/resolved.json`.

### Targets

UniProt hints are **starting points**, not authoritative — the verified accessions
live in each `resolved.json`.

| Target | UniProt hint | Notes / flags |
|---|---|---|
| Nicotinic AChR (α4β2) | CHRNA4 P43681, CHRNB2 P17787 | Neuronal nicotinic α4β2. Ground truth often from **AChBP surrogate** co-crystals — included and labelled as surrogates. |
| Estrogen receptor α | ESR1 P03372 | Mostly LBD; large set. |
| HIV-1 protease | from Gag-Pol (e.g. P04585) | Large. **Bridging waters** functionally important — noted. |
| β2-adrenoceptor | ADRB2 P07550 | GPCR; **fusion partners** (T4L/BRIL) + thermostabilising mutations — don't catalogue fusion-partner ligands. |
| CDK2 | P24941 | ± cyclin A; **bridging water** in hinge/ATP site. |
| Carbonic anhydrase II | CA2 P00918 | Isoform II. Catalytic **Zn²⁺ cofactor — kept.** |
| Acetylcholinesterase | human ACHE P22303 | Species ambiguity (*Torpedo*, mouse) resolved at scrape time. |
| CavAb | NavAb (A. butzleri) ~A8EVM5 | **Engineered surrogate** (Ca²⁺-selective NavAb mutant); small set, flagged. |
| Cyclooxygenase-2 | human PTGS2 P35354 | Species ambiguity resolved. **Heme** cofactor — kept. |
| HMG-CoA reductase | HMGCR P04035 | Statin/inhibitor complexes. |
| GABA-A receptor | GABRA1 P14867, GABRG2 P18507, + β | Pentameric, many compositions, mostly cryo-EM; lipids/detergents filtered. |
| Norepinephrine transporter | SLC6A2 P23975 | SLC6 transporter (**not** an adrenergic receptor). **dDAT** surrogate poses included only where wanted and labelled. |
| Nav1.7 (sodium channel) | SCN9A Q15858 | **Two drug sites, two slugs**: `nav1_7_vsd4` (VSD4 aryl-sulfonamide) + `nav1_7_pore` (central-cavity local-anaesthetic). Sites sit in different domains so they don't co-superpose — each anchored separately. Channel block = `negative`. |
| Glucocorticoid receptor | NR3C1 P04150 | Steroid LBD (nuclear-receptor analogue of ESR1). Some deposits are GR–Hsp90–p23 complexes — **Hsp90 ATP/ADP routed out**, not GR ligands. |
| Adenosine A₂ₐ receptor | ADORA2A P29274 | GPCR; **fusion partners** (BRIL/T4L) + thermostabilising mutations — don't catalogue fusion-partner ligands. Large set; **run uncapped** (the default 100-pose, best-resolution-first cap dropped the entire lower-resolution agonist class, emptying the `positive` cell). |
| Muscarinic M2 | CHRM2 P08172 | GPCR; acetylcholine receptor disambiguated to **muscarinic M2**. Distinct **extracellular allosteric vestibule** above the orthosteric site (geometric marker split). |
| Dopamine receptor D1 | DRD1 P21728 | GPCR; dopamine receptor disambiguated to **D1** (most structurally covered of D1–D5). Mostly **active-state Gs complexes** — **G-protein GDP/GTP/Mg routed out**, not receptor ligands; **fusion partners** (BRIL/T4L) — don't catalogue fusion-partner ligands. Structurally **agonist-dominated**: the `orthosteric__positive` cell is large; `orthosteric__negative` is one ligand (flupentixol). |

### Resolved scope decisions (durable)

- **Organism scope:** human where possible; surrogates included only as labelled
  gap-fillers (AChBP for nAChR, dDAT for NET) — see config + `resolved.json`.
- Species/isoform/subunit ambiguities (AChE, COX-2, CA isoform, GABA-A composition)
  were resolved at scrape time and recorded per target.
- **Known data-hygiene follow-up:** upstream UniProt mapping pulled a few wrong-target
  structures (C3aR/TAAR1/D1–D5/DAT into adrb2/net) and additives into the pools; they
  stay `unknown` and are correctly excluded from cells, but still sit in
  `datasets/all_poses`. A scrape-time mismatch/additive filter is the clean upstream fix.
