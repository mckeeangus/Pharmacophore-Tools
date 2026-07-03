# Pharmacophore — esr1/lbp__positive

- Ligands loaded: **16** (direct=1, template=15)
- Skipped poses: 0
- Consensus method: `kmeans`
- Representative ligand (viz): `9W12_A1ET8_A701`
- Features kept: **4**

Support is the fraction of the cell's ligands that contribute to a feature (one row per feature / peak; all features are kept only above the support floor).

| Feature | Points | Ligands | Support |
|---|---:|---:|---:|
| Acceptor 1 | 9 | 9 | 0.56 |
| Aromatic 1 | 17 | 16 | 1.00 |
| Donor 1 | 20 | 16 | 1.00 |
| Donor 2 | 15 | 13 | 0.81 |

## Feature resolution

Co-incident dual classifications collapsed by the feature hierarchy (higher-priority family kept on the shared atom); the listed ligands each carried both types on one atom.

| Kept ← dropped | Events | Ligands |
|---|---:|---|
| Aromatic ← LumpedHydrophobe | 26 | 2B1V_458_B202, 2B1Z_17M_B202, 2QAB_EI1_B1, 2QSE_1HP_B1, 2QZO_KN1_B1, 4MG8_27J_A601, 4MGA_27L_B601, 4MGB_XDH_B601, 4TV1_36M_A601, 5TN4_7FZ_A601, 5TN5_7G0_B601, 7NEL_EST_A601, 7NFB_GEN_A601, 7RKE_5VP_B601, 9W11_ZHB_A701, 9W12_A1ET8_A701 |

See `pharmacophore.json` (model), `features.csv` (raw points + cluster ids), and `raw_features_*.png` (per-family point distributions, each kept peak annotated with its label and support).