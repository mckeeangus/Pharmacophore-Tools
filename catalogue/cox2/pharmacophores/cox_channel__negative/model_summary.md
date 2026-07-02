# Pharmacophore — cox2/cox_channel__negative

- Ligands loaded: **5** (template=5)
- Skipped poses: 0
- Consensus method: `kmeans`
- Representative ligand (viz): `5IKR_ID8_A601`
- Features kept: **3**

Support is the fraction of the cell's ligands that contribute to a feature (one row per feature / peak; all features are kept only above the support floor).

| Feature | Points | Ligands | Support |
|---|---:|---:|---:|
| Acceptor 1 | 7 | 5 | 1.00 |
| Aromatic 1 | 5 | 5 | 1.00 |
| Aromatic 2 | 3 | 3 | 0.60 |

See `pharmacophore.json` (model), `features.csv` (raw points + cluster ids), and `raw_features_*.png` (per-family point distributions, each kept peak annotated with its label and support).