# DrugCLIP screening — pharmacophore evaluation vs known-actives + literature

Two methods per target: **docked** (full-docking consensus over all 1000 poses) and **seed_align** (minimum-docking, top-50 by DrugCLIP, seed_k=3). Verdicts: MATCH / PARTIAL / MISMATCH on feature-family recall + internal geometry (frame-independent). `vsKA` needs a built known-actives model; `vsLit` a literature entry.

| Target | Method | Feats | Ligands | vs Known | recall | geomD | vs Lit | recall |
|---|---|--:|--:|:--:|--:|--:|:--:|--:|
| esr1 | docked | 4 | 1000 | MATCH | 1.0 | 0.42 | MATCH | 1.0 |
| esr1 | seed_align | 6 | 50 | MATCH | 1.0 | 0.49 | MATCH | 1.0 |
| hiv1_protease | docked | 0 | 1000 | MISMATCH | 0.0 | - | MISMATCH | 0.0 |
| hiv1_protease | seed_align | 3 | 50 | PARTIAL | 0.75 | 1.99 | PARTIAL | 0.75 |
| cdk2 | docked | 0 | 1000 | MISMATCH | 0.0 | - | MISMATCH | 0.0 |
| cdk2 | seed_align | 2 | 50 | MISMATCH | 0.33 | - | PARTIAL | 0.5 |
| hmgcr | docked | 1 | 1000 | MISMATCH | 0.2 | - | - | - |
| hmgcr | seed_align | 8 | 50 | PARTIAL | 1.0 | 3.89 | - | - |
| nachr_a4b2_negative | docked | 0 | 1000 | - | - | - | MISMATCH | 0.0 |
| nachr_a4b2_negative | seed_align | 2 | 50 | - | - | - | MISMATCH | 0.33 |
| ca2 | docked | 0 | 1000 | MISMATCH | 0.0 | - | MISMATCH | 0.0 |
| ca2 | seed_align | 1 | 37 | MISMATCH | 0.25 | - | MISMATCH | 0.25 |
| ache | docked | 1 | 1000 | PARTIAL | 0.5 | - | - | - |
| ache | seed_align | 5 | 50 | PARTIAL | 1.0 | 4.99 | - | - |
| adrb2 | docked | 2 | 1000 | MISMATCH | 0.4 | 0.42 | MISMATCH | 0.4 |
| adrb2 | seed_align | 6 | 50 | PARTIAL | 0.8 | 1.55 | PARTIAL | 0.8 |
| cox2 | docked | 2 | 1000 | - | - | - | - | - |
| cox2 | seed_align | 6 | 50 | - | - | - | - | - |
| adora2a | docked | 1 | 1000 | PARTIAL | 0.5 | - | MISMATCH | 0.25 |
| adora2a | seed_align | 4 | 50 | PARTIAL | 0.5 | - | PARTIAL | 0.75 |
| nachr_a4b2_positive | docked | 1 | 1000 | MISMATCH | 0.33 | - | MISMATCH | 0.33 |
| nachr_a4b2_positive | seed_align | 3 | 43 | MATCH | 1.0 | 0.66 | MATCH | 1.0 |
| chrm2 | docked | 0 | 1000 | - | - | - | - | - |
| chrm2 | seed_align | 5 | 50 | - | - | - | - | - |
| gaba_a_bzd | docked | 0 | 1000 | - | - | - | MISMATCH | 0.0 |
| gaba_a_bzd | seed_align | 0 | 50 | - | - | - | MISMATCH | 0.0 |
| gaba_a_gaba | docked | 2 | 999 | - | - | - | MISMATCH | 0.25 |
| gaba_a_gaba | seed_align | 3 | 49 | - | - | - | PARTIAL | 0.5 |
| gr_nr3c1 | docked | 0 | 1000 | MISMATCH | 0.0 | - | MISMATCH | 0.0 |
| gr_nr3c1 | seed_align | 3 | 50 | PARTIAL | 0.67 | 1.87 | MISMATCH | 0.33 |
| nav1_7_pore | docked | 0 | 1000 | - | - | - | MISMATCH | 0.0 |
| nav1_7_pore | seed_align | 6 | 50 | - | - | - | PARTIAL | 0.75 |
| nav1_7_vsd4 | docked | 5 | 1000 | - | - | - | PARTIAL | 0.75 |
| nav1_7_vsd4 | seed_align | 7 | 50 | - | - | - | PARTIAL | 0.75 |
| drd1 | docked | 2 | 1000 | MISMATCH | 0.4 | 5.22 | MISMATCH | 0.4 |
| drd1 | seed_align | 4 | 50 | PARTIAL | 0.8 | 2.08 | PARTIAL | 0.8 |

## Per-target diagnosis

- **esr1** — families + geometry broadly consistent
- **hiv1_protease** — docked missing vs known: Acceptor, Aromatic, Donor, LumpedHydrophobe; seed_align missing vs known: Donor; seed_align geometry off known by 1.99 A mean
- **cdk2** — docked missing vs known: Acceptor, Aromatic, Donor; seed_align missing vs known: Acceptor, Donor
- **hmgcr** — full-docking over all poses diluted to 1 feature; seed-align (top slice) richer — dilution, not method failure; docked missing vs known: Acceptor, Aromatic, Donor, LumpedHydrophobe; seed_align geometry off known by 3.89 A mean
- **nachr_a4b2_negative** — families + geometry broadly consistent
- **ca2** — docked missing vs known: Acceptor, Aromatic, Donor, LumpedHydrophobe; seed_align missing vs known: Aromatic, Donor, LumpedHydrophobe
- **ache** — full-docking over all poses diluted to 1 feature; seed-align (top slice) richer — dilution, not method failure; docked missing vs known: LumpedHydrophobe; seed_align geometry off known by 4.99 A mean
- **adrb2** — docked missing vs known: Acceptor, Donor, PosIonizable; seed_align missing vs known: PosIonizable; seed_align geometry off known by 1.55 A mean
- **cox2** — families + geometry broadly consistent
- **adora2a** — full-docking over all poses diluted to 1 feature; seed-align (top slice) richer — dilution, not method failure; docked missing vs known: Donor; seed_align missing vs known: Donor
- **nachr_a4b2_positive** — full-docking over all poses diluted to 1 feature; seed-align (top slice) richer — dilution, not method failure; docked missing vs known: Acceptor, PosIonizable
- **chrm2** — families + geometry broadly consistent
- **gaba_a_bzd** — families + geometry broadly consistent
- **gaba_a_gaba** — families + geometry broadly consistent
- **gr_nr3c1** — docked missing vs known: Acceptor, Aromatic, LumpedHydrophobe; seed_align missing vs known: Acceptor; seed_align geometry off known by 1.87 A mean
- **nav1_7_pore** — families + geometry broadly consistent
- **nav1_7_vsd4** — families + geometry broadly consistent
- **drd1** — docked missing vs known: Acceptor, Donor, PosIonizable; docked geometry off known by 5.22 A mean; seed_align missing vs known: Donor; seed_align geometry off known by 2.08 A mean

See each `catalogue/screening_eval/<key>/{docked,seed_align}/` for the model + `model_summary.md`; `results.json` for the full comparison data.