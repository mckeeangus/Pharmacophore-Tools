# Pharmacophore — gr_nr3c1

- Ligands loaded: **50** (sdf=50)
- Skipped poses: 0
- Consensus method: `density`
- Representative ligand (viz): `Z9466035860`
- Features kept: **8**

**Support** = fraction of the cell's ligands that contribute to a feature (≤ 1.0; features are kept only above the 0.5 support floor). **Occupancy** = points ÷ contributing ligands (points-per-ligand, uncapped: > 1.0 when a cluster is denser than one point per ligand). One row per feature / peak.

| Feature | Points | Ligands | Support | Occupancy |
|---|---:|---:|---:|---:|
| Acceptor 1 | 41 | 41 | 0.82 | 1.00 |
| Acceptor 2 | 27 | 27 | 0.54 | 1.00 |
| Aromatic 1 | 41 | 41 | 0.82 | 1.00 |
| Aromatic 2 | 30 | 30 | 0.60 | 1.00 |
| Donor 1 | 41 | 41 | 0.82 | 1.00 |
| LumpedHydrophobe 1 | 36 | 36 | 0.72 | 1.00 |
| LumpedHydrophobe 2 | 32 | 32 | 0.64 | 1.00 |
| LumpedHydrophobe 3 | 25 | 25 | 0.50 | 1.00 |

## Feature resolution

Co-incident dual classifications collapsed by the feature hierarchy (higher-priority family kept on the shared atom); the listed ligands each carried both types on one atom.

| Kept ← dropped | Events | Ligands |
|---|---:|---|
| PosIonizable ← Donor | 20 | 3966-0064, 4119-0011, K788-9145, OSSL_457771, STK837320, V003-6048, V018-4858, V024-3760, V025-8049, V027-4235, V028-1746, Z16435552, Z30763274, Z30764334, Z3688957256, Z8786580910 |
| PosIonizable ← LumpedHydrophobe | 2 | Z16435552, Z26762628 |

## Below the support/size floor

Clusters that formed but never became candidates — below the 0.5 support floor or the minimum cluster size.

| Feature | Points | Ligands | Support | Occupancy |
|---|---:|---:|---:|---:|
| Aromatic | 22 | 22 | 0.44 | 1.00 |
| Acceptor | 14 | 14 | 0.28 | 1.00 |
| Donor | 6 | 6 | 0.12 | 1.00 |
| Acceptor | 4 | 4 | 0.08 | 1.00 |
| Aromatic | 4 | 4 | 0.08 | 1.00 |
| LumpedHydrophobe | 4 | 4 | 0.08 | 1.00 |
| Acceptor | 6 | 3 | 0.06 | 2.00 |
| Donor | 3 | 3 | 0.06 | 1.00 |
| LumpedHydrophobe | 3 | 3 | 0.06 | 1.00 |
| PosIonizable | 3 | 3 | 0.06 | 1.00 |
| Aromatic | 2 | 2 | 0.04 | 1.00 |
| LumpedHydrophobe | 2 | 2 | 0.04 | 1.00 |
| PosIonizable | 2 | 2 | 0.04 | 1.00 |
| PosIonizable | 2 | 2 | 0.04 | 1.00 |
| PosIonizable | 2 | 2 | 0.04 | 1.00 |
| Donor | 1 | 1 | 0.02 | 1.00 |
| Donor | 1 | 1 | 0.02 | 1.00 |
| Donor | 1 | 1 | 0.02 | 1.00 |
| Acceptor | 1 | 1 | 0.02 | 1.00 |
| Acceptor | 1 | 1 | 0.02 | 1.00 |
| Acceptor | 1 | 1 | 0.02 | 1.00 |
| Acceptor | 1 | 1 | 0.02 | 1.00 |
| Acceptor | 1 | 1 | 0.02 | 1.00 |
| Aromatic | 1 | 1 | 0.02 | 1.00 |
| Aromatic | 1 | 1 | 0.02 | 1.00 |
| Aromatic | 1 | 1 | 0.02 | 1.00 |
| Aromatic | 1 | 1 | 0.02 | 1.00 |
| LumpedHydrophobe | 1 | 1 | 0.02 | 1.00 |
| LumpedHydrophobe | 1 | 1 | 0.02 | 1.00 |
| LumpedHydrophobe | 1 | 1 | 0.02 | 1.00 |
| LumpedHydrophobe | 1 | 1 | 0.02 | 1.00 |
| LumpedHydrophobe | 1 | 1 | 0.02 | 1.00 |
| LumpedHydrophobe | 1 | 1 | 0.02 | 1.00 |
| PosIonizable | 1 | 1 | 0.02 | 1.00 |
| PosIonizable | 1 | 1 | 0.02 | 1.00 |
| PosIonizable | 1 | 1 | 0.02 | 1.00 |
| PosIonizable | 1 | 1 | 0.02 | 1.00 |

See `pharmacophore.json` (model), `features.csv` (raw points + cluster ids), and `raw_features_*.png` (per-family point distributions, each kept peak annotated with its label and support).