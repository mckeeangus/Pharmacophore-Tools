# Pharmacophore — ache/gorge__negative

- Ligands loaded: **13** (direct=1, template=12)
- Skipped poses: 0
- Consensus method: `density`
- Representative ligand (viz): `7D9O_H0L_B601`
- Features kept: **3**
- Excluded-volume spheres (receptor markers): **40**

Support is the fraction of the cell's ligands that contribute to a feature (one row per feature / peak; all features are kept only above the support floor).

| Feature | Points | Ligands | Support |
|---|---:|---:|---:|
| Acceptor 1 | 13 | 7 | 0.54 |
| Aromatic 1 | 14 | 10 | 0.77 |
| Aromatic 2 | 9 | 7 | 0.54 |

## Feature resolution

Co-incident dual classifications collapsed by the feature hierarchy (higher-priority family kept on the shared atom); the listed ligands each carried both types on one atom.

| Kept ← dropped | Events | Ligands |
|---|---:|---|
| Aromatic ← LumpedHydrophobe | 20 | 4BDT_HUW_A701, 4EY6_GNT_A604, 4M0E_1YL_B605, 4M0F_1YK_B605, 6O4W_E20_A604, 6O4X_AA_B603, 6O50_EBW_A601, 7D9O_H0L_B601, 7D9P_H0R_A601, 7D9Q_H1R_B601, 7XN1_THA_A601 |
| PosIonizable ← Donor | 6 | 4EY5_HUP_A604, 4EY6_GNT_A604, 6O4W_E20_A604, 7D9O_H0L_B601, 7D9P_H0R_A601, 7D9Q_H1R_B601 |

## Not selected

Clusters/peaks that formed but did not enter the model — below the support or size floor, or displaced by the cross-family overlap merge — with their mean support (fraction of the cell's ligands contributing).

| Feature | Points | Ligands | Mean support |
|---|---:|---:|---:|
| PosIonizable | 11 | 11 | 0.85 |
| Acceptor | 12 | 6 | 0.46 |
| Acceptor | 7 | 4 | 0.31 |
| Donor | 4 | 3 | 0.23 |
| Donor | 3 | 3 | 0.23 |
| Acceptor | 3 | 3 | 0.23 |
| Donor | 1 | 1 | 0.08 |
| PosIonizable | 1 | 1 | 0.08 |

See `pharmacophore.json` (model), `features.csv` (raw points + cluster ids), and `raw_features_*.png` (per-family point distributions, each kept peak annotated with its label and support).