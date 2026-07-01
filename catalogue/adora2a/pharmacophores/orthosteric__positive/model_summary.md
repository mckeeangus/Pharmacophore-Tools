# Pharmacophore — adora2a/orthosteric__positive

- Ligands loaded: **6** (template=6)
- Skipped poses: 1 (8RLN_A1H1S_A1211:fail)
- Consensus method: `kmeans`
- Representative ligand (viz): `4UHR_NGI_A1320`
- Features kept: **9**

Support is the fraction of the cell's ligands that contribute to a feature (one row per feature / peak; all features are kept only above the support floor).

| Feature | Points | Ligands | Support |
|---|---:|---:|---:|
| Acceptor 1 | 11 | 6 | 1.00 |
| Acceptor 2 | 10 | 5 | 0.83 |
| Acceptor 3 | 6 | 5 | 0.83 |
| Acceptor 4 | 5 | 5 | 0.83 |
| Acceptor 5 | 4 | 4 | 0.67 |
| Aromatic 1 | 12 | 6 | 1.00 |
| Aromatic 2 | 4 | 4 | 0.67 |
| Donor 1 | 6 | 6 | 1.00 |
| Donor 2 | 5 | 5 | 0.83 |

See `pharmacophore.json` (model), `features.csv` (raw points + cluster ids), and `raw_features_*.png` (per-family point distributions, each kept peak annotated with its label and support).