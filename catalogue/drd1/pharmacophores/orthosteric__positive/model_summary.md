# Pharmacophore — drd1/orthosteric__positive

- Ligands loaded: **16** (direct=1, template=15)
- Skipped poses: 0
- Consensus method: `density`
- Representative ligand (viz): `7X2C_G3C_F503`
- Features kept: **7**
- Excluded-volume spheres (receptor markers): **40**

**Support** = fraction of the cell's ligands that contribute to a feature (≤ 1.0; features are kept only above the 0.5 support floor). **Occupancy** = points ÷ contributing ligands (points-per-ligand, uncapped: > 1.0 when a cluster is denser than one point per ligand). One row per feature / peak.

| Feature | Points | Ligands | Support | Occupancy |
|---|---:|---:|---:|---:|
| Acceptor 1 | 8 | 8 | 0.50 | 1.00 |
| Aromatic 1 | 19 | 14 | 0.88 | 1.36 |
| Aromatic 2 | 10 | 10 | 0.62 | 1.00 |
| Donor 1 | 8 | 8 | 0.50 | 1.00 |
| LumpedHydrophobe 1 | 13 | 10 | 0.62 | 1.30 |
| LumpedHydrophobe 2 | 10 | 10 | 0.62 | 1.00 |
| PosIonizable 1 | 8 | 8 | 0.50 | 1.00 |

## Feature resolution

Co-incident dual classifications collapsed by the feature hierarchy (higher-priority family kept on the shared atom); the listed ligands each carried both types on one atom.

| Kept ← dropped | Events | Ligands |
|---|---:|---|
| PosIonizable ← Donor | 10 | 7CKX_G3O_R501, 7CRH_GBU_R501, 7JVP_SK9_R501, 7JVQ_OR9_R501, 7LJC_SK0_R501, 7X2C_G3C_F503, 8IRR_R5F_R501, 8JXR_7LD_A401, 9LLJ_LDP_R701, 9LWC_ALE_R501 |

## Below the support/size floor

Clusters that formed but never became candidates — below the 0.5 support floor or the minimum cluster size.

| Feature | Points | Ligands | Support | Occupancy |
|---|---:|---:|---:|---:|
| Acceptor | 6 | 6 | 0.38 | 1.00 |
| Donor | 7 | 5 | 0.31 | 1.40 |
| Acceptor | 5 | 5 | 0.31 | 1.00 |
| Acceptor | 2 | 2 | 0.12 | 1.00 |
| Donor | 1 | 1 | 0.06 | 1.00 |
| PosIonizable | 1 | 1 | 0.06 | 1.00 |

See `pharmacophore.json` (model), `features.csv` (raw points + cluster ids), and `raw_features_*.png` (per-family point distributions, each kept peak annotated with its label and support).