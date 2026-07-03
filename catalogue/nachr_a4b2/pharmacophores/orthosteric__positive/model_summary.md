# Pharmacophore — nachr_a4b2/orthosteric__positive

- Ligands loaded: **18** (direct=2, template=16)
- Skipped poses: 1 (3WTN_N2Y_H301:fail)
- Consensus method: `kmeans`
- Representative ligand (viz): `4FRR_0VC_F301`
- Features kept: **3**

Support is the fraction of the cell's ligands that contribute to a feature (one row per feature / peak; all features are kept only above the support floor).

| Feature | Points | Ligands | Support |
|---|---:|---:|---:|
| Acceptor 1 | 17 | 17 | 0.94 |
| Aromatic 1 | 14 | 14 | 0.78 |
| PosIonizable 1 | 15 | 15 | 0.83 |

## Feature resolution

Co-incident dual classifications collapsed by the feature hierarchy (higher-priority family kept on the shared atom); the listed ligands each carried both types on one atom.

| Kept ← dropped | Events | Ligands |
|---|---:|---|
| Aromatic ← LumpedHydrophobe | 1 | 3U8L_09Q_J211 |
| PosIonizable ← Donor | 13 | 3U8J_09O_A211, 3U8K_09P_F211, 3U8L_09Q_J211, 3U8M_09R_L211, 3U8N_09S_Q211, 3ZDG_XRX_I301, 3ZDH_XRS_A301, 4FRR_0VC_F301, 4ZJS_4P0_D301, 5BP0_FN1_D302, 5O87_NCT_A601, 5SYO_C5E_E301, 6SGV_LDQ_G601 |

See `pharmacophore.json` (model), `features.csv` (raw points + cluster ids), and `raw_features_*.png` (per-family point distributions, each kept peak annotated with its label and support).