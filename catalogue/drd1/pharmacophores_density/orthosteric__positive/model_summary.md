# Pharmacophore — drd1/orthosteric__positive

- Ligands loaded: **16** (direct=1, template=15)
- Skipped poses: 0
- Consensus method: `density`
- Representative ligand (viz): `7X2C_G3C_F503`
- Features kept: **4**
- Excluded-volume spheres (receptor markers): **40**

**Support** = fraction of the cell's ligands that contribute to a feature (≤ 1.0; features are kept only above the 0.5 support floor). **Occupancy** = points ÷ contributing ligands (points-per-ligand, uncapped: > 1.0 when a cluster is denser than one point per ligand). One row per feature / peak.

| Feature | Points | Ligands | Support | Occupancy |
|---|---:|---:|---:|---:|
| Acceptor 1 | 27 | 15 | 0.94 | 1.80 |
| Aromatic 1 | 21 | 16 | 1.00 | 1.31 |
| Aromatic 2 | 19 | 12 | 0.75 | 1.58 |
| PosIonizable 1 | 11 | 11 | 0.69 | 1.00 |

## Feature resolution

Co-incident dual classifications collapsed by the feature hierarchy (higher-priority family kept on the shared atom); the listed ligands each carried both types on one atom.

| Kept ← dropped | Events | Ligands |
|---|---:|---|
| Aromatic ← LumpedHydrophobe | 21 | 7CKX_G3O_R501, 7CKY_G3U_R502, 7CRH_GBU_R501, 7JOZ_VFP_R1201, 7JVP_SK9_R501, 7JVQ_OR9_R501, 7LJC_SK0_R501, 7X2C_G3C_F503, 7X2D_86W_F502, 8IRR_R5F_R501, 8JXR_7LD_A401, 8JXS_V6X_A401, 9I52_A1IZU_R501, 9LLJ_LDP_R701, 9LWC_ALE_R501 |
| PosIonizable ← Donor | 10 | 7CKX_G3O_R501, 7CRH_GBU_R501, 7JVP_SK9_R501, 7JVQ_OR9_R501, 7LJC_SK0_R501, 7X2C_G3C_F503, 8IRR_R5F_R501, 8JXR_7LD_A401, 9LLJ_LDP_R701, 9LWC_ALE_R501 |

## Merged away

Clusters that passed the support/size floor but were displaced by the 1 Å cross-family overlap merge — one feature per region, keeping the denser one. Each row states in favour of which kept feature it was removed.

| Feature | Points | Ligands | Support | Occupancy | In favour of |
|---|---:|---:|---:|---:|---|
| Donor | 18 | 10 | 0.62 | 1.80 | Acceptor 1 |

## Below the support/size floor

Clusters that formed but never became candidates — below the 0.5 support floor or the minimum cluster size.

| Feature | Points | Ligands | Support | Occupancy |
|---|---:|---:|---:|---:|
| Donor | 12 | 7 | 0.44 | 1.71 |
| Acceptor | 7 | 7 | 0.44 | 1.00 |
| Acceptor | 7 | 6 | 0.38 | 1.17 |
| Acceptor | 6 | 6 | 0.38 | 1.00 |
| LumpedHydrophobe | 4 | 1 | 0.06 | 4.00 |
| Donor | 1 | 1 | 0.06 | 1.00 |
| PosIonizable | 1 | 1 | 0.06 | 1.00 |

See `pharmacophore.json` (model), `features.csv` (raw points + cluster ids), and `raw_features_*.png` (per-family point distributions, each kept peak annotated with its label and support).