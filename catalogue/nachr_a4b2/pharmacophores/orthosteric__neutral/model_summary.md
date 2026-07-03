# Pharmacophore — nachr_a4b2/orthosteric__neutral

- Ligands loaded: **9** (template=9)
- Skipped poses: 0
- Consensus method: `kmeans`
- Representative ligand (viz): `2XYT_TC9_F1206`
- Features kept: **2**

Support is the fraction of the cell's ligands that contribute to a feature (one row per feature / peak; all features are kept only above the support floor).

| Feature | Points | Ligands | Support |
|---|---:|---:|---:|
| Acceptor 1 | 24 | 9 | 1.00 |
| Acceptor 2 | 13 | 6 | 0.67 |

## Feature resolution

Co-incident dual classifications collapsed by the feature hierarchy (higher-priority family kept on the shared atom); the listed ligands each carried both types on one atom.

| Kept ← dropped | Events | Ligands |
|---|---:|---|
| Aromatic ← LumpedHydrophobe | 8 | 2WNC_TKT_C300, 2XYS_SY9_E1206, 2XYT_TC9_F1206, 3SIO_MLK_D260, 9SG3_PHN_A302 |
| PosIonizable ← Donor | 4 | 2WNC_TKT_C300, 2XYS_SY9_E1206, 2XYT_TC9_F1206, 3SIO_MLK_D260 |

## Not selected

Clusters/peaks that formed but did not enter the model — below the support or size floor, or displaced by the cross-family overlap merge — with their mean support (fraction of the cell's ligands contributing).

| Feature | Points | Ligands | Mean support |
|---|---:|---:|---:|
| Donor | 6 | 5 | 0.56 |
| Aromatic | 8 | 4 | 0.44 |
| PosIonizable | 4 | 4 | 0.44 |
| Aromatic | 3 | 2 | 0.22 |
| Donor | 1 | 1 | 0.11 |
| Donor | 1 | 1 | 0.11 |
| PosIonizable | 1 | 1 | 0.11 |

See `pharmacophore.json` (model), `features.csv` (raw points + cluster ids), and `raw_features_*.png` (per-family point distributions, each kept peak annotated with its label and support).