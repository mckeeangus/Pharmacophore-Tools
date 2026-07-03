# Pharmacophore — hiv1_protease/active_site__negative

- Ligands loaded: **32** (direct=3, template=29)
- Skipped poses: 0
- Consensus method: `density`
- Representative ligand (viz): `1BWB_146_B641`
- Features kept: **6**
- Excluded-volume spheres (receptor markers): **40**

Support is the fraction of the cell's ligands that contribute to a feature (one row per feature / peak; all features are kept only above the support floor).

| Feature | Points | Ligands | Support |
|---|---:|---:|---:|
| Acceptor 1 | 69 | 30 | 0.94 |
| Acceptor 2 | 56 | 24 | 0.75 |
| Acceptor 3 | 32 | 23 | 0.72 |
| Aromatic 1 | 28 | 23 | 0.72 |
| Aromatic 2 | 26 | 23 | 0.72 |
| Donor 1 | 70 | 28 | 0.88 |

## Feature resolution

Co-incident dual classifications collapsed by the feature hierarchy (higher-priority family kept on the shared atom); the listed ligands each carried both types on one atom.

| Kept ← dropped | Events | Ligands |
|---|---:|---|
| Aromatic ← LumpedHydrophobe | 83 | 1BVE_DMP_B100, 1BWB_146_B641, 1DMP_DMQ_B450, 1HIV_1ZK_A100, 1HVH_Q82_B265, 1HVR_XK2_A263, 1HWR_216_B216, 1ODX_0E8_A201, 1ODY_LP1_A201, 1QBR_XV6_A638, 1QBU_846_B300, 2FDE_385_A101, 2WHH_PPN_A2301, 4Q1Y_017_A106, 4Q5M_ROC_A1101, 4U7Q_3EM_B101, 4U7V_3EN_B101, 5DGU_5B7_A201, 5DGW_5B5_A201, 5KAO_G43_A500, 6DIF_TPV_B201, 6DJ1_AB1_B201, 6DJ5_G52_B201, 6DJ7_G10_B201, 6DV0_GA8_B201, 6DV4_GA5_B201, 6E7J_HWY_A201, 6E9A_J0S_B201, 7DOZ_1UN_A1102, 8ESX_X7B_B203, 8F0F_X7H_B201 |
| NegIonizable ← Acceptor | 2 | 2WHH_GLU_A2302 |
| PosIonizable ← Donor | 27 | 1BWB_146_B641, 1HVH_Q82_B265, 1HVR_XK2_A263, 1ODX_0E8_A201, 1QBR_XV6_A638, 2FDE_385_A101, 2WHH_GLU_A2302, 4Q1Y_017_A106, 4Q5M_ROC_A1101, 4U7V_3EN_B101, 5DGU_5B7_A201, 5DGW_5B5_A201, 5KAO_G43_A500, 6DJ1_AB1_B201, 6DJ5_G52_B201, 6DJ7_G10_B201, 6DV0_GA8_B201, 6DV4_GA5_B201, 6E9A_J0S_B201, 7DOZ_1UN_A1102, 8ESX_X7B_B203 |
| PosIonizable ← LumpedHydrophobe | 2 | 1BWB_146_B641 |

## Not selected

Clusters/peaks that formed but did not enter the model — below the support or size floor, or displaced by the cross-family overlap merge — with their mean support (fraction of the cell's ligands contributing).

| Feature | Points | Ligands | Mean support |
|---|---:|---:|---:|
| Acceptor | 39 | 28 | 0.88 |
| Aromatic | 22 | 18 | 0.56 |
| Aromatic | 22 | 17 | 0.53 |
| Donor | 18 | 15 | 0.47 |
| Donor | 19 | 14 | 0.44 |
| PosIonizable | 12 | 12 | 0.38 |
| PosIonizable | 10 | 9 | 0.28 |
| LumpedHydrophobe | 9 | 9 | 0.28 |
| LumpedHydrophobe | 8 | 8 | 0.25 |
| LumpedHydrophobe | 5 | 5 | 0.16 |
| Acceptor | 6 | 4 | 0.12 |
| LumpedHydrophobe | 4 | 4 | 0.12 |
| PosIonizable | 2 | 2 | 0.06 |
| LumpedHydrophobe | 2 | 2 | 0.06 |
| NegIonizable | 2 | 1 | 0.03 |
| PosIonizable | 1 | 1 | 0.03 |
| LumpedHydrophobe | 1 | 1 | 0.03 |

See `pharmacophore.json` (model), `features.csv` (raw points + cluster ids), and `raw_features_*.png` (per-family point distributions, each kept peak annotated with its label and support).