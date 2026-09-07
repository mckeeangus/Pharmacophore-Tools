# Pharmacophore — nav1_7_vsd4/seed_align

- Ligands loaded: **50** (template=3)
- Skipped poses: 0
- Consensus method: `density`
- Representative ligand (viz): `Z33311913__p3`
- Features kept: **7**

> **Directional features (Acceptor, Donor) are low-confidence in this build (marked †).** Reconstructed from aligned poses, they inherit the docking pose/flip ambiguity — a correctly placed ring can present its H-bond atom in the wrong orientation. The cation/aromatic anchors are pose-invariant and trustworthy.

**Support** = fraction of the cell's ligands that contribute to a feature (≤ 1.0; features are kept only above the 0.5 support floor). **Occupancy** = points ÷ contributing ligands (points-per-ligand, uncapped: > 1.0 when a cluster is denser than one point per ligand). One row per feature / peak.

| Feature | Points | Ligands | Support | Occupancy |
|---|---:|---:|---:|---:|
| Acceptor 1 † | 33 | 33 | 0.66 | 1.00 |
| Aromatic 1 | 38 | 38 | 0.76 | 1.00 |
| Aromatic 2 | 37 | 36 | 0.72 | 1.03 |
| Donor 1 † | 28 | 28 | 0.56 | 1.00 |
| LumpedHydrophobe 1 | 38 | 38 | 0.76 | 1.00 |
| LumpedHydrophobe 2 | 37 | 34 | 0.68 | 1.09 |
| LumpedHydrophobe 3 | 26 | 26 | 0.52 | 1.00 |

## Below the support/size floor

Clusters that formed but never became candidates — below the 0.5 support floor or the minimum cluster size.

| Feature | Points | Ligands | Support | Occupancy |
|---|---:|---:|---:|---:|
| Aromatic | 24 | 24 | 0.48 | 1.00 |
| Donor | 23 | 23 | 0.46 | 1.00 |
| LumpedHydrophobe | 16 | 16 | 0.32 | 1.00 |
| Aromatic | 15 | 15 | 0.30 | 1.00 |
| Acceptor | 17 | 13 | 0.26 | 1.31 |
| Donor | 12 | 12 | 0.24 | 1.00 |
| Acceptor | 10 | 10 | 0.20 | 1.00 |
| Acceptor | 3 | 3 | 0.06 | 1.00 |

See `pharmacophore.json` (model), `features.csv` (raw points + cluster ids), and `raw_features_*.png` (per-family point distributions, each kept peak annotated with its label and support).