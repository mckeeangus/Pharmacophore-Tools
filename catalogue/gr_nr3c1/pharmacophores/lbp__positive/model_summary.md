# Pharmacophore — gr_nr3c1/lbp__positive

- Ligands loaded: **20** (direct=1, template=19)
- Skipped poses: 0
- Consensus method: `kmeans`
- Representative ligand (viz): `7PRX_82H_A801`
- Features kept: **3**

Support is the fraction of the cell's ligands that contribute to a feature (one row per feature / peak; all features are kept only above the support floor).

| Feature | Points | Ligands | Support |
|---|---:|---:|---:|
| Acceptor 1 | 69 | 20 | 1.00 |
| Acceptor 2 | 33 | 19 | 0.95 |
| Aromatic 1 | 24 | 13 | 0.65 |

See `pharmacophore.json` (model), `features.csv` (raw points + cluster ids), and `raw_features_*.png` (per-family point distributions, each kept peak annotated with its label and support).