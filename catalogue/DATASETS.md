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

## Cells — `groups/<pocket>__<efficacy>/`

A cell is the unit a single pharmacophore hypothesis is built from: a geometry-verified
pocket crossed with a curated efficacy sign. Pockets are named in `config/pockets.yaml`;
efficacy signs come from `config/efficacy.yaml` (provenance: literature > prelabelled >
curated > ChEMBL-CSV fallback). Cells present across the 17 site-slugs (16 biological
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

## Other tracked files

- `ligand_catalogue.md` / `ligand_catalogue.xlsx` — Stage 1 cross-target ligand catalogue.
- `run_summary.md` — per-stage run record (counts per target, all 17 site-slugs).
- `realignment_report.md` — Stage 2 binding-site alignment method + before/after QC.
- `stage3_efficacy_resolved.csv` — ChEMBL efficacy resolution (the fallback tier; read by the Stage-3 loader).
- `curation/` — Stage 3.4 literature efficacy provenance: `efficacy_curation_README.md`
  (start here), `literature_curation_traceability.csv` (batch 1, 158 ligands) and the
  batch-2 `efficacy_batch2_{traceability.csv,notes.md}`. Per-ligand efficacy direction,
  site/pose-source qualifiers, and PMID provenance.
