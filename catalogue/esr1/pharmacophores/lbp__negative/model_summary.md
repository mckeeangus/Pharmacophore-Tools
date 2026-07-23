# Pharmacophore — esr1/lbp__negative

- Ligands loaded: **42** (direct=11, template=31)
- Skipped poses: 0
- Consensus method: `density`
- Representative ligand (viz): `7NDO_RAL_B601`
- Features kept: **9**
- Excluded-volume spheres (receptor markers): **40**

**Support** = fraction of the cell's ligands that contribute to a feature (≤ 1.0; features are kept only above the 0.5 support floor). **Occupancy** = points ÷ contributing ligands (points-per-ligand, uncapped: > 1.0 when a cluster is denser than one point per ligand). One row per feature / peak.

| Feature | Points | Ligands | Support | Occupancy |
|---|---:|---:|---:|---:|
| Acceptor 1 | 32 | 32 | 0.76 | 1.00 |
| Acceptor 2 | 32 | 32 | 0.76 | 1.00 |
| Acceptor 3 | 22 | 22 | 0.52 | 1.00 |
| Aromatic 1 | 42 | 42 | 1.00 | 1.00 |
| Aromatic 2 | 40 | 40 | 0.95 | 1.00 |
| Donor 1 | 32 | 32 | 0.76 | 1.00 |
| LumpedHydrophobe 1 | 42 | 42 | 1.00 | 1.00 |
| LumpedHydrophobe 2 | 40 | 40 | 0.95 | 1.00 |
| PosIonizable 1 | 24 | 24 | 0.57 | 1.00 |

## Feature resolution

Co-incident dual classifications collapsed by the feature hierarchy (higher-priority family kept on the shared atom); the listed ligands each carried both types on one atom.

| Kept ← dropped | Events | Ligands |
|---|---:|---|
| PosIonizable ← Donor | 26 | 1XP1_AIH_A600, 1XP6_AIU_A600, 1XP9_AIJ_A600, 1XPC_AIT_A600, 2IOG_IOG_A600, 5W9C_OHT_D601, 5W9D_9XY_A601, 6PSJ_29S_B601, 6VJD_C3D_C601, 6VPF_53Q_B601, 7NDO_RAL_B601, 7RRY_L84_C601, 7RRZ_77I_C601, 7RS8_7EI_C601, 7UJ7_NYU_C901, 7UJF_R3V_C601, 7UJO_QYM_C601, 7UJY_RL4_C601, 8DUB_TTU_B601, 8DUC_TU9_A601, 8DUD_TV3_A601, 8DUK_TW6_C601, 8DV5_TX9_A601, 8DV7_TXK_B601, 8DV8_TZ3_A601 |

## Below the support/size floor

Clusters that formed but never became candidates — below the 0.5 support floor or the minimum cluster size.

| Feature | Points | Ligands | Support | Occupancy |
|---|---:|---:|---:|---:|
| Acceptor | 18 | 17 | 0.40 | 1.06 |
| Aromatic | 12 | 12 | 0.29 | 1.00 |
| LumpedHydrophobe | 12 | 12 | 0.29 | 1.00 |
| Donor | 9 | 9 | 0.21 | 1.00 |
| Donor | 9 | 9 | 0.21 | 1.00 |
| Donor | 4 | 4 | 0.10 | 1.00 |
| PosIonizable | 1 | 1 | 0.02 | 1.00 |
| Aromatic | 1 | 1 | 0.02 | 1.00 |
| LumpedHydrophobe | 1 | 1 | 0.02 | 1.00 |

See `pharmacophore.json` (model), `features.csv` (raw points + cluster ids), and `raw_features_*.png` (per-family point distributions, each kept peak annotated with its label and support).