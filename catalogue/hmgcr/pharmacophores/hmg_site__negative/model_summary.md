# Pharmacophore — hmgcr/hmg_site__negative

- Ligands loaded: **18** (template=18)
- Skipped poses: 0
- Consensus method: `density`
- Representative ligand (viz): `3CCZ_5HI_B876`
- Features kept: **9**
- Excluded-volume spheres (receptor markers): **40**

**Support** = fraction of the cell's ligands that contribute to a feature (≤ 1.0; features are kept only above the 0.5 support floor). **Occupancy** = points ÷ contributing ligands (points-per-ligand, uncapped: > 1.0 when a cluster is denser than one point per ligand). One row per feature / peak.

| Feature | Points | Ligands | Support | Occupancy |
|---|---:|---:|---:|---:|
| Acceptor 1 | 15 | 15 | 0.83 | 1.00 |
| Aromatic 1 | 16 | 16 | 0.89 | 1.00 |
| Aromatic 2 | 15 | 15 | 0.83 | 1.00 |
| Aromatic 3 | 10 | 10 | 0.56 | 1.00 |
| Donor 1 | 18 | 18 | 1.00 | 1.00 |
| Donor 2 | 18 | 18 | 1.00 | 1.00 |
| Donor 3 | 10 | 10 | 0.56 | 1.00 |
| LumpedHydrophobe 1 | 15 | 15 | 0.83 | 1.00 |
| NegIonizable 1 | 18 | 18 | 1.00 | 1.00 |

## Feature resolution

Co-incident dual classifications collapsed by the feature hierarchy (higher-priority family kept on the shared atom); the listed ligands each carried both types on one atom.

| Kept ← dropped | Events | Ligands |
|---|---:|---|
| Aromatic ← LumpedHydrophobe | 36 | 1HWI_115_A2, 1HWJ_116_A2, 1HWK_117_A2, 1HWL_FBI_A2, 2Q1L_882_A877, 2Q6B_HR2_A3001, 2Q6C_HR1_A3002, 2R4F_RIE_B876, 3BGL_RID_A2, 3CCT_3HI_D3, 3CCW_4HI_C4, 3CCZ_5HI_B876, 3CD0_6HI_D3, 3CD5_7HI_B1, 3CDA_8HI_B1, 3CDB_9HI_D3 |
| NegIonizable ← Acceptor | 18 | 1HW8_114_A2, 1HW9_SIM_C2, 1HWI_115_A2, 1HWJ_116_A2, 1HWK_117_A2, 1HWL_FBI_A2, 2Q1L_882_A877, 2Q6B_HR2_A3001, 2Q6C_HR1_A3002, 2R4F_RIE_B876, 3BGL_RID_A2, 3CCT_3HI_D3, 3CCW_4HI_C4, 3CCZ_5HI_B876, 3CD0_6HI_D3, 3CD5_7HI_B1, 3CDA_8HI_B1, 3CDB_9HI_D3 |

## Merged away

Clusters that passed the support/size floor but were displaced by the 1 Å cross-family overlap merge — one feature per region, keeping the denser one. Each row states in favour of which kept feature it was removed.

| Feature | Points | Ligands | Support | Occupancy | In favour of |
|---|---:|---:|---:|---:|---|
| Acceptor | 18 | 18 | 1.00 | 1.00 | Donor 1 |
| Acceptor | 18 | 18 | 1.00 | 1.00 | Donor 2 |

## Below the support/size floor

Clusters that formed but never became candidates — below the 0.5 support floor or the minimum cluster size.

| Feature | Points | Ligands | Support | Occupancy |
|---|---:|---:|---:|---:|
| Acceptor | 8 | 7 | 0.39 | 1.14 |
| PosIonizable | 3 | 3 | 0.17 | 1.00 |
| Acceptor | 2 | 2 | 0.11 | 1.00 |
| Donor | 1 | 1 | 0.06 | 1.00 |
| Donor | 1 | 1 | 0.06 | 1.00 |
| Acceptor | 0 | 0 | 0.00 | 0.00 |

See `pharmacophore.json` (model), `features.csv` (raw points + cluster ids), and `raw_features_*.png` (per-family point distributions, each kept peak annotated with its label and support).