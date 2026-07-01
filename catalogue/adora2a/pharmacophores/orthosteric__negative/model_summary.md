# Pharmacophore — adora2a/orthosteric__negative

- Ligands loaded: **25** (template=25)
- Skipped poses: 3 (5UIG_8D1_A503:fail, 7PX4_8E2_A2404:fail, 7PYR_8IM_A2404:fail)
- Consensus method: `kmeans`
- Representative ligand (viz): `8JWY_VBF_A1201`
- Features kept: **3**

Support is the fraction of the cell's ligands that contribute to a feature (one row per feature / peak; all features are kept only above the support floor).

| Feature | Points | Ligands | Support |
|---|---:|---:|---:|
| Acceptor 1 | 86 | 25 | 1.00 |
| Acceptor 2 | 24 | 14 | 0.56 |
| Donor 1 | 19 | 18 | 0.72 |

See `pharmacophore.json` (model), `features.csv` (raw points + cluster ids), and `raw_features_*.png` (per-family point distributions, each kept peak annotated with its label and support).