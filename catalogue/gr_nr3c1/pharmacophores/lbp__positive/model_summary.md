# Pharmacophore — gr_nr3c1/lbp__positive

- Ligands loaded: **20** (direct=1, template=19)
- Skipped poses: 0
- Consensus method: `density`
- Representative ligand (viz): `3K23_JZN_B2`
- Features kept: **5**
- Excluded-volume spheres (receptor markers): **40**

**Support** = fraction of the cell's ligands that contribute to a feature (≤ 1.0; features are kept only above the 0.5 support floor). **Occupancy** = points ÷ contributing ligands (points-per-ligand, uncapped: > 1.0 when a cluster is denser than one point per ligand). One row per feature / peak.

| Feature | Points | Ligands | Support | Occupancy |
|---|---:|---:|---:|---:|
| Acceptor 1 | 14 | 14 | 0.70 | 1.00 |
| Acceptor 2 | 10 | 10 | 0.50 | 1.00 |
| Aromatic 1 | 16 | 11 | 0.55 | 1.45 |
| Aromatic 2 | 10 | 10 | 0.50 | 1.00 |
| LumpedHydrophobe 1 | 14 | 14 | 0.70 | 1.00 |

## Feature resolution

Co-incident dual classifications collapsed by the feature hierarchy (higher-priority family kept on the shared atom); the listed ligands each carried both types on one atom.

| Kept ← dropped | Events | Ligands |
|---|---:|---|
| PosIonizable ← Donor | 1 | 3K23_JZN_B2 |

## Below the support/size floor

Clusters that formed but never became candidates — below the 0.5 support floor or the minimum cluster size.

| Feature | Points | Ligands | Support | Occupancy |
|---|---:|---:|---:|---:|
| Donor | 9 | 9 | 0.45 | 1.00 |
| LumpedHydrophobe | 9 | 9 | 0.45 | 1.00 |
| Acceptor | 6 | 6 | 0.30 | 1.00 |
| Acceptor | 6 | 6 | 0.30 | 1.00 |
| LumpedHydrophobe | 6 | 6 | 0.30 | 1.00 |
| Acceptor | 3 | 3 | 0.15 | 1.00 |
| Donor | 2 | 2 | 0.10 | 1.00 |
| Aromatic | 2 | 2 | 0.10 | 1.00 |
| Donor | 1 | 1 | 0.05 | 1.00 |
| PosIonizable | 1 | 1 | 0.05 | 1.00 |

See `pharmacophore.json` (model), `features.csv` (raw points + cluster ids), and `raw_features_*.png` (per-family point distributions, each kept peak annotated with its label and support).