# Pharmacophore — ca2/seed_align

- Ligands loaded: **37** (direct=2, template=1)
- Skipped poses: 0
- Consensus method: `density`
- Representative ligand (viz): `Z285136922__p1`
- Features kept: **1**

> **Directional features (Acceptor, Donor) are low-confidence in this build (marked †).** Reconstructed from aligned poses, they inherit the docking pose/flip ambiguity — a correctly placed ring can present its H-bond atom in the wrong orientation. The cation/aromatic anchors are pose-invariant and trustworthy.

**Support** = fraction of the cell's ligands that contribute to a feature (≤ 1.0; features are kept only above the 0.5 support floor). **Occupancy** = points ÷ contributing ligands (points-per-ligand, uncapped: > 1.0 when a cluster is denser than one point per ligand). One row per feature / peak.

| Feature | Points | Ligands | Support | Occupancy |
|---|---:|---:|---:|---:|
| Acceptor 1 † | 26 | 26 | 0.70 | 1.00 |

## Below the support/size floor

Clusters that formed but never became candidates — below the 0.5 support floor or the minimum cluster size.

| Feature | Points | Ligands | Support | Occupancy |
|---|---:|---:|---:|---:|
| Aromatic | 17 | 17 | 0.46 | 1.00 |
| Aromatic | 15 | 15 | 0.41 | 1.00 |
| Aromatic | 15 | 15 | 0.41 | 1.00 |
| LumpedHydrophobe | 14 | 14 | 0.38 | 1.00 |
| Donor | 13 | 13 | 0.35 | 1.00 |
| LumpedHydrophobe | 13 | 13 | 0.35 | 1.00 |
| Donor | 7 | 7 | 0.19 | 1.00 |
| Aromatic | 7 | 7 | 0.19 | 1.00 |
| LumpedHydrophobe | 5 | 5 | 0.14 | 1.00 |
| Donor | 2 | 2 | 0.05 | 1.00 |
| PosIonizable | 2 | 2 | 0.05 | 1.00 |
| PosIonizable | 1 | 1 | 0.03 | 1.00 |

See `pharmacophore.json` (model), `features.csv` (raw points + cluster ids), and `raw_features_*.png` (per-family point distributions, each kept peak annotated with its label and support).