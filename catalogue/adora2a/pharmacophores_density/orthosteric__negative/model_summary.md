# Pharmacophore — adora2a/orthosteric__negative

- Ligands loaded: **25** (template=25)
- Skipped poses: 3 (5UIG_8D1_A503:fail, 7PX4_8E2_A2404:fail, 7PYR_8IM_A2404:fail)
- Consensus method: `density`
- Representative ligand (viz): `8JWY_VBF_A1201`
- Features kept: **3**
- Excluded-volume spheres (receptor markers): **40**

**Support** = fraction of the cell's ligands that contribute to a feature (≤ 1.0; features are kept only above the 0.5 support floor). **Occupancy** = points ÷ contributing ligands (points-per-ligand, uncapped: > 1.0 when a cluster is denser than one point per ligand). One row per feature / peak.

| Feature | Points | Ligands | Support | Occupancy |
|---|---:|---:|---:|---:|
| Acceptor 1 | 87 | 25 | 1.00 | 3.48 |
| Acceptor 2 | 22 | 13 | 0.52 | 1.69 |
| Donor 1 | 14 | 14 | 0.56 | 1.00 |

## Feature resolution

Co-incident dual classifications collapsed by the feature hierarchy (higher-priority family kept on the shared atom); the listed ligands each carried both types on one atom.

| Kept ← dropped | Events | Ligands |
|---|---:|---|
| Aromatic ← LumpedHydrophobe | 19 | 10KT_A1C5S_A1202, 3REY_XAC_A999, 3UZA_T4G_A330, 5IU7_6DY_A2401, 5IUA_6DX_A2401, 5IUB_6DV_A2401, 5NM4_ZMA_A507, 5OLZ_T4E_A1201, 6ZDR_QGE_A1201, 6ZDV_QGW_A1201, 8CU7_LJX_A1202, 8DU3_TKO_A3001, 8JWY_VBF_A1201, 8RW4_A1H3L_A1201, 8RW7_A1H3J_A1201, 8RWC_A1H3I_A1201, 8RWD_A1H3H_A1201, 8RWE_A1H3K_A1201 |
| PosIonizable ← Donor | 17 | 3REY_XAC_A999, 5IU7_6DY_A2401, 5IU8_6DZ_A2401, 5IUA_6DX_A2401, 5IUB_6DV_A2401, 5N2R_8JN_A2401, 7IO5_TEP_A1202, 8RW4_A1H3L_A1201, 8RW7_A1H3J_A1201 |

## Merged away

Clusters that passed the support/size floor but were displaced by the 1 Å cross-family overlap merge — one feature per region, keeping the denser one. Each row states in favour of which kept feature it was removed.

| Feature | Points | Ligands | Support | Occupancy | In favour of |
|---|---:|---:|---:|---:|---|
| Aromatic | 66 | 25 | 1.00 | 2.64 | Acceptor 1 |

## Below the support/size floor

Clusters that formed but never became candidates — below the 0.5 support floor or the minimum cluster size.

| Feature | Points | Ligands | Support | Occupancy |
|---|---:|---:|---:|---:|
| Aromatic | 11 | 11 | 0.44 | 1.00 |
| PosIonizable | 10 | 10 | 0.40 | 1.00 |
| Donor | 7 | 7 | 0.28 | 1.00 |
| PosIonizable | 6 | 5 | 0.20 | 1.20 |
| Donor | 5 | 4 | 0.16 | 1.25 |
| Aromatic | 3 | 3 | 0.12 | 1.00 |
| Donor | 3 | 2 | 0.08 | 1.50 |
| LumpedHydrophobe | 4 | 1 | 0.04 | 4.00 |
| Acceptor | 1 | 1 | 0.04 | 1.00 |
| PosIonizable | 1 | 1 | 0.04 | 1.00 |
| PosIonizable | 1 | 1 | 0.04 | 1.00 |

See `pharmacophore.json` (model), `features.csv` (raw points + cluster ids), and `raw_features_*.png` (per-family point distributions, each kept peak annotated with its label and support).