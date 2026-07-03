# Pharmacophore — hiv1_protease/active_site__negative

- Ligands loaded: **32** (direct=3, template=29)
- Skipped poses: 0
- Consensus method: `kmeans`
- Representative ligand (viz): `6DV4_GA5_B201`
- Features kept: **9**

Support is the fraction of the cell's ligands that contribute to a feature (one row per feature / peak; all features are kept only above the support floor).

| Feature | Points | Ligands | Support |
|---|---:|---:|---:|
| Acceptor 1 | 47 | 23 | 0.72 |
| Acceptor 2 | 44 | 30 | 0.94 |
| Acceptor 3 | 35 | 21 | 0.66 |
| Acceptor 4 | 29 | 23 | 0.72 |
| Aromatic 1 | 21 | 21 | 0.66 |
| Aromatic 2 | 21 | 21 | 0.66 |
| Aromatic 3 | 18 | 17 | 0.53 |
| Aromatic 4 | 18 | 17 | 0.53 |
| Donor 1 | 72 | 28 | 0.88 |

## Feature resolution

Co-incident dual classifications collapsed by the feature hierarchy (higher-priority family kept on the shared atom); the listed ligands each carried both types on one atom.

| Kept ← dropped | Events | Ligands |
|---|---:|---|
| Aromatic ← LumpedHydrophobe | 83 | 1BVE_DMP_B100, 1BWB_146_B641, 1DMP_DMQ_B450, 1HIV_1ZK_A100, 1HVH_Q82_B265, 1HVR_XK2_A263, 1HWR_216_B216, 1ODX_0E8_A201, 1ODY_LP1_A201, 1QBR_XV6_A638, 1QBU_846_B300, 2FDE_385_A101, 2WHH_PPN_A2301, 4Q1Y_017_A106, 4Q5M_ROC_A1101, 4U7Q_3EM_B101, 4U7V_3EN_B101, 5DGU_5B7_A201, 5DGW_5B5_A201, 5KAO_G43_A500, 6DIF_TPV_B201, 6DJ1_AB1_B201, 6DJ5_G52_B201, 6DJ7_G10_B201, 6DV0_GA8_B201, 6DV4_GA5_B201, 6E7J_HWY_A201, 6E9A_J0S_B201, 7DOZ_1UN_A1102, 8ESX_X7B_B203, 8F0F_X7H_B201 |
| NegIonizable ← Acceptor | 2 | 2WHH_GLU_A2302 |
| PosIonizable ← Donor | 27 | 1BWB_146_B641, 1HVH_Q82_B265, 1HVR_XK2_A263, 1ODX_0E8_A201, 1QBR_XV6_A638, 2FDE_385_A101, 2WHH_GLU_A2302, 4Q1Y_017_A106, 4Q5M_ROC_A1101, 4U7V_3EN_B101, 5DGU_5B7_A201, 5DGW_5B5_A201, 5KAO_G43_A500, 6DJ1_AB1_B201, 6DJ5_G52_B201, 6DJ7_G10_B201, 6DV0_GA8_B201, 6DV4_GA5_B201, 6E9A_J0S_B201, 7DOZ_1UN_A1102, 8ESX_X7B_B203 |
| PosIonizable ← LumpedHydrophobe | 2 | 1BWB_146_B641 |

See `pharmacophore.json` (model), `features.csv` (raw points + cluster ids), and `raw_features_*.png` (per-family point distributions, each kept peak annotated with its label and support).