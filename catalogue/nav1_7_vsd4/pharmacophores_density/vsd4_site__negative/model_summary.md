# Pharmacophore — nav1_7_vsd4/vsd4_site__negative

- Ligands loaded: **3** (template=3)
- Skipped poses: 0
- Consensus method: `density`
- Representative ligand (viz): `8F0P_X7L_A1610`
- Features kept: **2**
- Excluded-volume spheres (receptor markers): **40**

Support is the fraction of the cell's ligands that contribute to a feature (one row per feature / peak; all features are kept only above the support floor).

| Feature | Points | Ligands | Support |
|---|---:|---:|---:|
| Donor 1 | 3 | 3 | 1.00 |
| LumpedHydrophobe 1 | 2 | 2 | 0.67 |

## Feature resolution

Co-incident dual classifications collapsed by the feature hierarchy (higher-priority family kept on the shared atom); the listed ligands each carried both types on one atom.

| Kept ← dropped | Events | Ligands |
|---|---:|---|
| Aromatic ← LumpedHydrophobe | 6 | 8F0P_X7L_A1610, 8F0R_X7W_A1606, 8F0S_X80_A1605 |
| PosIonizable ← Donor | 3 | 8F0P_X7L_A1610, 8F0R_X7W_A1606, 8F0S_X80_A1605 |

See `pharmacophore.json` (model), `features.csv` (raw points + cluster ids), and `raw_features_*.png` (per-family point distributions, each kept peak annotated with its label and support).