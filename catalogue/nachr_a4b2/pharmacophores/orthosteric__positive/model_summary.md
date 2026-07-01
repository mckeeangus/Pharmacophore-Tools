# Pharmacophore — nachr_a4b2/orthosteric__positive

- Ligands loaded: **18** (direct=2, template=16)
- Skipped poses: 1 (3WTN_N2Y_H301:fail)
- Consensus method: `kmeans`
- Representative ligand (viz): `4FRR_0VC_F301`
- Features kept: **3**

Support is the fraction of the cell's ligands that contribute to a feature (one row per feature / peak; all features are kept only above the support floor).

| Feature | Points | Ligands | Support |
|---|---:|---:|---:|
| Acceptor 1 | 17 | 17 | 0.94 |
| Aromatic 1 | 14 | 14 | 0.78 |
| PosIonizable 1 | 15 | 15 | 0.83 |

See `pharmacophore.json` (model), `features.csv` (raw points + cluster ids), and `raw_features_*.png` (per-family point distributions, each kept peak annotated with its label and support).