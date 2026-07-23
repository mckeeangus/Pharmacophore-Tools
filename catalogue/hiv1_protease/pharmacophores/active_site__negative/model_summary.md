# Pharmacophore — hiv1_protease/active_site__negative

- Ligands loaded: **32** (direct=3, template=29)
- Skipped poses: 0
- Consensus method: `density`
- Representative ligand (viz): `1BWB_146_B641`
- Features kept: **9**
- Excluded-volume spheres (receptor markers): **40**

**Support** = fraction of the cell's ligands that contribute to a feature (≤ 1.0; features are kept only above the 0.5 support floor). **Occupancy** = points ÷ contributing ligands (points-per-ligand, uncapped: > 1.0 when a cluster is denser than one point per ligand). One row per feature / peak.

| Feature | Points | Ligands | Support | Occupancy |
|---|---:|---:|---:|---:|
| Acceptor 1 | 27 | 27 | 0.84 | 1.00 |
| Acceptor 2 | 22 | 22 | 0.69 | 1.00 |
| Aromatic 1 | 20 | 20 | 0.62 | 1.00 |
| Aromatic 2 | 17 | 17 | 0.53 | 1.00 |
| Donor 1 | 26 | 26 | 0.81 | 1.00 |
| LumpedHydrophobe 1 | 21 | 21 | 0.66 | 1.00 |
| LumpedHydrophobe 2 | 20 | 20 | 0.62 | 1.00 |
| LumpedHydrophobe 3 | 20 | 20 | 0.62 | 1.00 |
| LumpedHydrophobe 4 | 16 | 16 | 0.50 | 1.00 |

## Feature resolution

Co-incident dual classifications collapsed by the feature hierarchy (higher-priority family kept on the shared atom); the listed ligands each carried both types on one atom.

| Kept ← dropped | Events | Ligands |
|---|---:|---|
| NegIonizable ← Acceptor | 2 | 2WHH_GLU_A2302 |
| PosIonizable ← Donor | 27 | 1BWB_146_B641, 1HVH_Q82_B265, 1HVR_XK2_A263, 1ODX_0E8_A201, 1QBR_XV6_A638, 2FDE_385_A101, 2WHH_GLU_A2302, 4Q1Y_017_A106, 4Q5M_ROC_A1101, 4U7V_3EN_B101, 5DGU_5B7_A201, 5DGW_5B5_A201, 5KAO_G43_A500, 6DJ1_AB1_B201, 6DJ5_G52_B201, 6DJ7_G10_B201, 6DV0_GA8_B201, 6DV4_GA5_B201, 6E9A_J0S_B201, 7DOZ_1UN_A1102, 8ESX_X7B_B203 |
| PosIonizable ← LumpedHydrophobe | 2 | 1BWB_146_B641 |

## Below the support/size floor

Clusters that formed but never became candidates — below the 0.5 support floor or the minimum cluster size.

| Feature | Points | Ligands | Support | Occupancy |
|---|---:|---:|---:|---:|
| Aromatic | 15 | 15 | 0.47 | 1.00 |
| Acceptor | 15 | 14 | 0.44 | 1.07 |
| Aromatic | 14 | 14 | 0.44 | 1.00 |
| Acceptor | 15 | 10 | 0.31 | 1.50 |
| Donor | 8 | 8 | 0.25 | 1.00 |
| Donor | 7 | 7 | 0.22 | 1.00 |
| PosIonizable | 6 | 6 | 0.19 | 1.00 |
| PosIonizable | 6 | 6 | 0.19 | 1.00 |
| Acceptor | 2 | 2 | 0.06 | 1.00 |
| LumpedHydrophobe | 1 | 1 | 0.03 | 1.00 |
| PosIonizable | 1 | 1 | 0.03 | 1.00 |
| PosIonizable | 1 | 1 | 0.03 | 1.00 |
| NegIonizable | 1 | 1 | 0.03 | 1.00 |

See `pharmacophore.json` (model), `features.csv` (raw points + cluster ids), and `raw_features_*.png` (per-family point distributions, each kept peak annotated with its label and support).