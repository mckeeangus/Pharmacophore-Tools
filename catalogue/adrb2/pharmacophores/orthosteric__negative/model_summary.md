# Pharmacophore — adrb2/orthosteric__negative

- Ligands loaded: **7** (direct=1, template=6)
- Skipped poses: 0
- Consensus method: `kmeans`
- Representative ligand (viz): `6PS3_CVD_A1201`
- Features kept: **4**

Support is the fraction of the cell's ligands that contribute to a feature (one row per feature / peak; all features are kept only above the support floor).

| Feature | Points | Ligands | Support |
|---|---:|---:|---:|
| Acceptor 1 | 7 | 7 | 1.00 |
| Aromatic 1 | 14 | 7 | 1.00 |
| Donor 1 | 7 | 7 | 1.00 |
| PosIonizable 1 | 4 | 4 | 0.57 |

## Feature resolution

Co-incident dual classifications collapsed by the feature hierarchy (higher-priority family kept on the shared atom); the listed ligands each carried both types on one atom.

| Kept ← dropped | Events | Ligands |
|---|---:|---|
| Aromatic ← LumpedHydrophobe | 12 | 2RH1_CAU_A408, 3NY9_JSZ_A1203, 6PS3_CVD_A1201, 6PS4_JRZ_A1201, 6PS5_SNP_A1201, 9RKF_A1JHU_A520 |
| PosIonizable ← Donor | 7 | 2RH1_CAU_A408, 3NY9_JSZ_A1203, 6PS3_CVD_A1201, 6PS4_JRZ_A1201, 6PS5_SNP_A1201, 6PS6_TIM_A1201, 9RKF_A1JHU_A520 |

## Not selected

Clusters/peaks that formed but did not enter the model — below the support or size floor, or displaced by the cross-family overlap merge — with their mean support (fraction of the cell's ligands contributing).

| Feature | Points | Ligands | Mean support |
|---|---:|---:|---:|
| Acceptor | 7 | 7 | 1.00 |
| LumpedHydrophobe | 3 | 3 | 0.43 |
| LumpedHydrophobe | 3 | 3 | 0.43 |
| Acceptor | 3 | 2 | 0.29 |
| Donor | 2 | 2 | 0.29 |
| PosIonizable | 2 | 2 | 0.29 |
| Acceptor | 2 | 1 | 0.14 |
| Acceptor | 2 | 1 | 0.14 |
| Donor | 1 | 1 | 0.14 |
| Acceptor | 1 | 1 | 0.14 |
| PosIonizable | 1 | 1 | 0.14 |
| Aromatic | 1 | 1 | 0.14 |

See `pharmacophore.json` (model), `features.csv` (raw points + cluster ids), and `raw_features_*.png` (per-family point distributions, each kept peak annotated with its label and support).