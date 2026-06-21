# Run summary — 2026-06-21

Two-stage pipeline. **Stage 1** scrapes every ligand-bound PDB structure mapped to each verified UniProt accession and curates the bound ligands (drop additives/buffers/cryo/waters; keep cofactors; flag metals). **Stage 2** keeps only ligands bound at the *relevant site* of each model system, superposes their poses into one reference frame (binding-site-local fit with iterative pocket-local ICP refinement), and writes a PyMOL session.

## Stage 1 — scrape & curate

| Target | Primary acc | Structures | Uniq kept | Excl HET | Flagged |
|--------|-------------|-----------:|----------:|---------:|--------:|
| Nicotinic acetylcholine receptor ( | P43681,P17787 | 169 | 111 | 24 | 5 |
| Estrogen receptor alpha | P03372 | 479 | 431 | 12 | 6 |
| HIV-1 protease | P04585 | 277 | 144 | 22 | 5 |
| Beta-2 adrenoceptor | P07550 | 145 | 43 | 17 | 2 |
| Cyclin-dependent kinase 2 (CDK2) | P24941 | 521 | 420 | 19 | 3 |
| Carbonic anhydrase II | P00918 | 1241 | 730 | 36 | 10 |
| Acetylcholinesterase | P22303 | 78 | 43 | 18 | 2 |
| CavAb (Ca2+-selective NavAb mutant | A8EVM5 | 77 | 16 | 13 | 3 |
| Cyclooxygenase-2 (PTGS2) | P35354 | 7 | 8 | 6 | 0 |
| HMG-CoA reductase | P04035 | 24 | 23 | 2 | 0 |
| GABA-A receptor | P14867,P47870,P28472,P18507 | 128 | 38 | 18 | 1 |
| Norepinephrine transporter (NET, S | P23975 | 61 | 42 | 12 | 0 |
| Nav1.7 sodium channel — VSD4 site | Q15858 | 43 | 28 | 11 | 0 |
| Nav1.7 sodium channel — pore site | Q15858 | 43 | 28 | 11 | 0 |
| Glucocorticoid receptor | P04150 | 57 | 30 | 11 | 2 |
| Adenosine A2A receptor | P29274 | 188 | 133 | 25 | 0 |
| Muscarinic acetylcholine receptor  | P08172 | 17 | 7 | 2 | 1 |

## Stage 2 — site filtering & alignment

Poses per session capped at **100** (best-resolution first), except adenosine A2A which was run uncapped (1000) to retain its lower-resolution agonist class. Symmetry-equivalent copies of a ligand within a structure are collapsed to one representative pose. `off-site` = correct location test failed (wrong site/cofactor/lipid); `other` = no matching pocket / unavailable (`poor_fit`, `no_pocket`, `not_found`, `align_error`).

| Target | Ref | Anchor | Structs (proc/total) | Poses in .pse | At-site | Off-site | Other | Capped |
|--------|-----|--------|---------------------|--------------:|--------:|---------:|------:|:------:|
| nachr_a4b2 | 8ST4 | ACH | 138/138 | 97 | 502 | 481 | 0 | — |
| esr1 | 7NEL | EST | 214/468 | 100 | 237 | 131 | 0 | yes |
| hiv1_protease | 1DMP | DMQ | 199/199 | 48 | 51 | 170 | 2 | — |
| adrb2 | 2RH1 | CAU | 103/137 | 100 | 102 | 42 | 9 | yes |
| cdk2 | 4EOJ | ATP | 106/478 | 100 | 106 | 23 | 0 | yes |
| ca2 | 3K34 | ZN | 121/1000 | 100 | 102 | 150 | 0 | yes |
| ache | 6O4W | E20 | 67/67 | 84 | 164 | 3 | 0 | — |
| cavab | 6KE5 | 6UB | 13/13 | 6 | 6 | 24 | 0 | — |
| cox2 | 5KIR | RCX | 7/7 | 6 | 12 | 24 | 0 | — |
| hmgcr | 1HWK | 117 | 23/23 | 22 | 85 | 40 | 0 | — |
| gaba_a | 9EQG | ABU | 102/102 | 97 | 198 | 171 | 0 | — |
| net_slc6a2 | 8ZOY | LNR | 54/54 | 50 | 57 | 42 | 0 | — |
| nav1_7_vsd4 | 8I5G | T70 | 35/43 | 5 | 8 | 83 | 0 | — |
| nav1_7_pore | 8I5B | OJ0 | 35/43 | 13 | 13 | 78 | 0 | — |
| gr_nr3c1 | 1M2Z | DEX | 35/57 | 33 | 56 | 14 | 0 | — |
| adora2a | 5NM4 | ZMA | 179/179 | 179 | 183 | 152 | 3 | — |
| chrm2 | 7T94 | ACH | 14/17 | 13 | 13 | 5 | 0 | — |

Per-target detail: `catalogue/<slug>/site_filter.csv` (every instance, its status, distance-to-anchor and pocket RMSD). The Stage-2 overlay is superseded by the Stage-3 `catalogue/<slug>/<slug>_grouped.pse` (same frame, recoloured by cell).

## Stage 3 — effect-based grouping (pocket-verified)

_Stage 3 run 2026-06-20._ Each pose is assigned a **geometry-verified pocket** (native contact fingerprints, not the coarse Stage-2 distance) and an **efficacy sign** from curated external pharmacology (`config/efficacy.yaml`). A cell = (pocket × efficacy). Covalent/reactivator/degrader/substrate ligands are routed to a separate-state track; unconfident efficacy and out-of-pocket poses are first-class review outputs, never force-bucketed. **Stage 3.3** folds in efficacy resolved from ChEMBL for previously-`unknown` ligands (`catalogue/stage3_efficacy_resolved.csv`, used only below curated config). Pseudo-symmetric multi-pocket targets (GABA-A) are re-aligned onto the reference at their true subunit interface so the benzodiazepine and orthosteric sites are spatially distinct in the session. Cell/grouped sessions show one representative pose per ligand.

| Target | Pockets found | Cells | In cells | Separate-state | Unknown eff. | Quarantined |
|--------|---------------|------:|---------:|---------------:|-------------:|------------:|
| nachr_a4b2 | accessory, orthosteric | 3 | 56 | 0 | 40 | 1 |
| esr1 | lbp | 2 | 70 | 17 | 13 | 0 |
| hiv1_protease | active_site | 1 | 48 | 0 | 0 | 0 |
| adrb2 | orthosteric | 3 | 92 | 2 | 3 | 3 |
| cdk2 | atp_site | 1 | 94 | 3 | 0 | 3 |
| ca2 | active_site | 1 | 87 | 12 | 0 | 1 |
| ache | gorge | 1 | 18 | 66 | 0 | 0 |
| cavab | dhp_site | 1 | 5 | 0 | 0 | 1 |
| cox2 | cox_channel | 1 | 5 | 0 | 0 | 1 |
| hmgcr | hmg_site | 1 | 19 | 3 | 0 | 0 |
| gaba_a | bzd_site, orthosteric | 4 | 93 | 0 | 3 | 1 |
| net_slc6a2 | central_s1 | 2 | 44 | 0 | 6 | 0 |
| nav1_7_vsd4 | vsd4_site | 1 | 3 | 0 | 0 | 2 |
| nav1_7_pore | pore_site | 1 | 13 | 0 | 0 | 0 |
| gr_nr3c1 | lbp | 2 | 32 | 0 | 0 | 1 |
| adora2a | orthosteric | 3 | 172 | 0 | 5 | 2 |
| chrm2 | orthosteric | 2 | 13 | 0 | 0 | 0 |

Per-target detail: `catalogue/<slug>/<slug>_stage3_report.md`, the cell mol2 in `catalogue/<slug>/groups/`, `effect_groups.json`, and the recoloured session `catalogue/<slug>/<slug>_grouped.pse`.

**Pose datasets** (pharmacophore inputs): each target carries `catalogue/<slug>/datasets/{all_poses,representative}/` (every kept pose vs one per ligand), with a cross-target master under `catalogue/datasets/` (808 poses / 500 representative). Each set ships a `.pml` + baked `.pse`.
