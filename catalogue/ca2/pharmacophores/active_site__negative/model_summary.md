# Pharmacophore — ca2/active_site__negative

- Ligands loaded: **76** (direct=13, template=63)
- Skipped poses: 0
- Consensus method: `kmeans`
- Representative ligand (viz): `5DRS_5EF_A305`
- Features kept: **4**

Support is the fraction of the cell's ligands that contribute to a feature (one row per feature / peak; all features are kept only above the support floor).

| Feature | Points | Ligands | Support |
|---|---:|---:|---:|
| Acceptor 1 | 74 | 73 | 0.96 |
| Acceptor 2 | 72 | 72 | 0.95 |
| Aromatic 1 | 62 | 59 | 0.78 |
| Donor 1 | 74 | 61 | 0.80 |

See `pharmacophore.json` (model), `features.csv` (raw points + cluster ids), and `raw_features_*.png` (per-family point distributions, each kept peak annotated with its label and support).