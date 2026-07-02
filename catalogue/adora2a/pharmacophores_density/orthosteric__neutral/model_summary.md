# Pharmacophore — adora2a/orthosteric__neutral

- Ligands loaded: **5** (template=5)
- Skipped poses: 0
- Consensus method: `density`
- Representative ligand (viz): `8CIC_U30_A1202`
- Features kept: **3**
- Excluded-volume spheres (receptor markers): **40**

Support is the fraction of the cell's ligands that contribute to a feature (one row per feature / peak; all features are kept only above the support floor).

| Feature | Points | Ligands | Support |
|---|---:|---:|---:|
| Acceptor 1 | 20 | 5 | 1.00 |
| Donor 1 | 6 | 4 | 0.80 |
| LumpedHydrophobe 1 | 3 | 3 | 0.60 |

See `pharmacophore.json` (model), `features.csv` (raw points + cluster ids), and `raw_features_*.png` (per-family point distributions, each kept peak annotated with its label and support).