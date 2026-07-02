# Pharmacophore — esr1/lbp__negative

- Ligands loaded: **42** (direct=11, template=31)
- Skipped poses: 0
- Consensus method: `density`
- Representative ligand (viz): `7NDO_RAL_B601`
- Features kept: **5**
- Excluded-volume spheres (receptor markers): **40**

Support is the fraction of the cell's ligands that contribute to a feature (one row per feature / peak; all features are kept only above the support floor).

| Feature | Points | Ligands | Support |
|---|---:|---:|---:|
| Acceptor 1 | 52 | 27 | 0.64 |
| Acceptor 2 | 31 | 31 | 0.74 |
| Aromatic 1 | 48 | 42 | 1.00 |
| LumpedHydrophobe 1 | 48 | 42 | 1.00 |
| PosIonizable 1 | 27 | 27 | 0.64 |

See `pharmacophore.json` (model), `features.csv` (raw points + cluster ids), and `raw_features_*.png` (per-family point distributions, each kept peak annotated with its label and support).