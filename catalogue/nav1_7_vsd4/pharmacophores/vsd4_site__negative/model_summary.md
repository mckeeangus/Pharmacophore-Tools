# Pharmacophore — nav1_7_vsd4/vsd4_site__negative

- Ligands loaded: **3** (template=3)
- Skipped poses: 0
- Consensus method: `density`
- Representative ligand (viz): `8F0P_X7L_A1610`
- Features kept: **3**
- Excluded-volume spheres (receptor markers): **40**

**Support** = fraction of the cell's ligands that contribute to a feature (≤ 1.0; features are kept only above the 0.5 support floor). **Occupancy** = points ÷ contributing ligands (points-per-ligand, uncapped: > 1.0 when a cluster is denser than one point per ligand). One row per feature / peak.

| Feature | Points | Ligands | Support | Occupancy |
|---|---:|---:|---:|---:|
| Donor 1 | 3 | 3 | 1.00 | 1.00 |
| LumpedHydrophobe 1 | 2 | 2 | 0.67 | 1.00 |
| PosIonizable 1 | 2 | 2 | 0.67 | 1.00 |

## Feature resolution

Co-incident dual classifications collapsed by the feature hierarchy (higher-priority family kept on the shared atom); the listed ligands each carried both types on one atom.

| Kept ← dropped | Events | Ligands |
|---|---:|---|
| Aromatic ← LumpedHydrophobe | 6 | 8F0P_X7L_A1610, 8F0R_X7W_A1606, 8F0S_X80_A1605 |
| PosIonizable ← Donor | 3 | 8F0P_X7L_A1610, 8F0R_X7W_A1606, 8F0S_X80_A1605 |

## Below the support/size floor

Clusters that formed but never became candidates — below the 0.5 support floor or the minimum cluster size.

| Feature | Points | Ligands | Support | Occupancy |
|---|---:|---:|---:|---:|
| Acceptor | 4 | 3 | 1.00 | 1.33 |
| Aromatic | 3 | 3 | 1.00 | 1.00 |
| Aromatic | 3 | 3 | 1.00 | 1.00 |
| Acceptor | 3 | 2 | 0.67 | 1.50 |
| Donor | 2 | 2 | 0.67 | 1.00 |
| Aromatic | 1 | 1 | 0.33 | 1.00 |

See `pharmacophore.json` (model), `features.csv` (raw points + cluster ids), and `raw_features_*.png` (per-family point distributions, each kept peak annotated with its label and support).