# Pharmacophore — cox2/cox_channel__negative

- Ligands loaded: **5** (template=5)
- Skipped poses: 0
- Consensus method: `kmeans`
- Representative ligand (viz): `5IKR_ID8_A601`
- Features kept: **4**

Support is the fraction of the cell's ligands that contribute to a feature (one row per feature / peak; all features are kept only above the support floor).

| Feature | Points | Ligands | Support |
|---|---:|---:|---:|
| Aromatic 1 | 5 | 5 | 1.00 |
| Aromatic 2 | 3 | 3 | 0.60 |
| Donor 1 | 3 | 3 | 0.60 |
| NegIonizable 1 | 3 | 3 | 0.60 |

## Feature resolution

Co-incident dual classifications collapsed by the feature hierarchy (higher-priority family kept on the shared atom); the listed ligands each carried both types on one atom.

| Kept ← dropped | Events | Ligands |
|---|---:|---|
| Aromatic ← LumpedHydrophobe | 9 | 5F1A_SAL_A601, 5IKR_ID8_A601, 5IKT_TLF_B601, 5IKV_FLF_B601, 5KIR_RCX_A601 |
| NegIonizable ← Acceptor | 4 | 5F1A_SAL_A601, 5IKR_ID8_A601, 5IKT_TLF_B601, 5IKV_FLF_B601 |

See `pharmacophore.json` (model), `features.csv` (raw points + cluster ids), and `raw_features_*.png` (per-family point distributions, each kept peak annotated with its label and support).