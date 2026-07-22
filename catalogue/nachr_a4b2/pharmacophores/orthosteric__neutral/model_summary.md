# Pharmacophore — nachr_a4b2/orthosteric__neutral

- Ligands loaded: **9** (template=9)
- Skipped poses: 0
- Consensus method: `density`
- Representative ligand (viz): `2XYT_TC9_F1206`
- Features kept: **0**
- Excluded-volume spheres (receptor markers): **40**

**Support** = fraction of the cell's ligands that contribute to a feature (≤ 1.0; features are kept only above the 0.5 support floor). **Occupancy** = points ÷ contributing ligands (points-per-ligand, uncapped: > 1.0 when a cluster is denser than one point per ligand). One row per feature / peak.

| Feature | Points | Ligands | Support | Occupancy |
|---|---:|---:|---:|---:|

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
| Acceptor | 3 | 3 | 0.33 | 1.00 |
| PosIonizable | 3 | 3 | 0.33 | 1.00 |
| Donor | 2 | 2 | 0.22 | 1.00 |
| Acceptor | 2 | 1 | 0.11 | 2.00 |
| Donor | 1 | 1 | 0.11 | 1.00 |
| Donor | 1 | 1 | 0.11 | 1.00 |
| PosIonizable | 1 | 1 | 0.11 | 1.00 |
| Aromatic | 1 | 1 | 0.11 | 1.00 |
| Aromatic | 1 | 1 | 0.11 | 1.00 |
| Aromatic | 1 | 1 | 0.11 | 1.00 |

See `pharmacophore.json` (model), `features.csv` (raw points + cluster ids), and `raw_features_*.png` (per-family point distributions, each kept peak annotated with its label and support).