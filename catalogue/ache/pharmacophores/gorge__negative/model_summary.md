# Pharmacophore — ache/gorge__negative

- Ligands loaded: **13** (direct=1, template=12)
- Skipped poses: 0
- Consensus method: `kmeans`
- Representative ligand (viz): `7D9O_H0L_B601`
- Features kept: **4**

Support is the fraction of the cell's ligands that contribute to a feature (one row per feature / peak; all features are kept only above the support floor).

| Feature | Points | Ligands | Support |
|---|---:|---:|---:|
| Acceptor 1 | 8 | 7 | 0.54 |
| Aromatic 1 | 14 | 10 | 0.77 |
| Aromatic 2 | 9 | 7 | 0.54 |
| Donor 1 | 11 | 10 | 0.77 |

See `pharmacophore.json` (model), `features.csv` (raw points + cluster ids), and `raw_features_*.png` (per-family point distributions, each kept peak annotated with its label and support).