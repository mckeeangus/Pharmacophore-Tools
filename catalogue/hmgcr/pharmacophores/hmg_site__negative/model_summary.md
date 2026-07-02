# Pharmacophore — hmgcr/hmg_site__negative

- Ligands loaded: **18** (template=18)
- Skipped poses: 0
- Consensus method: `kmeans`
- Representative ligand (viz): `3CCT_3HI_D3`
- Features kept: **10**

Support is the fraction of the cell's ligands that contribute to a feature (one row per feature / peak; all features are kept only above the support floor).

| Feature | Points | Ligands | Support |
|---|---:|---:|---:|
| Acceptor 1 | 19 | 15 | 0.83 |
| Acceptor 2 | 18 | 18 | 1.00 |
| Acceptor 3 | 15 | 15 | 0.83 |
| Aromatic 1 | 18 | 16 | 0.89 |
| Aromatic 2 | 15 | 15 | 0.83 |
| Aromatic 3 | 12 | 11 | 0.61 |
| Donor 1 | 18 | 18 | 1.00 |
| Donor 2 | 18 | 18 | 1.00 |
| Donor 3 | 14 | 10 | 0.56 |
| LumpedHydrophobe 1 | 15 | 15 | 0.83 |

See `pharmacophore.json` (model), `features.csv` (raw points + cluster ids), and `raw_features_*.png` (per-family point distributions, each kept peak annotated with its label and support).