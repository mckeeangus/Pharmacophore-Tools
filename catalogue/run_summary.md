# Run summary — 2026-06-23

Two-stage pipeline. **Stage 1** scrapes every ligand-bound PDB structure mapped to each verified UniProt accession and curates the bound ligands (drop additives/buffers/cryo/waters; keep cofactors; flag metals). **Stage 2** keeps only ligands bound at the *relevant site* of each model system, superposes their poses into one reference frame (binding-site-local fit), and writes a PyMOL session for comparison.

## Stage 1 — scrape & curate

| Target | Primary acc | Structures | Uniq kept | Excl HET | Flagged |
|--------|-------------|-----------:|----------:|---------:|--------:|
| Dopamine receptor D1 | P21728 | 31 | 21 | 3 | 1 |

## Stage 2 — site filtering & alignment

Poses per session capped at **100** (best-resolution first). Symmetry-equivalent copies of a ligand within a structure are collapsed to one representative pose. `off-site` = correct location test failed (wrong site/cofactor/lipid); `other` = no matching pocket / unavailable (`poor_fit`, `no_pocket`, `not_found`, `align_error`).

| Target | Ref | Anchor | Structs (proc/total) | Poses in .pse | At-site | Off-site | Other | Capped |
|--------|-----|--------|---------------------|--------------:|--------:|---------:|------:|:------:|
| drd1 | 9LLJ | LDP | 31/31 | 35 | 35 | 5 | 0 | — |

Per-target detail: `catalogue/<slug>/site_filter.csv` (every instance, its status, distance-to-anchor and pocket RMSD) and the session `catalogue/<slug>/<slug>_aligned.pse`.

## Stage 3 — effect-based grouping (pocket-verified)

_Stage 3 run 2026-06-23._ Each pose is assigned a **geometry-verified pocket** (native contact fingerprints, not the coarse Stage-2 distance) and an **efficacy sign** from curated external pharmacology (`config/efficacy.yaml`). A cell = (pocket × efficacy). Covalent/reactivator/degrader/substrate ligands are routed to a separate-state track; unconfident efficacy and out-of-pocket poses are first-class review outputs, never force-bucketed. **Stage 3.3** folds in efficacy resolved from ChEMBL for previously-`unknown` ligands (`catalogue/stage3_efficacy_resolved.csv`, used only below curated config). Pseudo-symmetric multi-pocket targets (GABA-A) are re-aligned onto the reference at their true subunit interface so the benzodiazepine and orthosteric sites are spatially distinct in the session. Cell/grouped sessions show one representative pose per ligand.

| Target | Pockets found | Cells | In cells | Separate-state | Unknown eff. | Quarantined |
|--------|---------------|------:|---------:|---------------:|-------------:|------------:|
| drd1 | orthosteric | 2 | 31 | 4 | 0 | 0 |

Per-target detail: `catalogue/<slug>/<slug>_stage3_report.md`, the cell mol2 in `catalogue/<slug>/groups/`, `effect_groups.json`, and the recoloured session `catalogue/<slug>/<slug>_grouped.pse`.

**Pose datasets** (pharmacophore inputs): each target carries `catalogue/<slug>/datasets/{all_poses,representative}/` (every kept pose vs one per ligand), with a cross-target master under `catalogue/datasets/` (35 poses / 19 representative). Each set ships a `.pml` + baked `.pse`.
