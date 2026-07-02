# Pharmacophore — adora2a/orthosteric__negative

- Ligands loaded: **25** (template=25)
- Skipped poses: 3 (5UIG_8D1_A503:fail, 7PX4_8E2_A2404:fail, 7PYR_8IM_A2404:fail)
- Consensus method: `density`
- Representative ligand (viz): `3REY_XAC_A999`
- Features kept: **2**
- Excluded-volume spheres (receptor markers): **40**

Support is the fraction of the cell's ligands that contribute to a feature (one row per feature / peak; all features are kept only above the support floor).

| Feature | Points | Ligands | Support |
|---|---:|---:|---:|
| Acceptor 1 | 87 | 25 | 1.00 |
| Acceptor 2 | 22 | 13 | 0.52 |

See `pharmacophore.json` (model), `features.csv` (raw points + cluster ids), and `raw_features_*.png` (per-family point distributions, each kept peak annotated with its label and support).