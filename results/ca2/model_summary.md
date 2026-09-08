# Pharmacophore — ca2

- Ligands loaded: **23** (sdf=23)
- Skipped poses: 0
- Consensus method: `density`
- Representative ligand (viz): `Z56785999`
- Features kept: **2**

**Support** = fraction of the cell's ligands that contribute to a feature (≤ 1.0; features are kept only above the 0.5 support floor). **Occupancy** = points ÷ contributing ligands (points-per-ligand, uncapped: > 1.0 when a cluster is denser than one point per ligand). One row per feature / peak.

| Feature | Points | Ligands | Support | Occupancy |
|---|---:|---:|---:|---:|
| Acceptor 1 | 33 | 19 | 0.83 | 1.74 |
| Aromatic 1 | 22 | 22 | 0.96 | 1.00 |

## Feature resolution

Co-incident dual classifications collapsed by the feature hierarchy (higher-priority family kept on the shared atom); the listed ligands each carried both types on one atom.

| Kept ← dropped | Events | Ligands |
|---|---:|---|
| PosIonizable ← LumpedHydrophobe | 1 | Z56771527 |

## Below the support/size floor

Clusters that formed but never became candidates — below the 0.5 support floor or the minimum cluster size.

| Feature | Points | Ligands | Support | Occupancy |
|---|---:|---:|---:|---:|
| Donor | 4 | 3 | 0.13 | 1.33 |
| Acceptor | 3 | 3 | 0.13 | 1.00 |
| Aromatic | 2 | 2 | 0.09 | 1.00 |
| Donor | 2 | 2 | 0.09 | 1.00 |
| LumpedHydrophobe | 2 | 2 | 0.09 | 1.00 |
| Acceptor | 1 | 1 | 0.04 | 1.00 |
| Acceptor | 1 | 1 | 0.04 | 1.00 |
| Acceptor | 1 | 1 | 0.04 | 1.00 |
| Aromatic | 1 | 1 | 0.04 | 1.00 |
| Aromatic | 1 | 1 | 0.04 | 1.00 |
| Donor | 1 | 1 | 0.04 | 1.00 |
| Donor | 1 | 1 | 0.04 | 1.00 |
| Donor | 1 | 1 | 0.04 | 1.00 |
| LumpedHydrophobe | 1 | 1 | 0.04 | 1.00 |
| LumpedHydrophobe | 1 | 1 | 0.04 | 1.00 |
| LumpedHydrophobe | 1 | 1 | 0.04 | 1.00 |
| LumpedHydrophobe | 1 | 1 | 0.04 | 1.00 |
| PosIonizable | 1 | 1 | 0.04 | 1.00 |

See `pharmacophore.json` (model), `features.csv` (raw points + cluster ids), and `raw_features_*.png` (per-family point distributions, each kept peak annotated with its label and support).