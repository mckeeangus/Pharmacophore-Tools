# Pharmacophore — adora2a

- Ligands loaded: **50** (sdf=50)
- Skipped poses: 0
- Consensus method: `density`
- Representative ligand (viz): `OSSL_644910`
- Features kept: **4**

**Support** = fraction of the cell's ligands that contribute to a feature (≤ 1.0; features are kept only above the 0.5 support floor). **Occupancy** = points ÷ contributing ligands (points-per-ligand, uncapped: > 1.0 when a cluster is denser than one point per ligand). One row per feature / peak.

| Feature | Points | Ligands | Support | Occupancy |
|---|---:|---:|---:|---:|
| Acceptor 1 | 41 | 41 | 0.82 | 1.00 |
| Acceptor 2 | 33 | 27 | 0.54 | 1.22 |
| Aromatic 1 | 40 | 38 | 0.76 | 1.05 |
| Donor 1 | 30 | 30 | 0.60 | 1.00 |

## Feature resolution

Co-incident dual classifications collapsed by the feature hierarchy (higher-priority family kept on the shared atom); the listed ligands each carried both types on one atom.

| Kept ← dropped | Events | Ligands |
|---|---:|---|
| PosIonizable ← Donor | 6 | Z1770253642, Z52660414, Z52665462, Z52665806 |

## Below the support/size floor

Clusters that formed but never became candidates — below the 0.5 support floor or the minimum cluster size.

| Feature | Points | Ligands | Support | Occupancy |
|---|---:|---:|---:|---:|
| Acceptor | 21 | 21 | 0.42 | 1.00 |
| Aromatic | 18 | 17 | 0.34 | 1.06 |
| LumpedHydrophobe | 17 | 17 | 0.34 | 1.00 |
| Donor | 23 | 16 | 0.32 | 1.44 |
| LumpedHydrophobe | 12 | 12 | 0.24 | 1.00 |
| PosIonizable | 4 | 4 | 0.08 | 1.00 |
| LumpedHydrophobe | 3 | 3 | 0.06 | 1.00 |
| Aromatic | 2 | 2 | 0.04 | 1.00 |
| Acceptor | 1 | 1 | 0.02 | 1.00 |
| PosIonizable | 1 | 1 | 0.02 | 1.00 |
| Aromatic | 1 | 1 | 0.02 | 1.00 |
| LumpedHydrophobe | 1 | 1 | 0.02 | 1.00 |
| LumpedHydrophobe | 1 | 1 | 0.02 | 1.00 |
| LumpedHydrophobe | 1 | 1 | 0.02 | 1.00 |

See `pharmacophore.json` (model), `features.csv` (raw points + cluster ids), and `raw_features_*.png` (per-family point distributions, each kept peak annotated with its label and support).