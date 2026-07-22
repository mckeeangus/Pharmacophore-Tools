# Pharmacophore — gr_nr3c1/lbp__negative

- Ligands loaded: **3** (template=3)
- Skipped poses: 0
- Consensus method: `density`
- Representative ligand (viz): `4MDD_29M_B801`
- Features kept: **2**
- Excluded-volume spheres (receptor markers): **40**

**Support** = fraction of the cell's ligands that contribute to a feature (≤ 1.0; features are kept only above the 0.5 support floor). **Occupancy** = points ÷ contributing ligands (points-per-ligand, uncapped: > 1.0 when a cluster is denser than one point per ligand). One row per feature / peak.

| Feature | Points | Ligands | Support | Occupancy |
|---|---:|---:|---:|---:|
| Aromatic 1 | 2 | 2 | 0.67 | 1.00 |
| Donor 1 | 2 | 2 | 0.67 | 1.00 |

## Feature resolution

Co-incident dual classifications collapsed by the feature hierarchy (higher-priority family kept on the shared atom); the listed ligands each carried both types on one atom.

| Kept ← dropped | Events | Ligands |
|---|---:|---|
| Aromatic ← LumpedHydrophobe | 5 | 4MDD_29M_B801, 5UC3_486_B801, 6DXK_HJ4_A801 |
| PosIonizable ← Donor | 1 | 4MDD_29M_B801 |

## Below the support/size floor

Clusters that formed but never became candidates — below the 0.5 support floor or the minimum cluster size.

| Feature | Points | Ligands | Support | Occupancy |
|---|---:|---:|---:|---:|
| Acceptor | 2 | 2 | 0.67 | 1.00 |
| Acceptor | 2 | 2 | 0.67 | 1.00 |
| LumpedHydrophobe | 2 | 2 | 0.67 | 1.00 |
| LumpedHydrophobe | 2 | 2 | 0.67 | 1.00 |
| Acceptor | 1 | 1 | 0.33 | 1.00 |
| PosIonizable | 1 | 1 | 0.33 | 1.00 |

See `pharmacophore.json` (model), `features.csv` (raw points + cluster ids), and `raw_features_*.png` (per-family point distributions, each kept peak annotated with its label and support).