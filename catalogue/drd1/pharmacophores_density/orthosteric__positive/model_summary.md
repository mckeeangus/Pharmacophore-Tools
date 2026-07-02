# Pharmacophore — drd1/orthosteric__positive

- Ligands loaded: **16** (direct=1, template=15)
- Skipped poses: 0
- Consensus method: `density`
- Representative ligand (viz): `7X2C_G3C_F503`
- Features kept: **3**
- Excluded-volume spheres (receptor markers): **40**

Support is the fraction of the cell's ligands that contribute to a feature (one row per feature / peak; all features are kept only above the support floor).

| Feature | Points | Ligands | Support |
|---|---:|---:|---:|
| Acceptor 1 | 27 | 15 | 0.94 |
| Aromatic 1 | 19 | 12 | 0.75 |
| PosIonizable 1 | 11 | 11 | 0.69 |

See `pharmacophore.json` (model), `features.csv` (raw points + cluster ids), and `raw_features_*.png` (per-family point distributions, each kept peak annotated with its label and support).