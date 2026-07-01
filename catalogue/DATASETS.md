# Catalogue layout & datasets

`catalogue/` is the tracked deliverable of the known-actives assembly (Stages 1–3.4).
`data/` (gitignored) holds the large cached mmCIF and intermediate mol2; everything
needed to consume or audit the result lives here.

## Pose file naming

Every pose is one mol2 file named:

```
<PDB>_<HET>_<chain><authSeqId>.mol2      e.g. 6HUO_08H_D501.mol2
```

`<PDB>` 4-char entry · `<HET>` PDB chemical-component (ligand) code · `<chain><authSeqId>`
the ligand instance's author chain + residue number (disambiguates copies within an entry).
All poses for a target share one superposed reference frame (Stage 2 / Stage 3 alignment).

## Per-target directory — `catalogue/<slug>/`

| Path | What it is |
|---|---|
| `unique_ligands.csv` | Stage 1 — one row per kept ligand (HET, name, counts, flags). |
| `protonated_ligands.csv` | Stage-4 prep — HET → dominant **pH-7.4 microstate** SMILES (pkasolver pKa + ladder walk, with the `config/protonation.yaml` weak-acid guard) + predicted pKa list; `guard_neutralized` records any weak-acid group re-protonated by the guard as `<class>:<count>` (e.g. `phenol:2;amide:1`). The loader prefers it over the neutral SMILES. |
| `per_structure.csv` | Stage 1 — one row per (structure × ligand) curation decision. |
| `resolved.json` | Verified UniProt accession(s) + scrape provenance for the target. |
| `site_filter.csv` | Stage 2 — every ligand instance with its at-site/off-site status, distance-to-anchor and pocket RMSD. |
| `effect_groups.json` | Stage 3 — machine-readable assignment of every pose to a cell / review track. |
| `<slug>_stage3_report.md` | Stage 3 — human-readable per-target report. |
| `<slug>_grouped.pml` / `.pse` | PyMOL session: reference + all cells, recoloured by efficacy (green=positive, salmon=negative, yellow=neutral). |
| `groups/<pocket>__<efficacy>/` | **The cells** — mol2 poses partitioned by (verified pocket × efficacy sign), each with a ligand-only `.pml`/`.pse`. |
| `review/{separate_state,unknown,quarantine}/` | First-class review tracks, never force-bucketed (see below). |
| `datasets/all_poses/` | Every kept pose for the target (one mol2 each) + a combined `.pml`/`.pse`. |
| `datasets/representative/` | One pose per ligand (best resolution) + a combined `.pml`/`.pse`. |
| `pharmacophores/<pocket>__<efficacy>/` | Stage 4 — the ensemble pharmacophore built from that cell (see below). |

## Cells — `groups/<pocket>__<efficacy>/`

A cell is the unit a single pharmacophore hypothesis is built from: a geometry-verified
pocket crossed with a curated efficacy sign. Pockets are named in `config/pockets.yaml`;
efficacy signs come from `config/efficacy.yaml` (provenance: literature > prelabelled >
curated > ChEMBL-CSV fallback). Cells present across the 18 site-slugs (17 biological
targets; Nav1.7 is split into a VSD4 and a pore slug):

`orthosteric`/`lbp`/`active_site`/`atp_site`/`gorge`/`cox_channel`/`hmg_site`/`dhp_site`/
`central_s1`/`vsd4_site`/`pore_site` × `{positive, negative, neutral}`, plus the nAChR
`accessory__positive` PAM site and the GABA-A `bzd_site__{positive,neutral,negative}`
benzodiazepine split. The muscarinic-M2 extracellular `allosteric` marker is configured
but currently unpopulated (its poses fall outside the Stage-2 orthosteric cutoff).

> **Batch-2 (2026-06-19) — complete.** `nav1_7_vsd4`, `nav1_7_pore`, `gr_nr3c1`,
> `adora2a`, `chrm2` are built through Stage 3.4 with literature efficacy curation
> merged (provenance under `curation/`). Populated cells: `gr_nr3c1` lbp+/−;
> `adora2a` orthosteric +/neutral/−; `chrm2` orthosteric +/−;
> `nav1_7_vsd4`/`nav1_7_pore` blocker-only (−).
>
> **Batch-3 (2026-06-23) — complete.** `drd1` (dopamine receptor D1) built through
> Stage 3.4 with literature efficacy curation merged (provenance under `curation/`,
> batch-3 files). D1 structural coverage is **agonist-dominated** (almost every
> deposit is an active-state Gs complex): populated cells `orthosteric__positive`
> (16 ligands) and `orthosteric__negative` (one ligand, flupentixol); G-protein
> GDP/GTP routed to `separate_state`.

## Review tracks — `review/`

| Track | Meaning |
|---|---|
| `separate_state` | Covalent adducts, degraders (SERD/PROTAC/glue), catalytic substrates/cofactors — non-equilibrium geometry; excluded from agonist/antagonist maps. |
| `unknown` | Efficacy direction not establishable for *this* target/subtype from available evidence; held out rather than guessed. |
| `quarantine` | Pose survived the coarse Stage-2 filter but does not populate a verified pocket (outlier). |

