# Pharmacophore — cavab/dhp_site__negative

- Ligands loaded: **3** (template=3)
- Skipped poses: 0
- Consensus method: `density`
- Representative ligand (viz): `5KLS_6UC_C1304`
- Features kept: **3**
- Excluded-volume spheres (receptor markers): **40**

Support is the fraction of the cell's ligands that contribute to a feature (one row per feature / peak; all features are kept only above the support floor).

| Feature | Points | Ligands | Support |
|---|---:|---:|---:|
| Aromatic 1 | 3 | 3 | 1.00 |
| Donor 1 | 3 | 3 | 1.00 |
| PosIonizable 1 | 2 | 2 | 0.67 |

## Feature resolution

Co-incident dual classifications collapsed by the feature hierarchy (higher-priority family kept on the shared atom); the listed ligands each carried both types on one atom.

| Kept ← dropped | Events | Ligands |
|---|---:|---|
| Aromatic ← LumpedHydrophobe | 3 | 5KLS_6UC_C1304, 5KMF_6U9_A1301, 6KE5_6UB_B1301 |
| PosIonizable ← Donor | 2 | 5KLS_6UC_C1304, 6KE5_6UB_B1301 |

See `pharmacophore.json` (model), `features.csv` (raw points + cluster ids), and `raw_features_*.png` (per-family point distributions, each kept peak annotated with its label and support).