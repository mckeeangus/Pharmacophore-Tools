# Pharmacophore — hmgcr/hmg_site__negative

- Ligands loaded: **18** (template=18)
- Skipped poses: 0
- Consensus method: `kmeans`
- Representative ligand (viz): `3CCZ_5HI_B876`
- Features kept: **10**

Support is the fraction of the cell's ligands that contribute to a feature (one row per feature / peak; all features are kept only above the support floor).

| Feature | Points | Ligands | Support |
|---|---:|---:|---:|
| Acceptor 1 | 17 | 14 | 0.78 |
| Acceptor 2 | 15 | 15 | 0.83 |
| Aromatic 1 | 18 | 16 | 0.89 |
| Aromatic 2 | 15 | 15 | 0.83 |
| Aromatic 3 | 12 | 11 | 0.61 |
| Donor 1 | 18 | 18 | 1.00 |
| Donor 2 | 18 | 18 | 1.00 |
| Donor 3 | 14 | 10 | 0.56 |
| LumpedHydrophobe 1 | 15 | 15 | 0.83 |
| NegIonizable 1 | 11 | 11 | 0.61 |

## Feature resolution

Co-incident dual classifications collapsed by the feature hierarchy (higher-priority family kept on the shared atom); the listed ligands each carried both types on one atom.

| Kept ← dropped | Events | Ligands |
|---|---:|---|
| Aromatic ← LumpedHydrophobe | 36 | 1HWI_115_A2, 1HWJ_116_A2, 1HWK_117_A2, 1HWL_FBI_A2, 2Q1L_882_A877, 2Q6B_HR2_A3001, 2Q6C_HR1_A3002, 2R4F_RIE_B876, 3BGL_RID_A2, 3CCT_3HI_D3, 3CCW_4HI_C4, 3CCZ_5HI_B876, 3CD0_6HI_D3, 3CD5_7HI_B1, 3CDA_8HI_B1, 3CDB_9HI_D3 |
| NegIonizable ← Acceptor | 18 | 1HW8_114_A2, 1HW9_SIM_C2, 1HWI_115_A2, 1HWJ_116_A2, 1HWK_117_A2, 1HWL_FBI_A2, 2Q1L_882_A877, 2Q6B_HR2_A3001, 2Q6C_HR1_A3002, 2R4F_RIE_B876, 3BGL_RID_A2, 3CCT_3HI_D3, 3CCW_4HI_C4, 3CCZ_5HI_B876, 3CD0_6HI_D3, 3CD5_7HI_B1, 3CDA_8HI_B1, 3CDB_9HI_D3 |

See `pharmacophore.json` (model), `features.csv` (raw points + cluster ids), and `raw_features_*.png` (per-family point distributions, each kept peak annotated with its label and support).