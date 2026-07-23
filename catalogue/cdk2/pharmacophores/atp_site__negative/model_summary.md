# Pharmacophore — cdk2/atp_site__negative

- Ligands loaded: **87** (direct=4, template=83)
- Skipped poses: 5 (7SA0_8KQ_A305:fail, 8FP0_RRC_A303:fail, 9JJ5_A1EB0_A301:fail, 9UAU_A1EOM_A301:fail, 9UGF_A1EO5_A301:fail)
- Consensus method: `density`
- Representative ligand (viz): `1H00_FAP_A1300`
- Features kept: **4**
- Excluded-volume spheres (receptor markers): **40**

**Support** = fraction of the cell's ligands that contribute to a feature (≤ 1.0; features are kept only above the 0.5 support floor). **Occupancy** = points ÷ contributing ligands (points-per-ligand, uncapped: > 1.0 when a cluster is denser than one point per ligand). One row per feature / peak.

| Feature | Points | Ligands | Support | Occupancy |
|---|---:|---:|---:|---:|
| Acceptor 1 | 82 | 81 | 0.93 | 1.01 |
| Aromatic 1 | 78 | 65 | 0.75 | 1.20 |
| Aromatic 2 | 45 | 45 | 0.52 | 1.00 |
| Donor 1 | 65 | 65 | 0.75 | 1.00 |

## Feature resolution

Co-incident dual classifications collapsed by the feature hierarchy (higher-priority family kept on the shared atom); the listed ligands each carried both types on one atom.

| Kept ← dropped | Events | Ligands |
|---|---:|---|
| NegIonizable ← Acceptor | 10 | 4FKG_4CK_A300, 4FKU_60K_A303, 6Q4D_HHT_A301, 6Q4G_HJK_A301, 6Q4H_HGH_A301, 6Q4I_HGK_A302, 6Q4J_HHB_A303, 7M2F_YOS_A901, 7RWE_7TH_A301 |
| PosIonizable ← Donor | 41 | 1GZ8_MBP_A1300, 1H00_FAP_A1300, 1H00_FCP_A1400, 1URW_I1P_A1300, 2VTT_LZD_A1299, 3PY0_SU9_A301, 3R73_X87_A920, 3RAI_X85_A923, 3RM6_18Z_A478, 4ACM_7YG_A1302, 4FKJ_11K_A301, 4FKP_LS5_A301, 4FKT_48K_A301, 4FKV_61K_A301, 5ANE_SZL_A1299, 5ANJ_ZXC_A1299, 5IEY_6AE_A1001, 6GUK_FC8_A301, 6Q4E_HH5_A303, 6Q4G_HJK_A301, 6Q4H_HGH_A301, 7M2F_YOS_A901, 7QHL_D5P_C301, 7RA5_3I3_A301, 7VDU_65L_A301, 8ERN_WQK_A402, 8RU8_I74_A301, 9UAW_A1EOO_A301 |

## Below the support/size floor

Clusters that formed but never became candidates — below the 0.5 support floor or the minimum cluster size.

| Feature | Points | Ligands | Support | Occupancy |
|---|---:|---:|---:|---:|
| LumpedHydrophobe | 26 | 26 | 0.30 | 1.00 |
| LumpedHydrophobe | 25 | 24 | 0.28 | 1.04 |
| Acceptor | 18 | 18 | 0.21 | 1.00 |
| LumpedHydrophobe | 16 | 16 | 0.18 | 1.00 |
| Donor | 11 | 11 | 0.13 | 1.00 |
| PosIonizable | 7 | 7 | 0.08 | 1.00 |
| PosIonizable | 4 | 4 | 0.05 | 1.00 |
| NegIonizable | 4 | 4 | 0.05 | 1.00 |
| PosIonizable | 2 | 2 | 0.02 | 1.00 |
| PosIonizable | 2 | 2 | 0.02 | 1.00 |
| NegIonizable | 1 | 1 | 0.01 | 1.00 |
| NegIonizable | 1 | 1 | 0.01 | 1.00 |
| NegIonizable | 1 | 1 | 0.01 | 1.00 |

See `pharmacophore.json` (model), `features.csv` (raw points + cluster ids), and `raw_features_*.png` (per-family point distributions, each kept peak annotated with its label and support).