## Cross-target master — `catalogue/datasets/`

`all_poses/` and `representative/` pool every target into one frame-agnostic set
(per-target frames are independent), each with a baked `.pse`. Use the per-target
`groups/` cells as pharmacophore inputs; the master sets are for cross-target overview.

## Pharmacophores (Stage 4) — `pharmacophores/<pocket>__<efficacy>/`

One ligand-based ensemble pharmacophore per cell, built from the RDKit features of that
cell's poses (see `config/pharmacophore.yaml`; method/params recorded in each model).
**The full method — feature families, both consensus strategies, selection, overlap
merging, tolerance, excluded volume, the visualisation, and what "cluster size" means —
is documented in [`pharmacophore_method.md`](pharmacophore_method.md).** Headline choices:

- the consensus step is pluggable via **`consensus_method`**: **`kmeans`** (default,
  silhouette k-means → `pharmacophores/`) or **`density`** (Gaussian occupancy field →
  peaks, written to the side-by-side **`pharmacophores_density/`** namespace). Both share
  one in/out contract `(family, position, tolerance, optional direction)`;
- features use RDKit's **`LumpedHydrophobe`** (one centroid per hydrophobic group) so
  hydrophobes don't swamp the model;
- a cell with **fewer than 3 ligands is skipped** (no output written/kept) — too few
  for an ensemble hypothesis;
- (k-means) overlapping clusters are **merged, keeping the dominant one** — both within a
  family and **across families** (a donor and an acceptor cannot share one spot), with a
  geometric threshold (one centre inside the other's sphere);
- (density) the unit of evidence is the **distinct molecule** (per-point weighting),
  features emerge from field peaks with **no `k`**, the **same cross-family merge** then
  gives one feature per region, and **excluded-volume** spheres mark receptor regions no
  ligand occupies; deterministic, two knobs only;
- ligands are **protonated to their pH-7.4 microstate** (pkasolver + a config-driven
  **weak-acid guard** that corrects pkasolver's over-deprotonation of phenols/alcohols/
  amides/sulfonamides/amino-heteroaromatics) before perception, so donor/acceptor/
  ±ionizable features reflect the real ionisation (`protonated_ligands.csv`; see
  [`pharmacophore_method.md`](pharmacophore_method.md) §2.1);
- the visualisation uses a **real representative ligand** from the cell (clean SDF),
  not the heavy-atom raw poses;
- family colours: HBD/Donor **pink**, HBA/Acceptor **green**, hydrophobic **cyan**,
  Aromatic **yellow**, PosIonizable **red**, NegIonizable orange, ExcludedVolume grey.

Files per model:

| File | What it is |
|---|---|
| `pharmacophore.json` | Canonical, schema-versioned model (`pharmpipe.pharmacophore/v1`): each feature's family, centre, tolerance radius, point count, ligand support, plus a provenance block (incl. the representative ligand). Format is method-stable — swapping the clustering method changes positions, not structure. |
| `features.csv` | Every raw extracted feature point (family, source ligand, x/y/z, cluster id, kept flag) — the data behind the model. |
| `representative_ligand.sdf` | One real cell ligand (correct bond orders + 3D coords) chosen as the best fit to the model; the clean visual scaffold. |
| `raw_features_<family>.png` | Per-family 3D scatter of the raw points, coloured by cluster; centre-marker area scales with cluster population, kept centres a filled "X". |
| `pharmacophore.pml` | Lightweight PyMOL script (representative ligand + feature spheres). The richer `scripts/pymol_pharmacophore.py` reads the JSON and adds a raw-point overlay. |
| `model_summary.md` | Human-readable summary: load coverage, representative ligand, and one row **per feature (peak)** — its `<Family> <n>` label, point/ligand counts, and support (fraction of the cell's ligands contributing). |

## Other tracked files

- `ligand_catalogue.md` / `ligand_catalogue.xlsx` — Stage 1 cross-target ligand catalogue.
- `run_summary.md` — per-stage run record (counts per target, all 18 site-slugs).
- `realignment_report.md` — Stage 2 binding-site alignment method + before/after QC.
- `pharmacophore_method.md` — Stage 4 pharmacophore-construction method (feature
  families, clustering, selection, overlap merging, tolerance, visualisation).
- `stage3_efficacy_resolved.csv` — ChEMBL efficacy resolution (the fallback tier; read by the Stage-3 loader).
- `curation/` — Stage 3.4 literature efficacy provenance: `efficacy_curation_README.md`
  (start here), `literature_curation_traceability.csv` (batch 1, 158 ligands), the
  batch-2 `efficacy_batch2_{traceability.csv,notes.md}`, and the batch-3
  `efficacy_batch3_{traceability.csv,notes.md}` (drd1). Per-ligand efficacy direction,
  site/pose-source qualifiers, and PMID provenance.
