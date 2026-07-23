# Pharmacophore — adora2a/orthosteric__negative

- Ligands loaded: **25** (template=25)
- Skipped poses: 3 (5UIG_8D1_A503:fail, 7PX4_8E2_A2404:fail, 7PYR_8IM_A2404:fail)
- Consensus method: `density`
- Representative ligand (viz): `5IUB_6DV_A2401`
- Features kept: **2**
- Excluded-volume spheres (receptor markers): **40**

**Support** = fraction of the cell's ligands that contribute to a feature (≤ 1.0; features are kept only above the 0.5 support floor). **Occupancy** = points ÷ contributing ligands (points-per-ligand, uncapped: > 1.0 when a cluster is denser than one point per ligand). One row per feature / peak.

| Feature | Points | Ligands | Support | Occupancy |
|---|---:|---:|---:|---:|
| Aromatic 1 | 30 | 24 | 0.96 | 1.25 |
| Donor 1 | 14 | 14 | 0.56 | 1.00 |

## Feature resolution

Co-incident dual classifications collapsed by the feature hierarchy (higher-priority family kept on the shared atom); the listed ligands each carried both types on one atom.

| Kept ← dropped | Events | Ligands |
|---|---:|---|
| PosIonizable ← Donor | 17 | 3REY_XAC_A999, 5IU7_6DY_A2401, 5IU8_6DZ_A2401, 5IUA_6DX_A2401, 5IUB_6DV_A2401, 5N2R_8JN_A2401, 7IO5_TEP_A1202, 8RW4_A1H3L_A1201, 8RW7_A1H3J_A1201 |

## Below the support/size floor

Clusters that formed but never became candidates — below the 0.5 support floor or the minimum cluster size.

| Feature | Points | Ligands | Support | Occupancy |
|---|---:|---:|---:|---:|
| Acceptor | 14 | 11 | 0.44 | 1.27 |
| PosIonizable | 8 | 8 | 0.32 | 1.00 |
| Aromatic | 7 | 7 | 0.28 | 1.00 |
| Acceptor | 6 | 6 | 0.24 | 1.00 |
| LumpedHydrophobe | 6 | 6 | 0.24 | 1.00 |
| Donor | 5 | 5 | 0.20 | 1.00 |
| LumpedHydrophobe | 4 | 4 | 0.16 | 1.00 |
| PosIonizable | 4 | 4 | 0.16 | 1.00 |
| Aromatic | 3 | 3 | 0.12 | 1.00 |
| LumpedHydrophobe | 3 | 3 | 0.12 | 1.00 |
| Donor | 2 | 2 | 0.08 | 1.00 |
| Donor | 2 | 2 | 0.08 | 1.00 |
| LumpedHydrophobe | 4 | 1 | 0.04 | 4.00 |
| Acceptor | 1 | 1 | 0.04 | 1.00 |
| LumpedHydrophobe | 1 | 1 | 0.04 | 1.00 |
| PosIonizable | 1 | 1 | 0.04 | 1.00 |
| PosIonizable | 1 | 1 | 0.04 | 1.00 |

See `pharmacophore.json` (model), `features.csv` (raw points + cluster ids), and `raw_features_*.png` (per-family point distributions, each kept peak annotated with its label and support).