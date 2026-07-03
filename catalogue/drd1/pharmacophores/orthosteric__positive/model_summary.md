# Pharmacophore — drd1/orthosteric__positive

- Ligands loaded: **16** (direct=1, template=15)
- Skipped poses: 0
- Consensus method: `kmeans`
- Representative ligand (viz): `9I54_A1IZV_R501`
- Features kept: **4**

Support is the fraction of the cell's ligands that contribute to a feature (one row per feature / peak; all features are kept only above the support floor).

| Feature | Points | Ligands | Support |
|---|---:|---:|---:|
| Acceptor 1 | 31 | 15 | 0.94 |
| Acceptor 2 | 16 | 8 | 0.50 |
| Aromatic 1 | 11 | 11 | 0.69 |
| PosIonizable 1 | 11 | 11 | 0.69 |

## Feature resolution

Co-incident dual classifications collapsed by the feature hierarchy (higher-priority family kept on the shared atom); the listed ligands each carried both types on one atom.

| Kept ← dropped | Events | Ligands |
|---|---:|---|
| Aromatic ← LumpedHydrophobe | 21 | 7CKX_G3O_R501, 7CKY_G3U_R502, 7CRH_GBU_R501, 7JOZ_VFP_R1201, 7JVP_SK9_R501, 7JVQ_OR9_R501, 7LJC_SK0_R501, 7X2C_G3C_F503, 7X2D_86W_F502, 8IRR_R5F_R501, 8JXR_7LD_A401, 8JXS_V6X_A401, 9I52_A1IZU_R501, 9LLJ_LDP_R701, 9LWC_ALE_R501 |
| PosIonizable ← Donor | 10 | 7CKX_G3O_R501, 7CRH_GBU_R501, 7JVP_SK9_R501, 7JVQ_OR9_R501, 7LJC_SK0_R501, 7X2C_G3C_F503, 8IRR_R5F_R501, 8JXR_7LD_A401, 9LLJ_LDP_R701, 9LWC_ALE_R501 |

## Not selected

Clusters/peaks that formed but did not enter the model — below the support or size floor, or displaced by the cross-family overlap merge — with their mean support (fraction of the cell's ligands contributing).

| Feature | Points | Ligands | Mean support |
|---|---:|---:|---:|
| Aromatic | 21 | 16 | 1.00 |
| Donor | 19 | 10 | 0.62 |
| Donor | 12 | 7 | 0.44 |
| Aromatic | 8 | 7 | 0.44 |
| LumpedHydrophobe | 3 | 1 | 0.06 |
| PosIonizable | 1 | 1 | 0.06 |
| LumpedHydrophobe | 1 | 1 | 0.06 |

See `pharmacophore.json` (model), `features.csv` (raw points + cluster ids), and `raw_features_*.png` (per-family point distributions, each kept peak annotated with its label and support).