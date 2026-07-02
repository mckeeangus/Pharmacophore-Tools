# Pharmacophore — adora2a/orthosteric__neutral

- Ligands loaded: **5** (template=5)
- Skipped poses: 0
- Consensus method: `kmeans`
- Representative ligand (viz): `8CIC_U30_A1202`
- Features kept: **5**

Support is the fraction of the cell's ligands that contribute to a feature (one row per feature / peak; all features are kept only above the support floor).

| Feature | Points | Ligands | Support |
|---|---:|---:|---:|
| Acceptor 1 | 7 | 5 | 1.00 |
| Acceptor 2 | 6 | 5 | 1.00 |
| Aromatic 1 | 12 | 5 | 1.00 |
| Aromatic 2 | 4 | 3 | 0.60 |
| Donor 1 | 6 | 4 | 0.80 |

See `pharmacophore.json` (model), `features.csv` (raw points + cluster ids), and `raw_features_*.png` (per-family point distributions, each kept peak annotated with its label and support).