# Pharmacophore — nachr_a4b2/orthosteric__neutral

- Ligands loaded: **9** (template=9)
- Skipped poses: 0
- Consensus method: `kmeans`
- Representative ligand (viz): `2XYT_TC9_F1206`
- Features kept: **3**

**Support** = fraction of the cell's ligands that contribute to a feature (≤ 1.0; features are kept only above the 0.5 support floor). **Occupancy** = points ÷ contributing ligands (points-per-ligand, uncapped: > 1.0 when a cluster is denser than one point per ligand). One row per feature / peak.

| Feature | Points | Ligands | Support | Occupancy |
|---|---:|---:|---:|---:|
| Acceptor 1 | 24 | 9 | 1.00 | 2.67 |
| Acceptor 2 | 13 | 6 | 0.67 | 2.17 |
| Donor 1 | 6 | 5 | 0.56 | 1.20 |

## Feature resolution

Co-incident dual classifications collapsed by the feature hierarchy (higher-priority family kept on the shared atom); the listed ligands each carried both types on one atom.

| Kept ← dropped | Events | Ligands |
|---|---:|---|
| Aromatic ← LumpedHydrophobe | 8 | 2WNC_TKT_C300, 2XYS_SY9_E1206, 2XYT_TC9_F1206, 3SIO_MLK_D260, 9SG3_PHN_A302 |
| PosIonizable ← Donor | 4 | 2WNC_TKT_C300, 2XYS_SY9_E1206, 2XYT_TC9_F1206, 3SIO_MLK_D260 |

## Below the support/size floor

Clusters that formed but never became candidates — below the 0.5 support floor or the minimum cluster size.

| Feature | Points | Ligands | Support | Occupancy |
|---|---:|---:|---:|---:|
| Aromatic | 8 | 4 | 0.44 | 2.00 |
| PosIonizable | 4 | 4 | 0.44 | 1.00 |
| Aromatic | 3 | 2 | 0.22 | 1.50 |
| Donor | 1 | 1 | 0.11 | 1.00 |
| Donor | 1 | 1 | 0.11 | 1.00 |
| PosIonizable | 1 | 1 | 0.11 | 1.00 |

See `pharmacophore.json` (model), `features.csv` (raw points + cluster ids), and `raw_features_*.png` (per-family point distributions, each kept peak annotated with its label and support).