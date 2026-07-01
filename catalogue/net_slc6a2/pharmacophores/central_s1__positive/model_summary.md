# Pharmacophore — net_slc6a2/central_s1__positive

- Ligands loaded: **6** (direct=3, template=3)
- Skipped poses: 0
- Consensus method: `kmeans`
- Representative ligand (viz): `8WTV_E5E_A704`
- Features kept: **3**

Support is the fraction of the cell's ligands that contribute to a feature (one row per feature / peak; all features are kept only above the support floor).

| Feature | Points | Ligands | Support |
|---|---:|---:|---:|
| Aromatic 1 | 4 | 4 | 0.67 |
| Donor 1 | 7 | 5 | 0.83 |
| Donor 2 | 6 | 3 | 0.50 |

See `pharmacophore.json` (model), `features.csv` (raw points + cluster ids), and `raw_features_*.png` (per-family point distributions, each kept peak annotated with its label and support).