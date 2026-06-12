# Run summary — 2026-06-12

Two-stage pipeline. **Stage 1** scrapes every ligand-bound PDB structure mapped to each verified UniProt accession and curates the bound ligands (drop additives/buffers/cryo/waters; keep cofactors; flag metals). **Stage 2** keeps only ligands bound at the *relevant site* of each model system, superposes their poses into one reference frame (binding-site-local fit), and writes a PyMOL session for comparison.

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

## Stage 2 — site filtering & alignment

Poses per session capped at **100** (best-resolution first). Symmetry-equivalent copies of a ligand within a structure are collapsed to one representative pose. `off-site` = correct location test failed (wrong site/cofactor/lipid); `other` = no matching pocket / unavailable (`poor_fit`, `no_pocket`, `not_found`, `align_error`).

| Target | Ref | Anchor | Structs (proc/total) | Poses in .pse | At-site | Off-site | Other | Capped |
|--------|-----|--------|---------------------|--------------:|--------:|---------:|------:|:------:|
| nachr_a4b2 | 8ST4 | ACH | 138/138 | 95 | 489 | 494 | 0 | — |
| esr1 | 7NEL | EST | 214/468 | 100 | 237 | 131 | 0 | yes |
| hiv1_protease | 1DMP | DMQ | 199/199 | 48 | 51 | 156 | 16 | — |
| adrb2 | 2RH1 | CAU | 103/137 | 100 | 102 | 39 | 12 | yes |
| cdk2 | 4EOJ | ATP | 106/478 | 100 | 106 | 24 | 0 | yes |
| ca2 | 3K34 | ZN | 121/1000 | 100 | 102 | 150 | 0 | yes |
| ache | 6O4W | E20 | 67/67 | 84 | 164 | 3 | 0 | — |
| cavab | 6KE5 | 6UB | 13/13 | 6 | 6 | 24 | 0 | — |
| cox2 | 5KIR | RCX | 7/7 | 6 | 12 | 24 | 0 | — |
| hmgcr | 1HWK | 117 | 23/23 | 22 | 85 | 40 | 0 | — |
| gaba_a | 9EQG | ABU | 102/102 | 97 | 198 | 171 | 0 | — |
| net_slc6a2 | 8ZOY | LNR | 54/54 | 50 | 57 | 42 | 0 | — |

Per-target detail: `catalogue/<slug>/site_filter.csv` (every instance, its status, distance-to-anchor and pocket RMSD) and the session `catalogue/<slug>/<slug>_aligned.pse`.
