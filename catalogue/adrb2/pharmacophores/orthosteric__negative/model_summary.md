# Pharmacophore — adrb2/orthosteric__negative

- Ligands loaded: **7** (direct=1, template=6)
- Skipped poses: 0
- Consensus method: `kmeans`
- Representative ligand (viz): `6PS3_CVD_A1201`
- Features kept: **4**

**Support** = fraction of the cell's ligands that contribute to a feature (≤ 1.0; features are kept only above the 0.5 support floor). **Occupancy** = points ÷ contributing ligands (points-per-ligand, uncapped: > 1.0 when a cluster is denser than one point per ligand). One row per feature / peak.

| Feature | Points | Ligands | Support | Occupancy |
|---|---:|---:|---:|---:|
| Acceptor 1 | 7 | 7 | 1.00 | 1.00 |
| Aromatic 1 | 14 | 7 | 1.00 | 2.00 |
| Donor 1 | 7 | 7 | 1.00 | 1.00 |
| PosIonizable 1 | 4 | 4 | 0.57 | 1.00 |

## Feature resolution

Co-incident dual classifications collapsed by the feature hierarchy (higher-priority family kept on the shared atom); the listed ligands each carried both types on one atom.

| Kept ← dropped | Events | Ligands |
|---|---:|---|
| Aromatic ← LumpedHydrophobe | 12 | 2RH1_CAU_A408, 3NY9_JSZ_A1203, 6PS3_CVD_A1201, 6PS4_JRZ_A1201, 6PS5_SNP_A1201, 9RKF_A1JHU_A520 |
| PosIonizable ← Donor | 7 | 2RH1_CAU_A408, 3NY9_JSZ_A1203, 6PS3_CVD_A1201, 6PS4_JRZ_A1201, 6PS5_SNP_A1201, 6PS6_TIM_A1201, 9RKF_A1JHU_A520 |

## Merged away

Clusters that passed the support/size floor but were displaced by the 1 Å cross-family overlap merge — one feature per region, keeping the denser one. Each row states in favour of which kept feature it was removed.

| Feature | Points | Ligands | Support | Occupancy | In favour of |
|---|---:|---:|---:|---:|---|
| Acceptor | 7 | 7 | 1.00 | 1.00 | Donor 1 |

## Below the support/size floor

Clusters that formed but never became candidates — below the 0.5 support floor or the minimum cluster size.

| Feature | Points | Ligands | Support | Occupancy |
|---|---:|---:|---:|---:|
| LumpedHydrophobe | 3 | 3 | 0.43 | 1.00 |
| LumpedHydrophobe | 3 | 3 | 0.43 | 1.00 |
| Acceptor | 3 | 2 | 0.29 | 1.50 |
| Donor | 2 | 2 | 0.29 | 1.00 |
| PosIonizable | 2 | 2 | 0.29 | 1.00 |
| Acceptor | 2 | 1 | 0.14 | 2.00 |
| Acceptor | 2 | 1 | 0.14 | 2.00 |
| Donor | 1 | 1 | 0.14 | 1.00 |
| Acceptor | 1 | 1 | 0.14 | 1.00 |
| PosIonizable | 1 | 1 | 0.14 | 1.00 |
| Aromatic | 1 | 1 | 0.14 | 1.00 |

See `pharmacophore.json` (model), `features.csv` (raw points + cluster ids), and `raw_features_*.png` (per-family point distributions, each kept peak annotated with its label and support).