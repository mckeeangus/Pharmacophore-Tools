# Pharmacophore — ca2/active_site__negative

- Ligands loaded: **76** (direct=13, template=63)
- Skipped poses: 0
- Consensus method: `kmeans`
- Representative ligand (viz): `5DRS_5EF_A305`
- Features kept: **4**

Support is the fraction of the cell's ligands that contribute to a feature (one row per feature / peak; all features are kept only above the support floor).

| Feature | Points | Ligands | Support |
|---|---:|---:|---:|
| Acceptor 1 | 74 | 73 | 0.96 |
| Acceptor 2 | 71 | 71 | 0.93 |
| Aromatic 1 | 62 | 59 | 0.78 |
| Donor 1 | 60 | 58 | 0.76 |

## Feature resolution

Co-incident dual classifications collapsed by the feature hierarchy (higher-priority family kept on the shared atom); the listed ligands each carried both types on one atom.

| Kept ← dropped | Events | Ligands |
|---|---:|---|
| Aromatic ← LumpedHydrophobe | 68 | 2FOS_B17_A301, 2NNO_M28_A301, 2NNS_M25_A301, 2NNV_M29_A301, 3K34_SUA_A1003, 3SAX_E50_A263, 4MTY_SBW_A302, 4PZH_V13_A305, 4Q08_V90_A305, 4WL4_FC5_A302, 4WW6_3TV_A306, 4YX4_FB2_A303, 4YXI_4J8_A303, 4YXO_4JC_A305, 4YYT_S2O_A305, 5DOH_5DU_B304, 5DRS_5EF_A305, 5JGS_EVF_B301, 5LL8_6YP_A306, 5LLC_V26_A308, 5M78_SAL_A304, 5NY6_9EB_A302, 5OGO_WWO_A302, 6HR3_4JE_A305, 6I0W_M4S_A308, 6I1U_3W8_A307, 6I3E_H1Z_A309, 6RFH_4SO_A305, 6RH4_4NZ_A308, 6RIG_K4N_A308, 6RIT_FBV_A306, 6RJJ_K5W_A305, 6RKN_FBS_A304, 6RL9_SAN_A304, 6RNP_KBB_A303, 6ROB_KBZ_A306, 6ROE_FBT_A307, 6RQI_FBW_A307, 6RRI_KFH_A304, 6RS5_KGK_A306, 6RSZ_KJ5_A305, 6SB7_8K2_A310, 6SBH_L4K_A304, 6SBL_L4Q_A306, 6SBM_L4W_A306, 6SD7_L7T_A304, 6SDI_0VV_A305, 6SFQ_7Q1_A304, 6SFU_LBQ_A308, 6SG6_LC8_A304, 6T81_MUE_A302, 7OYO_TKR_A302, 8BZZ_SVO_AAA303, 8QFK_UII_AAA301, 8QH8_V8I_A302, 8ROW_A1H15_A302, 9FJQ_A1IDL_A303, 9GFW_A1IKU_A302 |
| NegIonizable ← Acceptor | 5 | 2NNO_M28_A301, 5M78_SAL_A304, 6RFH_4SO_A305, 8QFK_UII_AAA301, 8QH8_V8I_A302 |
| PosIonizable ← Donor | 23 | 2NNO_M28_A301, 2NNS_M25_A301, 4FPT_0VZ_A303, 4FRC_0VY_A303, 4FU5_0VX_A303, 4FVN_0VW_A303, 4Q08_V90_A305, 5DRS_5EF_A305, 6G3Q_FO9_A302, 6SBL_L4Q_A306, 6SDI_0VV_A305, 6SDJ_J3K_A302, 8QFK_UII_AAA301 |

## Not selected

Clusters/peaks that formed but did not enter the model — below the support or size floor, or displaced by the cross-family overlap merge — with their mean support (fraction of the cell's ligands contributing).

| Feature | Points | Ligands | Mean support |
|---|---:|---:|---:|
| Donor | 24 | 21 | 0.28 |
| Acceptor | 29 | 19 | 0.25 |
| Acceptor | 20 | 19 | 0.25 |
| Acceptor | 22 | 17 | 0.22 |
| Acceptor | 13 | 11 | 0.14 |
| Acceptor | 13 | 11 | 0.14 |
| PosIonizable | 14 | 10 | 0.13 |
| Aromatic | 8 | 8 | 0.11 |
| PosIonizable | 9 | 5 | 0.07 |
| Acceptor | 6 | 5 | 0.07 |
| Aromatic | 3 | 3 | 0.04 |
| NegIonizable | 3 | 3 | 0.04 |
| Aromatic | 2 | 2 | 0.03 |
| NegIonizable | 2 | 2 | 0.03 |
| LumpedHydrophobe | 2 | 2 | 0.03 |
| LumpedHydrophobe | 1 | 1 | 0.01 |

See `pharmacophore.json` (model), `features.csv` (raw points + cluster ids), and `raw_features_*.png` (per-family point distributions, each kept peak annotated with its label and support).