# Pharmacophore — gaba_a/bzd_site__positive

- Ligands loaded: **3** (template=3)
- Skipped poses: 0
- Consensus method: `kmeans`
- Representative ligand (viz): `6HUO_08H_D501`
- Features kept: **4**

Support is the fraction of the cell's ligands that contribute to a feature (one row per feature / peak; all features are kept only above the support floor).

| Feature | Points | Ligands | Support |
|---|---:|---:|---:|
| Acceptor 1 | 3 | 2 | 0.67 |
| Aromatic 1 | 4 | 3 | 1.00 |
| Aromatic 2 | 2 | 2 | 0.67 |
| Aromatic 3 | 2 | 2 | 0.67 |

## Feature resolution

Co-incident dual classifications collapsed by the feature hierarchy (higher-priority family kept on the shared atom); the listed ligands each carried both types on one atom.

| Kept ← dropped | Events | Ligands |
|---|---:|---|
| Aromatic ← LumpedHydrophobe | 6 | 6HUO_08H_D501, 6X3X_DZP_D404, 8VQY_A1ADG_E401 |

See `pharmacophore.json` (model), `features.csv` (raw points + cluster ids), and `raw_features_*.png` (per-family point distributions, each kept peak annotated with its label and support).