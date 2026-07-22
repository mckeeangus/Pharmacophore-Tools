# Pharmacophore — nachr_a4b2/orthosteric__positive

- Ligands loaded: **18** (direct=2, template=16)
- Skipped poses: 1 (3WTN_N2Y_H301:fail)
- Consensus method: `density`
- Representative ligand (viz): `4FRR_0VC_F301`
- Features kept: **3**
- Excluded-volume spheres (receptor markers): **40**

**Support** = fraction of the cell's ligands that contribute to a feature (≤ 1.0; features are kept only above the 0.5 support floor). **Occupancy** = points ÷ contributing ligands (points-per-ligand, uncapped: > 1.0 when a cluster is denser than one point per ligand). One row per feature / peak.

| Feature | Points | Ligands | Support | Occupancy |
|---|---:|---:|---:|---:|
| Acceptor 1 | 17 | 17 | 0.94 | 1.00 |
| Aromatic 1 | 14 | 14 | 0.78 | 1.00 |
| PosIonizable 1 | 15 | 15 | 0.83 | 1.00 |

## Feature resolution

Co-incident dual classifications collapsed by the feature hierarchy (higher-priority family kept on the shared atom); the listed ligands each carried both types on one atom.

| Kept ← dropped | Events | Ligands |
|---|---:|---|
| Aromatic ← LumpedHydrophobe | 1 | 3U8L_09Q_J211 |
| PosIonizable ← Donor | 13 | 3U8J_09O_A211, 3U8K_09P_F211, 3U8L_09Q_J211, 3U8M_09R_L211, 3U8N_09S_Q211, 3ZDG_XRX_I301, 3ZDH_XRS_A301, 4FRR_0VC_F301, 4ZJS_4P0_D301, 5BP0_FN1_D302, 5O87_NCT_A601, 5SYO_C5E_E301, 6SGV_LDQ_G601 |

## Below the support/size floor

Clusters that formed but never became candidates — below the 0.5 support floor or the minimum cluster size.

| Feature | Points | Ligands | Support | Occupancy |
|---|---:|---:|---:|---:|
| Donor | 2 | 2 | 0.11 | 1.00 |
| Donor | 1 | 1 | 0.06 | 1.00 |
| LumpedHydrophobe | 1 | 1 | 0.06 | 1.00 |
| LumpedHydrophobe | 1 | 1 | 0.06 | 1.00 |
| Acceptor | 0 | 0 | 0.00 | 0.00 |

See `pharmacophore.json` (model), `features.csv` (raw points + cluster ids), and `raw_features_*.png` (per-family point distributions, each kept peak annotated with its label and support).