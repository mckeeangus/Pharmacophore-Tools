# Pharmacophore — cavab/dhp_site__negative

- Ligands loaded: **3** (template=3)
- Skipped poses: 0
- Consensus method: `kmeans`
- Representative ligand (viz): `6KE5_6UB_B1301`
- Features kept: **4**

**Support** = fraction of the cell's ligands that contribute to a feature (≤ 1.0; features are kept only above the 0.5 support floor). **Occupancy** = points ÷ contributing ligands (points-per-ligand, uncapped: > 1.0 when a cluster is denser than one point per ligand). One row per feature / peak.

| Feature | Points | Ligands | Support | Occupancy |
|---|---:|---:|---:|---:|
| Acceptor 1 | 6 | 3 | 1.00 | 2.00 |
| Aromatic 1 | 2 | 2 | 0.67 | 1.00 |
| Donor 1 | 2 | 2 | 0.67 | 1.00 |
| PosIonizable 1 | 2 | 2 | 0.67 | 1.00 |

## Feature resolution

Co-incident dual classifications collapsed by the feature hierarchy (higher-priority family kept on the shared atom); the listed ligands each carried both types on one atom.

| Kept ← dropped | Events | Ligands |
|---|---:|---|
| Aromatic ← LumpedHydrophobe | 3 | 5KLS_6UC_C1304, 5KMF_6U9_A1301, 6KE5_6UB_B1301 |
| PosIonizable ← Donor | 2 | 5KLS_6UC_C1304, 6KE5_6UB_B1301 |

## Below the support/size floor

Clusters that formed but never became candidates — below the 0.5 support floor or the minimum cluster size.

| Feature | Points | Ligands | Support | Occupancy |
|---|---:|---:|---:|---:|
| Acceptor | 3 | 1 | 0.33 | 3.00 |
| Acceptor | 3 | 1 | 0.33 | 3.00 |
| Acceptor | 3 | 1 | 0.33 | 3.00 |
| LumpedHydrophobe | 2 | 1 | 0.33 | 2.00 |
| Donor | 1 | 1 | 0.33 | 1.00 |
| Aromatic | 1 | 1 | 0.33 | 1.00 |

See `pharmacophore.json` (model), `features.csv` (raw points + cluster ids), and `raw_features_*.png` (per-family point distributions, each kept peak annotated with its label and support).