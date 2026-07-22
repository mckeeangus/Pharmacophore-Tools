# Pharmacophore — net_slc6a2/central_s1__negative

- Ligands loaded: **25** (direct=3, template=22)
- Skipped poses: 0
- Consensus method: `kmeans`
- Representative ligand (viz): `4XNX_41X_A707`
- Features kept: **3**

**Support** = fraction of the cell's ligands that contribute to a feature (≤ 1.0; features are kept only above the 0.5 support floor). **Occupancy** = points ÷ contributing ligands (points-per-ligand, uncapped: > 1.0 when a cluster is denser than one point per ligand). One row per feature / peak.

| Feature | Points | Ligands | Support | Occupancy |
|---|---:|---:|---:|---:|
| Acceptor 1 | 29 | 16 | 0.64 | 1.81 |
| Aromatic 1 | 38 | 24 | 0.96 | 1.58 |
| PosIonizable 1 | 17 | 17 | 0.68 | 1.00 |

## Feature resolution

Co-incident dual classifications collapsed by the feature hierarchy (higher-priority family kept on the shared atom); the listed ligands each carried both types on one atom.

| Kept ← dropped | Events | Ligands |
|---|---:|---|
| Aromatic ← LumpedHydrophobe | 46 | 4M48_21B_A704, 4XNX_41X_A707, 4XP4_COC_A706, 4XPF_42F_A703, 4XPG_42L_A701, 6M38_29E_A601, 6M3Z_F0F_A701, 6M47_F1U_A608, 8HFI_DSM_A701, 8HFL_1XR_A701, 8I3V_68P_A701, 8WTX_Y60_A701, 8WTY_XEF_A701, 8XB2_YNT_A702, 8Y8Z_A1LX3_E701, 8Y90_A1LX6_A701, 8Y91_A1LX5_D703, 8Y93_TP0_A701, 8YR2_41U_B701, 8ZP1_A1D9Y_A702, 8ZP2_A1LX4_A701, 9JEL_A1EBN_A701, 9JF3_A1EBO_A701, 9KDH_A1D5S_B709, 9KE3_A1EFR_B707 |
| PosIonizable ← Donor | 26 | 4M48_21B_A704, 4XNX_41X_A707, 4XP4_COC_A706, 4XPF_42F_A703, 4XPG_42L_A701, 6M38_29E_A601, 6M3Z_F0F_A701, 6M47_F1U_A608, 8HFI_DSM_A701, 8HFL_1XR_A701, 8I3V_68P_A701, 8WTX_Y60_A701, 8WTY_XEF_A701, 8XB2_YNT_A702, 8Y8Z_A1LX3_E701, 8Y90_A1LX6_A701, 8Y91_A1LX5_D703, 8Y93_TP0_A701, 8YR2_41U_B701, 8ZP1_A1D9Y_A702, 8ZP2_A1LX4_A701, 9KDH_A1D5S_B709, 9KE3_A1EFR_B707 |

## Below the support/size floor

Clusters that formed but never became candidates — below the 0.5 support floor or the minimum cluster size.

| Feature | Points | Ligands | Support | Occupancy |
|---|---:|---:|---:|---:|
| PosIonizable | 11 | 9 | 0.36 | 1.22 |
| Aromatic | 8 | 5 | 0.20 | 1.60 |
| Acceptor | 9 | 4 | 0.16 | 2.25 |
| Donor | 3 | 3 | 0.12 | 1.00 |
| LumpedHydrophobe | 2 | 2 | 0.08 | 1.00 |
| Donor | 2 | 2 | 0.08 | 1.00 |
| LumpedHydrophobe | 1 | 1 | 0.04 | 1.00 |

See `pharmacophore.json` (model), `features.csv` (raw points + cluster ids), and `raw_features_*.png` (per-family point distributions, each kept peak annotated with its label and support).