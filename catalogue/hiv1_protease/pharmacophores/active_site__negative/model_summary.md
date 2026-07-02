# Pharmacophore — hiv1_protease/active_site__negative

- Ligands loaded: **32** (direct=3, template=29)
- Skipped poses: 0
- Consensus method: `kmeans`
- Representative ligand (viz): `6DV4_GA5_B201`
- Features kept: **10**

Support is the fraction of the cell's ligands that contribute to a feature (one row per feature / peak; all features are kept only above the support floor).

| Feature | Points | Ligands | Support |
|---|---:|---:|---:|
| Acceptor 1 | 47 | 23 | 0.72 |
| Acceptor 2 | 44 | 30 | 0.94 |
| Acceptor 3 | 35 | 21 | 0.66 |
| Acceptor 4 | 31 | 24 | 0.75 |
| Donor 1 | 38 | 28 | 0.88 |
| Donor 2 | 29 | 27 | 0.84 |
| LumpedHydrophobe 1 | 30 | 30 | 0.94 |
| LumpedHydrophobe 2 | 29 | 29 | 0.91 |
| LumpedHydrophobe 3 | 22 | 21 | 0.66 |
| LumpedHydrophobe 4 | 20 | 19 | 0.59 |

See `pharmacophore.json` (model), `features.csv` (raw points + cluster ids), and `raw_features_*.png` (per-family point distributions, each kept peak annotated with its label and support).