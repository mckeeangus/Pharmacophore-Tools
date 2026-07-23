# Pharmacophore — adrb2/orthosteric__positive

- Ligands loaded: **11** (direct=1, template=10)
- Skipped poses: 0
- Consensus method: `density`
- Representative ligand (viz): `4LDL_XQC_A1401`
- Features kept: **7**
- Excluded-volume spheres (receptor markers): **40**

**Support** = fraction of the cell's ligands that contribute to a feature (≤ 1.0; features are kept only above the 0.5 support floor). **Occupancy** = points ÷ contributing ligands (points-per-ligand, uncapped: > 1.0 when a cluster is denser than one point per ligand). One row per feature / peak.

| Feature | Points | Ligands | Support | Occupancy |
|---|---:|---:|---:|---:|
| Acceptor 1 | 10 | 10 | 0.91 | 1.00 |
| Acceptor 2 | 10 | 10 | 0.91 | 1.00 |
| Aromatic 1 | 11 | 11 | 1.00 | 1.00 |
| Donor 1 | 10 | 10 | 0.91 | 1.00 |
| Donor 2 | 10 | 10 | 0.91 | 1.00 |
| LumpedHydrophobe 1 | 11 | 11 | 1.00 | 1.00 |
| PosIonizable 1 | 10 | 10 | 0.91 | 1.00 |

## Feature resolution

Co-incident dual classifications collapsed by the feature hierarchy (higher-priority family kept on the shared atom); the listed ligands each carried both types on one atom.

| Kept ← dropped | Events | Ligands |
|---|---:|---|
| PosIonizable ← Donor | 11 | 4LDE_P0G_A1401, 4LDL_XQC_A1401, 4LDO_ALE_A1402, 6MXT_K5Y_A1401, 7DHI_68H_R401, 7XK9_GJ6_A1401, 8GG0_G1I_R501, 8JJ8_H98_F501, 8JJL_DZQ_A501, 9BUY_A1ASM_R504, 9LW5_LDP_R401 |

## Below the support/size floor

Clusters that formed but never became candidates — below the 0.5 support floor or the minimum cluster size.

| Feature | Points | Ligands | Support | Occupancy |
|---|---:|---:|---:|---:|
| Acceptor | 5 | 5 | 0.45 | 1.00 |
| Aromatic | 4 | 4 | 0.36 | 1.00 |
| LumpedHydrophobe | 4 | 4 | 0.36 | 1.00 |
| Aromatic | 2 | 2 | 0.18 | 1.00 |
| LumpedHydrophobe | 2 | 2 | 0.18 | 1.00 |
| Donor | 1 | 1 | 0.09 | 1.00 |

See `pharmacophore.json` (model), `features.csv` (raw points + cluster ids), and `raw_features_*.png` (per-family point distributions, each kept peak annotated with its label and support).