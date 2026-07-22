# Pharmacophore — adrb2/orthosteric__negative

- Ligands loaded: **7** (direct=1, template=6)
- Skipped poses: 0
- Consensus method: `density`
- Representative ligand (viz): `2RH1_CAU_A408`
- Features kept: **5**
- Excluded-volume spheres (receptor markers): **40**

**Support** = fraction of the cell's ligands that contribute to a feature (≤ 1.0; features are kept only above the 0.5 support floor). **Occupancy** = points ÷ contributing ligands (points-per-ligand, uncapped: > 1.0 when a cluster is denser than one point per ligand). One row per feature / peak.

| Feature | Points | Ligands | Support | Occupancy |
|---|---:|---:|---:|---:|
| Acceptor 1 | 7 | 7 | 1.00 | 1.00 |
| Aromatic 1 | 9 | 6 | 0.86 | 1.50 |
| Donor 1 | 7 | 7 | 1.00 | 1.00 |
| LumpedHydrophobe 1 | 6 | 6 | 0.86 | 1.00 |
| PosIonizable 1 | 7 | 7 | 1.00 | 1.00 |

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
| Donor | 2 | 2 | 0.29 | 1.00 |
| Acceptor | 2 | 2 | 0.29 | 1.00 |
| Donor | 1 | 1 | 0.14 | 1.00 |
| Acceptor | 1 | 1 | 0.14 | 1.00 |
| Aromatic | 1 | 1 | 0.14 | 1.00 |
| Acceptor | 0 | 0 | 0.00 | 0.00 |

See `pharmacophore.json` (model), `features.csv` (raw points + cluster ids), and `raw_features_*.png` (per-family point distributions, each kept peak annotated with its label and support).