# Pharmacophore — esr1/lbp__negative

- Ligands loaded: **42** (direct=11, template=31)
- Skipped poses: 0
- Consensus method: `kmeans`
- Representative ligand (viz): `7RS8_7EI_C601`
- Features kept: **6**

Support is the fraction of the cell's ligands that contribute to a feature (one row per feature / peak; all features are kept only above the support floor).

| Feature | Points | Ligands | Support |
|---|---:|---:|---:|
| Acceptor 1 | 79 | 36 | 0.86 |
| Acceptor 2 | 38 | 35 | 0.83 |
| Acceptor 3 | 36 | 32 | 0.76 |
| Aromatic 1 | 44 | 42 | 1.00 |
| Aromatic 2 | 42 | 42 | 1.00 |
| PosIonizable 1 | 27 | 27 | 0.64 |

See `pharmacophore.json` (model), `features.csv` (raw points + cluster ids), and `raw_features_*.png` (per-family point distributions, each kept peak annotated with its label and support).