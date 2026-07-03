# Pharmacophore — esr1/lbp__negative

- Ligands loaded: **42** (direct=11, template=31)
- Skipped poses: 0
- Consensus method: `kmeans`
- Representative ligand (viz): `7NDO_RAL_B601`
- Features kept: **6**

Support is the fraction of the cell's ligands that contribute to a feature (one row per feature / peak; all features are kept only above the support floor).

| Feature | Points | Ligands | Support |
|---|---:|---:|---:|
| Acceptor 1 | 79 | 36 | 0.86 |
| Acceptor 2 | 38 | 35 | 0.83 |
| Acceptor 3 | 36 | 32 | 0.76 |
| Aromatic 1 | 44 | 42 | 1.00 |
| Aromatic 2 | 42 | 42 | 1.00 |
| PosIonizable 1 | 27 | 27 | 0.64 |

## Feature resolution

Co-incident dual classifications collapsed by the feature hierarchy (higher-priority family kept on the shared atom); the listed ligands each carried both types on one atom.

| Kept ← dropped | Events | Ligands |
|---|---:|---|
| Aromatic ← LumpedHydrophobe | 128 | 1XP1_AIH_A600, 1XP6_AIU_A600, 1XP9_AIJ_A600, 1XPC_AIT_A600, 2IOG_IOG_A600, 4ZNS_OFB_B601, 4ZNV_4Q7_B601, 5KCD_OB2_A601, 5KCE_OB3_A602, 5KCT_OB6_B601, 5KCT_OB7_A601, 5U2D_OBH_A601, 5W9C_OHT_D601, 5W9D_9XY_A601, 6PSJ_29S_B601, 6VJD_C3D_C601, 6VPF_53Q_B601, 7NDO_RAL_B601, 7RRX_7AI_B601, 7RRY_L84_C601, 7RRZ_77I_C601, 7RS0_7I9_C601, 7RS1_7Q5_C601, 7RS2_7I5_C601, 7RS3_7OR_B604, 7RS7_73I_A601, 7RS8_7EI_C601, 7RS9_7OI_C601, 7UJ7_NYU_C901, 7UJF_R3V_C601, 7UJO_QYM_C601, 7UJY_RL4_C601, 8DU8_TS7_B601, 8DUB_TTU_B601, 8DUC_TU9_A601, 8DUD_TV3_A601, 8DUK_TW6_C601, 8DV5_TX9_A601, 8DV7_TXK_B601, 8DV8_TZ3_A601, 8W03_OBT_C600, 9BU1_A1ASN_B601 |
| PosIonizable ← Donor | 26 | 1XP1_AIH_A600, 1XP6_AIU_A600, 1XP9_AIJ_A600, 1XPC_AIT_A600, 2IOG_IOG_A600, 5W9C_OHT_D601, 5W9D_9XY_A601, 6PSJ_29S_B601, 6VJD_C3D_C601, 6VPF_53Q_B601, 7NDO_RAL_B601, 7RRY_L84_C601, 7RRZ_77I_C601, 7RS8_7EI_C601, 7UJ7_NYU_C901, 7UJF_R3V_C601, 7UJO_QYM_C601, 7UJY_RL4_C601, 8DUB_TTU_B601, 8DUC_TU9_A601, 8DUD_TV3_A601, 8DUK_TW6_C601, 8DV5_TX9_A601, 8DV7_TXK_B601, 8DV8_TZ3_A601 |

## Not selected

Clusters/peaks that formed but did not enter the model — below the support or size floor, or displaced by the cross-family overlap merge — with their mean support (fraction of the cell's ligands contributing).

| Feature | Points | Ligands | Mean support |
|---|---:|---:|---:|
| Donor | 32 | 32 | 0.76 |
| Aromatic | 12 | 12 | 0.29 |
| Donor | 9 | 9 | 0.21 |
| Donor | 9 | 9 | 0.21 |
| Aromatic | 9 | 9 | 0.21 |
| Aromatic | 8 | 8 | 0.19 |
| Aromatic | 6 | 6 | 0.14 |
| Donor | 4 | 4 | 0.10 |
| Donor | 3 | 3 | 0.07 |
| Aromatic | 3 | 3 | 0.07 |
| Donor | 2 | 2 | 0.05 |
| LumpedHydrophobe | 2 | 2 | 0.05 |
| PosIonizable | 1 | 1 | 0.02 |
| Aromatic | 1 | 1 | 0.02 |

See `pharmacophore.json` (model), `features.csv` (raw points + cluster ids), and `raw_features_*.png` (per-family point distributions, each kept peak annotated with its label and support).