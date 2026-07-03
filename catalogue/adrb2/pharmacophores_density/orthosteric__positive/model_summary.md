# Pharmacophore — adrb2/orthosteric__positive

- Ligands loaded: **11** (direct=1, template=10)
- Skipped poses: 0
- Consensus method: `density`
- Representative ligand (viz): `4LDL_XQC_A1401`
- Features kept: **2**
- Excluded-volume spheres (receptor markers): **40**

Support is the fraction of the cell's ligands that contribute to a feature (one row per feature / peak; all features are kept only above the support floor).

| Feature | Points | Ligands | Support |
|---|---:|---:|---:|
| Acceptor 1 | 24 | 11 | 1.00 |
| PosIonizable 1 | 11 | 11 | 1.00 |

## Feature resolution

Co-incident dual classifications collapsed by the feature hierarchy (higher-priority family kept on the shared atom); the listed ligands each carried both types on one atom.

| Kept ← dropped | Events | Ligands |
|---|---:|---|
| Aromatic ← LumpedHydrophobe | 17 | 4LDE_P0G_A1401, 4LDL_XQC_A1401, 4LDO_ALE_A1402, 6MXT_K5Y_A1401, 7DHI_68H_R401, 7XK9_GJ6_A1401, 8GG0_G1I_R501, 8JJ8_H98_F501, 8JJL_DZQ_A501, 9BUY_A1ASM_R504, 9LW5_LDP_R401 |
| PosIonizable ← Donor | 11 | 4LDE_P0G_A1401, 4LDL_XQC_A1401, 4LDO_ALE_A1402, 6MXT_K5Y_A1401, 7DHI_68H_R401, 7XK9_GJ6_A1401, 8GG0_G1I_R501, 8JJ8_H98_F501, 8JJL_DZQ_A501, 9BUY_A1ASM_R504, 9LW5_LDP_R401 |

See `pharmacophore.json` (model), `features.csv` (raw points + cluster ids), and `raw_features_*.png` (per-family point distributions, each kept peak annotated with its label and support).