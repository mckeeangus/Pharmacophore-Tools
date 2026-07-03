# Pharmacophore — cdk2/atp_site__negative

- Ligands loaded: **87** (direct=4, template=83)
- Skipped poses: 5 (7SA0_8KQ_A305:fail, 8FP0_RRC_A303:fail, 9JJ5_A1EB0_A301:fail, 9UAU_A1EOM_A301:fail, 9UGF_A1EO5_A301:fail)
- Consensus method: `kmeans`
- Representative ligand (viz): `9GNO_A1INI_A301`
- Features kept: **3**

Support is the fraction of the cell's ligands that contribute to a feature (one row per feature / peak; all features are kept only above the support floor).

| Feature | Points | Ligands | Support |
|---|---:|---:|---:|
| Acceptor 1 | 210 | 85 | 0.98 |
| Acceptor 2 | 89 | 53 | 0.61 |
| Donor 1 | 69 | 69 | 0.79 |

## Feature resolution

Co-incident dual classifications collapsed by the feature hierarchy (higher-priority family kept on the shared atom); the listed ligands each carried both types on one atom.

| Kept ← dropped | Events | Ligands |
|---|---:|---|
| Aromatic ← LumpedHydrophobe | 84 | 1H00_FAP_A1300, 1H00_FCP_A1400, 1JVP_89E_P301, 1OIT_HDT_A1299, 1URW_I1P_A1300, 2R3F_SC8_A501, 2R3G_SC9_A501, 2R3I_SCF_A501, 2R3J_SCJ_A501, 2R3K_SCQ_A501, 2R3L_SCW_A501, 2R3M_SCX_A501, 2R3N_SCZ_A501, 2R3P_3SC_A501, 2R3Q_5SC_A501, 2R3R_6SC_A501, 2VTT_LZD_A1299, 3PXZ_JWS_A301, 3PY0_SU9_A301, 3QQF_X07_A543, 3QQJ_X11_A300, 3QRT_X14_A535, 3QWJ_X6A_A483, 3QX2_X63_A300, 3QXO_X65_A668, 3QZG_X67_A471, 3QZI_X72_A512, 3R28_XA0_A782, 3R73_X87_A920, 3RAI_X85_A923, 3RM6_18Z_A478, 3SW4_18K_A299, 4ACM_7YG_A1302, 4EK4_1CK_A301, 4EK5_03K_A300, 4EK6_10K_A301, 4EK8_16K_A301, 4FKG_4CK_A300, 4FKI_09K_A301, 4FKJ_11K_A301, 4FKO_20K_A301, 4FKP_LS5_A301, 4FKS_46K_A301, 4FKT_48K_A301, 4FKU_60K_A303, 4FKV_61K_A301, 4GCJ_X64_A305, 5ANJ_ZXC_A1299, 5IEY_6AE_A1001, 5K4J_6QB_A301, 5OO3_9ZB_A301, 6GUH_FB8_A301, 6GUK_FC8_A301, 6Q4D_HHT_A301, 6Q4G_HJK_A301, 6Q4H_HGH_A301, 6Q4I_HGK_A302, 6Q4J_HHB_A303, 6YL1_OWN_A301, 6YLK_OY2_A301, 7M2F_YOS_A901, 7QHL_D5P_C301, 7RA5_3I3_A301, 7RWE_7TH_A301, 7VDU_65L_A301, 7ZPC_JLC_A301, 8ERD_WQ6_A301, 8ERN_WQK_A402, 8RU8_I74_A301 |
| NegIonizable ← Acceptor | 10 | 4FKG_4CK_A300, 4FKU_60K_A303, 6Q4D_HHT_A301, 6Q4G_HJK_A301, 6Q4H_HGH_A301, 6Q4I_HGK_A302, 6Q4J_HHB_A303, 7M2F_YOS_A901, 7RWE_7TH_A301 |
| PosIonizable ← Donor | 41 | 1GZ8_MBP_A1300, 1H00_FAP_A1300, 1H00_FCP_A1400, 1URW_I1P_A1300, 2VTT_LZD_A1299, 3PY0_SU9_A301, 3R73_X87_A920, 3RAI_X85_A923, 3RM6_18Z_A478, 4ACM_7YG_A1302, 4FKJ_11K_A301, 4FKP_LS5_A301, 4FKT_48K_A301, 4FKV_61K_A301, 5ANE_SZL_A1299, 5ANJ_ZXC_A1299, 5IEY_6AE_A1001, 6GUK_FC8_A301, 6Q4E_HH5_A303, 6Q4G_HJK_A301, 6Q4H_HGH_A301, 7M2F_YOS_A901, 7QHL_D5P_C301, 7RA5_3I3_A301, 7VDU_65L_A301, 8ERN_WQK_A402, 8RU8_I74_A301, 9UAW_A1EOO_A301 |

## Not selected

Clusters/peaks that formed but did not enter the model — below the support or size floor, or displaced by the cross-family overlap merge — with their mean support (fraction of the cell's ligands contributing).

| Feature | Points | Ligands | Mean support |
|---|---:|---:|---:|
| Aromatic | 116 | 84 | 0.97 |
| Aromatic | 65 | 59 | 0.68 |
| Donor | 49 | 38 | 0.44 |
| Aromatic | 39 | 35 | 0.40 |
| PosIonizable | 16 | 16 | 0.18 |
| PosIonizable | 16 | 15 | 0.17 |
| Donor | 15 | 15 | 0.17 |
| Donor | 15 | 15 | 0.17 |
| Donor | 15 | 13 | 0.15 |
| LumpedHydrophobe | 11 | 11 | 0.13 |
| LumpedHydrophobe | 11 | 11 | 0.13 |
| PosIonizable | 12 | 9 | 0.10 |
| NegIonizable | 7 | 7 | 0.08 |
| Donor | 5 | 5 | 0.06 |
| LumpedHydrophobe | 4 | 4 | 0.05 |
| NegIonizable | 2 | 2 | 0.02 |
| LumpedHydrophobe | 1 | 1 | 0.01 |

See `pharmacophore.json` (model), `features.csv` (raw points + cluster ids), and `raw_features_*.png` (per-family point distributions, each kept peak annotated with its label and support).