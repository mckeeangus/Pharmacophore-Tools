# Pharmacophore — nav1_7_pore/pore_site__negative

- Ligands loaded: **5** (template=5)
- Skipped poses: 0
- Consensus method: `density`
- Representative ligand (viz): `8THH_IYJ_A2004`
- Features kept: **2**
- Excluded-volume spheres (receptor markers): **40**

Support is the fraction of the cell's ligands that contribute to a feature (one row per feature / peak; all features are kept only above the support floor).

| Feature | Points | Ligands | Support |
|---|---:|---:|---:|
| Acceptor 1 | 8 | 5 | 1.00 |
| Aromatic 1 | 3 | 3 | 0.60 |

## Feature resolution

Co-incident dual classifications collapsed by the feature hierarchy (higher-priority family kept on the shared atom); the listed ligands each carried both types on one atom.

| Kept ← dropped | Events | Ligands |
|---|---:|---|
| Aromatic ← LumpedHydrophobe | 5 | 8I5B_OJ0_A2021, 8S9B_LQO_A2003, 8S9C_N6W_A2003, 8THH_IYJ_A2004 |
| PosIonizable ← Donor | 1 | 8I5B_OJ0_A2021 |

See `pharmacophore.json` (model), `features.csv` (raw points + cluster ids), and `raw_features_*.png` (per-family point distributions, each kept peak annotated with its label and support).