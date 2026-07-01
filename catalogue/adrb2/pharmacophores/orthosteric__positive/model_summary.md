# Pharmacophore — adrb2/orthosteric__positive

- Ligands loaded: **11** (direct=1, template=10)
- Skipped poses: 0
- Consensus method: `kmeans`
- Representative ligand (viz): `4LDL_XQC_A1401`
- Features kept: **5**

Support is the fraction of the cell's ligands that contribute to a feature (one row per feature / peak; all features are kept only above the support floor).

| Feature | Points | Ligands | Support |
|---|---:|---:|---:|
| Aromatic 1 | 11 | 11 | 1.00 |
| Donor 1 | 11 | 11 | 1.00 |
| Donor 2 | 11 | 11 | 1.00 |
| Donor 3 | 11 | 11 | 1.00 |
| Donor 4 | 10 | 10 | 0.91 |

See `pharmacophore.json` (model), `features.csv` (raw points + cluster ids), and `raw_features_*.png` (per-family point distributions, each kept peak annotated with its label and support).