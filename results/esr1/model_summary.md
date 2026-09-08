# Pharmacophore — esr1

- Ligands loaded: **50** (sdf=50)
- Skipped poses: 0
- Consensus method: `density`
- Representative ligand (viz): `STK803083`
- Features kept: **6**

**Support** = fraction of the cell's ligands that contribute to a feature (≤ 1.0; features are kept only above the 0.5 support floor). **Occupancy** = points ÷ contributing ligands (points-per-ligand, uncapped: > 1.0 when a cluster is denser than one point per ligand). One row per feature / peak.

| Feature | Points | Ligands | Support | Occupancy |
|---|---:|---:|---:|---:|
| Acceptor 1 | 50 | 50 | 1.00 | 1.00 |
| Acceptor 2 | 29 | 29 | 0.58 | 1.00 |
| Aromatic 1 | 50 | 50 | 1.00 | 1.00 |
| Donor 1 | 46 | 46 | 0.92 | 1.00 |
| LumpedHydrophobe 1 | 50 | 50 | 1.00 | 1.00 |
| LumpedHydrophobe 2 | 34 | 29 | 0.58 | 1.17 |

## Below the support/size floor

Clusters that formed but never became candidates — below the 0.5 support floor or the minimum cluster size.

| Feature | Points | Ligands | Support | Occupancy |
|---|---:|---:|---:|---:|
| Donor | 23 | 23 | 0.46 | 1.00 |
| Aromatic | 21 | 21 | 0.42 | 1.00 |

See `pharmacophore.json` (model), `features.csv` (raw points + cluster ids), and `raw_features_*.png` (per-family point distributions, each kept peak annotated with its label and support).