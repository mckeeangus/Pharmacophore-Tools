# Pharmacophore — cavab/dhp_site__negative

- Ligands loaded: **3** (template=3)
- Skipped poses: 0
- Consensus method: `kmeans`
- Representative ligand (viz): `5KLS_6UC_C1304`
- Features kept: **4**

Support is the fraction of the cell's ligands that contribute to a feature (one row per feature / peak; all features are kept only above the support floor).

| Feature | Points | Ligands | Support |
|---|---:|---:|---:|
| Acceptor 1 | 6 | 3 | 1.00 |
| Donor 1 | 3 | 3 | 1.00 |
| Donor 2 | 2 | 2 | 0.67 |
| LumpedHydrophobe 1 | 4 | 3 | 1.00 |

See `pharmacophore.json` (model), `features.csv` (raw points + cluster ids), and `raw_features_*.png` (per-family point distributions, each kept peak annotated with its label and support).