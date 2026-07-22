# Pharmacophore — hiv1_protease/active_site__negative

- Ligands loaded: **32** (direct=3, template=29)
- Skipped poses: 0
- Consensus method: `density`
- Representative ligand (viz): `1BWB_146_B641`
- Features kept: **4**
- Excluded-volume spheres (receptor markers): **40**

**Support** = fraction of the cell's ligands that contribute to a feature (≤ 1.0; features are kept only above the 0.5 support floor). **Occupancy** = points ÷ contributing ligands (points-per-ligand, uncapped: > 1.0 when a cluster is denser than one point per ligand). One row per feature / peak.

| Feature | Points | Ligands | Support | Occupancy |
|---|---:|---:|---:|---:|
| Acceptor 1 | 31 | 27 | 0.84 | 1.15 |
| Acceptor 2 | 17 | 16 | 0.50 | 1.06 |
| Aromatic 1 | 19 | 19 | 0.59 | 1.00 |
| Aromatic 2 | 17 | 17 | 0.53 | 1.00 |

## Feature resolution

Co-incident dual classifications collapsed by the feature hierarchy (higher-priority family kept on the shared atom); the listed ligands each carried both types on one atom.

| Kept ← dropped | Events | Ligands |
|---|---:|---|
| Aromatic ← LumpedHydrophobe | 83 | 1BVE_DMP_B100, 1BWB_146_B641, 1DMP_DMQ_B450, 1HIV_1ZK_A100, 1HVH_Q82_B265, 1HVR_XK2_A263, 1HWR_216_B216, 1ODX_0E8_A201, 1ODY_LP1_A201, 1QBR_XV6_A638, 1QBU_846_B300, 2FDE_385_A101, 2WHH_PPN_A2301, 4Q1Y_017_A106, 4Q5M_ROC_A1101, 4U7Q_3EM_B101, 4U7V_3EN_B101, 5DGU_5B7_A201, 5DGW_5B5_A201, 5KAO_G43_A500, 6DIF_TPV_B201, 6DJ1_AB1_B201, 6DJ5_G52_B201, 6DJ7_G10_B201, 6DV0_GA8_B201, 6DV4_GA5_B201, 6E7J_HWY_A201, 6E9A_J0S_B201, 7DOZ_1UN_A1102, 8ESX_X7B_B203, 8F0F_X7H_B201 |
| NegIonizable ← Acceptor | 2 | 2WHH_GLU_A2302 |
| PosIonizable ← Donor | 27 | 1BWB_146_B641, 1HVH_Q82_B265, 1HVR_XK2_A263, 1ODX_0E8_A201, 1QBR_XV6_A638, 2FDE_385_A101, 2WHH_GLU_A2302, 4Q1Y_017_A106, 4Q5M_ROC_A1101, 4U7V_3EN_B101, 5DGU_5B7_A201, 5DGW_5B5_A201, 5KAO_G43_A500, 6DJ1_AB1_B201, 6DJ5_G52_B201, 6DJ7_G10_B201, 6DV0_GA8_B201, 6DV4_GA5_B201, 6E9A_J0S_B201, 7DOZ_1UN_A1102, 8ESX_X7B_B203 |
| PosIonizable ← LumpedHydrophobe | 2 | 1BWB_146_B641 |

## Merged away

Clusters that passed the support/size floor but were displaced by the 1 Å cross-family overlap merge — one feature per region, keeping the denser one. Each row states in favour of which kept feature it was removed.

| Feature | Points | Ligands | Support | Occupancy | In favour of |
|---|---:|---:|---:|---:|---|
| Donor | 21 | 21 | 0.66 | 1.00 | Acceptor 1 |

## Below the support/size floor

Clusters that formed but never became candidates — below the 0.5 support floor or the minimum cluster size.

| Feature | Points | Ligands | Support | Occupancy |
|---|---:|---:|---:|---:|
| Aromatic | 13 | 12 | 0.38 | 1.08 |
| Aromatic | 12 | 12 | 0.38 | 1.00 |
| Acceptor | 11 | 10 | 0.31 | 1.10 |
| Donor | 8 | 8 | 0.25 | 1.00 |
| LumpedHydrophobe | 8 | 8 | 0.25 | 1.00 |
| LumpedHydrophobe | 8 | 8 | 0.25 | 1.00 |
| Acceptor | 7 | 7 | 0.22 | 1.00 |
| PosIonizable | 6 | 6 | 0.19 | 1.00 |
| PosIonizable | 6 | 6 | 0.19 | 1.00 |
| LumpedHydrophobe | 5 | 5 | 0.16 | 1.00 |
| LumpedHydrophobe | 4 | 4 | 0.12 | 1.00 |
| Donor | 2 | 2 | 0.06 | 1.00 |
| Acceptor | 2 | 2 | 0.06 | 1.00 |
| LumpedHydrophobe | 2 | 2 | 0.06 | 1.00 |
| PosIonizable | 1 | 1 | 0.03 | 1.00 |
| PosIonizable | 1 | 1 | 0.03 | 1.00 |
| LumpedHydrophobe | 1 | 1 | 0.03 | 1.00 |
| NegIonizable | 1 | 1 | 0.03 | 1.00 |

See `pharmacophore.json` (model), `features.csv` (raw points + cluster ids), and `raw_features_*.png` (per-family point distributions, each kept peak annotated with its label and support).