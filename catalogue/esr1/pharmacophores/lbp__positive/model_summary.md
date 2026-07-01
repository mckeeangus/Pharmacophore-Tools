# Pharmacophore — esr1/lbp__positive

- Ligands loaded: **16** (direct=1, template=15)
- Skipped poses: 0
- Consensus method: `kmeans`
- Representative ligand (viz): `7NFB_GEN_A601`
- Features kept: **5**

Support is the fraction of the cell's ligands that contribute to a feature (one row per feature / peak; all features are kept only above the support floor).

| Feature | Points | Ligands | Support |
|---|---:|---:|---:|
| Acceptor 1 | 9 | 9 | 0.56 |
| Donor 1 | 20 | 16 | 1.00 |
| Donor 2 | 15 | 13 | 0.81 |
| LumpedHydrophobe 1 | 18 | 16 | 1.00 |
| LumpedHydrophobe 2 | 11 | 10 | 0.62 |

See `pharmacophore.json` (model), `features.csv` (raw points + cluster ids), and `raw_features_*.png` (per-family point distributions, each kept peak annotated with its label and support).