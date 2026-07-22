# Pharmacophore — gr_nr3c1/lbp__positive

- Ligands loaded: **20** (direct=1, template=19)
- Skipped poses: 0
- Consensus method: `kmeans`
- Representative ligand (viz): `7PRX_82H_A801`
- Features kept: **6**

**Support** = fraction of the cell's ligands that contribute to a feature (≤ 1.0; features are kept only above the 0.5 support floor). **Occupancy** = points ÷ contributing ligands (points-per-ligand, uncapped: > 1.0 when a cluster is denser than one point per ligand). One row per feature / peak.

| Feature | Points | Ligands | Support | Occupancy |
|---|---:|---:|---:|---:|
| Acceptor 1 | 69 | 20 | 1.00 | 3.45 |
| Acceptor 2 | 33 | 19 | 0.95 | 1.74 |
| Aromatic 1 | 24 | 13 | 0.65 | 1.85 |
| Aromatic 2 | 14 | 13 | 0.65 | 1.08 |
| Aromatic 3 | 10 | 10 | 0.50 | 1.00 |
| Donor 1 | 34 | 19 | 0.95 | 1.79 |

## Feature resolution

Co-incident dual classifications collapsed by the feature hierarchy (higher-priority family kept on the shared atom); the listed ligands each carried both types on one atom.

| Kept ← dropped | Events | Ligands |
|---|---:|---|
| Aromatic ← LumpedHydrophobe | 32 | 3BQD_DAY_A301, 3E7C_866_A1, 3K22_JZS_B1, 3K23_JZN_B2, 4CSJ_NN7_A1778, 4LSJ_LSJ_A801, 5G3J_E7T_A1779, 5G5W_R8C_A1778, 5NFT_8W8_A804, 6EL6_B9Q_A802, 6EL7_B9T_A802, 6EL9_B9W_A802, 7PRX_82H_A801, 8VKZ_A1ACE_A901 |
| PosIonizable ← Donor | 1 | 3K23_JZN_B2 |

## Below the support/size floor

Clusters that formed but never became candidates — below the 0.5 support floor or the minimum cluster size.

| Feature | Points | Ligands | Support | Occupancy |
|---|---:|---:|---:|---:|
| LumpedHydrophobe | 6 | 6 | 0.30 | 1.00 |
| Donor | 6 | 5 | 0.25 | 1.20 |
| LumpedHydrophobe | 2 | 2 | 0.10 | 1.00 |
| PosIonizable | 1 | 1 | 0.05 | 1.00 |
| LumpedHydrophobe | 1 | 1 | 0.05 | 1.00 |

See `pharmacophore.json` (model), `features.csv` (raw points + cluster ids), and `raw_features_*.png` (per-family point distributions, each kept peak annotated with its label and support).