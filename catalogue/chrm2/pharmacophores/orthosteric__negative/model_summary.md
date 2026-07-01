# Pharmacophore — chrm2/orthosteric__negative

- Ligands loaded: **3** (template=3)
- Skipped poses: 0
- Consensus method: `kmeans`
- Representative ligand (viz): `5ZK3_QNB_A501`
- Features kept: **5**

Support is the fraction of the cell's ligands that contribute to a feature (one row per feature / peak; all features are kept only above the support floor).

| Feature | Points | Ligands | Support |
|---|---:|---:|---:|
| Acceptor 1 | 5 | 3 | 1.00 |
| Acceptor 2 | 3 | 2 | 0.67 |
| Aromatic 1 | 3 | 3 | 1.00 |
| Aromatic 2 | 2 | 2 | 0.67 |
| Donor 1 | 4 | 2 | 0.67 |

See `pharmacophore.json` (model), `features.csv` (raw points + cluster ids), and `raw_features_*.png` (per-family point distributions, each kept peak annotated with its label and support).