# Pharmacophore — esr1/lbp__positive

- Ligands loaded: **16** (direct=1, template=15)
- Skipped poses: 0
- Consensus method: `density`
- Representative ligand (viz): `7NFB_GEN_A601`
- Features kept: **3**
- Excluded-volume spheres (receptor markers): **40**

Support is the fraction of the cell's ligands that contribute to a feature (one row per feature / peak; all features are kept only above the support floor).

| Feature | Points | Ligands | Support |
|---|---:|---:|---:|
| Aromatic 1 | 30 | 16 | 1.00 |
| Donor 1 | 20 | 16 | 1.00 |
| Donor 2 | 15 | 13 | 0.81 |

See `pharmacophore.json` (model), `features.csv` (raw points + cluster ids), and `raw_features_*.png` (per-family point distributions, each kept peak annotated with its label and support).