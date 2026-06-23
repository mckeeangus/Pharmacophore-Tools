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
`build-pharmacophores`; add `-e viz` to bake `.pse`). The downstream DrugCLIP→GNINA
flow stays out of scope.

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

Builds a **ligand-based ensemble pharmacophore** per cell, adapting the TeachOpenCADD
T009 workflow (extract RDKit features → cluster per family → cluster centres become
the model). The build unit is one **cell** —
`catalogue/<slug>/groups/<pocket>__<efficacy>/`, mol2 poses already superposed in a
common frame, same pocket, same efficacy sign. One hypothesis per cell. The pipeline
is **general**: its real entry point takes *any* directory of aligned mol2 and emits a
model; the catalogue batch mode is a convenience over that.

Run: `pixi run build-pharmacophores --catalogue` (or `--target <slug>`, or
`--input DIR --out DIR`). Offline.

**Modules** (pure core, IO at the edges):
- `pharmpipe/features` — `extract.py` (pure: feature factory → `FeaturePoint`/
  `FeatureTable`) + `load.py` (IO). The loader is the critical bit: our mol2 are
  heavy-atom-only, so RDKit's direct read misses donors / fails to kekulize. It
  prefers **SMILES-template** bond assignment (`AssignBondOrdersFromTemplate` on a
  connectivity-only graph; SMILES from the target's `unique_ligands.csv` keyed by HET)
  → falls back to a direct read → skips+logs. Per-pose coverage is recorded.
- `pharmpipe/clustering` — a `Clusterer` Protocol (`fit_predict(coords)->labels`) is
  the **only** contract the builder depends on, so methods are drop-in. `kmeans.py`
  is `KMeansSilhouette` — k chosen by **silhouette score**, not the tutorial's
  `k=n/kq` heuristic. Add a method in `registry.py`; output format is unchanged, so
  methods stay comparable.
- `pharmpipe/pharmacophore` — `build.py` (pure assembly: cluster→centre→support→
  tolerance→select), `model.py` (`Pharmacophore`, schema `pharmpipe.pharmacophore/v1`,
  JSON round-trip), `io.py`, `viz.py` (matplotlib raw-feature 3D plots), `config.py`,
  `run.py` (orchestration).

**Config** `config/pharmacophore.yaml` — feature families/colours, clustering
method+params, selection (min support fraction, min size, top-N), tolerance model.
All scientific choices; none in code.

**Outputs** per model dir (`catalogue/<slug>/pharmacophores/<cell>/`):
`pharmacophore.json` (canonical, method-stable), `features.csv` (every raw point +
cluster id + kept flag), `raw_features_<family>.png` (per-family 3D scatter — the
"sense of the data" view for judging clustering quality), `pharmacophore.pml`,
`model_summary.md`. Inspect a model in PyMOL with
`pixi run -e viz pymol -cq scripts/pymol_pharmacophore.py -- --pharmacophore … --compounds … [--features … --out …]`.

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
