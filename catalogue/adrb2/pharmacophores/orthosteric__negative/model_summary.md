# Pharmacophore — adrb2/orthosteric__negative

- Ligands loaded: **7** (direct=1, template=6)
- Skipped poses: 0
- Consensus method: `kmeans`
- Representative ligand (viz): `2RH1_CAU_A408`
- Features kept: **6**

Support is the fraction of the cell's ligands that contribute to a feature (one row per feature / peak; all features are kept only above the support floor).

| Feature | Points | Ligands | Support |
|---|---:|---:|---:|
| Acceptor 1 | 7 | 7 | 1.00 |
| Aromatic 1 | 14 | 7 | 1.00 |
| Donor 1 | 7 | 7 | 1.00 |
| Donor 2 | 7 | 7 | 1.00 |
| LumpedHydrophobe 1 | 7 | 7 | 1.00 |
| LumpedHydrophobe 2 | 5 | 5 | 0.71 |

See `pharmacophore.json` (model), `features.csv` (raw points + cluster ids), and `raw_features_*.png` (per-family point distributions, each kept peak annotated with its label and support).