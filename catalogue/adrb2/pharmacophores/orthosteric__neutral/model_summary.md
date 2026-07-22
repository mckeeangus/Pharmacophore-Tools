# Pharmacophore — adrb2/orthosteric__neutral

- Ligands loaded: **3** (template=3)
- Skipped poses: 0
- Consensus method: `density`
- Representative ligand (viz): `8W1V_A1AE2_B1201`
- Features kept: **1**
- Excluded-volume spheres (receptor markers): **40**

**Support** = fraction of the cell's ligands that contribute to a feature (≤ 1.0; features are kept only above the 0.5 support floor). **Occupancy** = points ÷ contributing ligands (points-per-ligand, uncapped: > 1.0 when a cluster is denser than one point per ligand). One row per feature / peak.

| Feature | Points | Ligands | Support | Occupancy |
|---|---:|---:|---:|---:|
| PosIonizable 1 | 3 | 3 | 1.00 | 1.00 |

## Feature resolution

Co-incident dual classifications collapsed by the feature hierarchy (higher-priority family kept on the shared atom); the listed ligands each carried both types on one atom.

| Kept ← dropped | Events | Ligands |
|---|---:|---|
| Aromatic ← LumpedHydrophobe | 5 | 6PS2_JTZ_A1201, 8W1V_A1AE2_B1201, 9W3F_BER_A1201 |
| PosIonizable ← Donor | 3 | 6PS2_JTZ_A1201, 8W1V_A1AE2_B1201 |

## Below the support/size floor

Clusters that formed but never became candidates — below the 0.5 support floor or the minimum cluster size.

| Feature | Points | Ligands | Support | Occupancy |
|---|---:|---:|---:|---:|
| Donor | 2 | 2 | 0.67 | 1.00 |
| Acceptor | 2 | 2 | 0.67 | 1.00 |
| Acceptor | 2 | 2 | 0.67 | 1.00 |
| Aromatic | 2 | 2 | 0.67 | 1.00 |
| Acceptor | 2 | 1 | 0.33 | 2.00 |
| Acceptor | 2 | 1 | 0.33 | 2.00 |
| Donor | 1 | 1 | 0.33 | 1.00 |
| Acceptor | 1 | 1 | 0.33 | 1.00 |
| Acceptor | 1 | 1 | 0.33 | 1.00 |
| PosIonizable | 1 | 1 | 0.33 | 1.00 |
| Aromatic | 1 | 1 | 0.33 | 1.00 |
| Aromatic | 1 | 1 | 0.33 | 1.00 |
| Aromatic | 1 | 1 | 0.33 | 1.00 |
| LumpedHydrophobe | 1 | 1 | 0.33 | 1.00 |
| LumpedHydrophobe | 1 | 1 | 0.33 | 1.00 |

See `pharmacophore.json` (model), `features.csv` (raw points + cluster ids), and `raw_features_*.png` (per-family point distributions, each kept peak annotated with its label and support).