# Pharmacophore — hiv1_protease

- Ligands loaded: **50** (sdf=50)
- Skipped poses: 0
- Consensus method: `density`
- Representative ligand (viz): `STL001747`
- Features kept: **8**

**Support** = fraction of the cell's ligands that contribute to a feature (≤ 1.0; features are kept only above the 0.5 support floor). **Occupancy** = points ÷ contributing ligands (points-per-ligand, uncapped: > 1.0 when a cluster is denser than one point per ligand). One row per feature / peak.

| Feature | Points | Ligands | Support | Occupancy |
|---|---:|---:|---:|---:|
| Acceptor 1 | 38 | 36 | 0.72 | 1.06 |
| Acceptor 2 | 36 | 36 | 0.72 | 1.00 |
| Aromatic 1 | 44 | 44 | 0.88 | 1.00 |
| Aromatic 2 | 34 | 34 | 0.68 | 1.00 |
| Aromatic 3 | 30 | 30 | 0.60 | 1.00 |
| LumpedHydrophobe 1 | 43 | 43 | 0.86 | 1.00 |
| LumpedHydrophobe 2 | 33 | 33 | 0.66 | 1.00 |
| LumpedHydrophobe 3 | 33 | 33 | 0.66 | 1.00 |

## Feature resolution

Co-incident dual classifications collapsed by the feature hierarchy (higher-priority family kept on the shared atom); the listed ligands each carried both types on one atom.

| Kept ← dropped | Events | Ligands |
|---|---:|---|
| PosIonizable ← Donor | 16 | G747-0001, G747-0004, G747-0011, G747-0035, G747-0043, G747-0051, G747-0063, G747-0365, G747-0390, G747-0519, G747-0544, Z358287958, Z8979036846 |

## Below the support/size floor

Clusters that formed but never became candidates — below the 0.5 support floor or the minimum cluster size.

| Feature | Points | Ligands | Support | Occupancy |
|---|---:|---:|---:|---:|
| Acceptor | 24 | 24 | 0.48 | 1.00 |
| Donor | 16 | 16 | 0.32 | 1.00 |
| Acceptor | 12 | 11 | 0.22 | 1.09 |
| Donor | 11 | 11 | 0.22 | 1.00 |
| Aromatic | 6 | 6 | 0.12 | 1.00 |
| LumpedHydrophobe | 4 | 4 | 0.08 | 1.00 |
| PosIonizable | 4 | 4 | 0.08 | 1.00 |
| Acceptor | 3 | 3 | 0.06 | 1.00 |
| PosIonizable | 3 | 3 | 0.06 | 1.00 |
| Aromatic | 2 | 2 | 0.04 | 1.00 |
| Aromatic | 2 | 2 | 0.04 | 1.00 |
| LumpedHydrophobe | 2 | 2 | 0.04 | 1.00 |
| LumpedHydrophobe | 2 | 2 | 0.04 | 1.00 |
| LumpedHydrophobe | 2 | 2 | 0.04 | 1.00 |
| Donor | 1 | 1 | 0.02 | 1.00 |
| Donor | 1 | 1 | 0.02 | 1.00 |
| Acceptor | 1 | 1 | 0.02 | 1.00 |
| PosIonizable | 1 | 1 | 0.02 | 1.00 |

See `pharmacophore.json` (model), `features.csv` (raw points + cluster ids), and `raw_features_*.png` (per-family point distributions, each kept peak annotated with its label and support).