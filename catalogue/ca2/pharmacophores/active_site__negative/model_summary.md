# Pharmacophore — ca2/active_site__negative

- Ligands loaded: **76** (direct=13, template=63)
- Skipped poses: 0
- Consensus method: `density`
- Representative ligand (viz): `5DRS_5EF_A305`
- Features kept: **4**
- Excluded-volume spheres (receptor markers): **40**

**Support** = fraction of the cell's ligands that contribute to a feature (≤ 1.0; features are kept only above the 0.5 support floor). **Occupancy** = points ÷ contributing ligands (points-per-ligand, uncapped: > 1.0 when a cluster is denser than one point per ligand). One row per feature / peak.

| Feature | Points | Ligands | Support | Occupancy |
|---|---:|---:|---:|---:|
| Acceptor 1 | 71 | 71 | 0.93 | 1.00 |
| Aromatic 1 | 57 | 57 | 0.75 | 1.00 |
| Donor 1 | 57 | 57 | 0.75 | 1.00 |
| LumpedHydrophobe 1 | 54 | 54 | 0.71 | 1.00 |

## Feature resolution

Co-incident dual classifications collapsed by the feature hierarchy (higher-priority family kept on the shared atom); the listed ligands each carried both types on one atom.

| Kept ← dropped | Events | Ligands |
|---|---:|---|
| NegIonizable ← Acceptor | 5 | 2NNO_M28_A301, 5M78_SAL_A304, 6RFH_4SO_A305, 8QFK_UII_AAA301, 8QH8_V8I_A302 |
| PosIonizable ← Donor | 23 | 2NNO_M28_A301, 2NNS_M25_A301, 4FPT_0VZ_A303, 4FRC_0VY_A303, 4FU5_0VX_A303, 4FVN_0VW_A303, 4Q08_V90_A305, 5DRS_5EF_A305, 6G3Q_FO9_A302, 6SBL_L4Q_A306, 6SDI_0VV_A305, 6SDJ_J3K_A302, 8QFK_UII_AAA301 |

## Below the support/size floor

Clusters that formed but never became candidates — below the 0.5 support floor or the minimum cluster size.

| Feature | Points | Ligands | Support | Occupancy |
|---|---:|---:|---:|---:|
| Acceptor | 14 | 14 | 0.18 | 1.00 |
| PosIonizable | 7 | 7 | 0.09 | 1.00 |
| Donor | 7 | 7 | 0.09 | 1.00 |
| PosIonizable | 3 | 2 | 0.03 | 1.50 |
| NegIonizable | 2 | 2 | 0.03 | 1.00 |
| Aromatic | 1 | 1 | 0.01 | 1.00 |
| LumpedHydrophobe | 1 | 1 | 0.01 | 1.00 |
| NegIonizable | 1 | 1 | 0.01 | 1.00 |
| NegIonizable | 1 | 1 | 0.01 | 1.00 |
| NegIonizable | 1 | 1 | 0.01 | 1.00 |

See `pharmacophore.json` (model), `features.csv` (raw points + cluster ids), and `raw_features_*.png` (per-family point distributions, each kept peak annotated with its label and support).