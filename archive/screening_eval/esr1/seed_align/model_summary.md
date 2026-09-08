# Pharmacophore — esr1

- Ligands loaded: **100** (direct=1, template=4)
- Skipped poses: 0
- Consensus method: `density`
- Representative ligand (viz): `STL560881__p4`
- Features kept: **7**

> **Directional features (Acceptor, Donor) are low-confidence in this build (marked †).** Reconstructed from aligned poses, they inherit the docking pose/flip ambiguity — a correctly placed ring can present its H-bond atom in the wrong orientation. The cation/aromatic anchors are pose-invariant and trustworthy.

**Support** = fraction of the cell's ligands that contribute to a feature (≤ 1.0; features are kept only above the 0.5 support floor). **Occupancy** = points ÷ contributing ligands (points-per-ligand, uncapped: > 1.0 when a cluster is denser than one point per ligand). One row per feature / peak.

| Feature | Points | Ligands | Support | Occupancy |
|---|---:|---:|---:|---:|
| Acceptor 1 † | 74 | 74 | 0.74 | 1.00 |
| Acceptor 2 † | 57 | 57 | 0.57 | 1.00 |
| Aromatic 1 | 96 | 96 | 0.96 | 1.00 |
| Aromatic 2 | 79 | 67 | 0.67 | 1.18 |
| Donor 1 † | 72 | 72 | 0.72 | 1.00 |
| LumpedHydrophobe 1 | 109 | 77 | 0.77 | 1.42 |
| LumpedHydrophobe 2 | 93 | 92 | 0.92 | 1.01 |

## Below the support/size floor

Clusters that formed but never became candidates — below the 0.5 support floor or the minimum cluster size.

| Feature | Points | Ligands | Support | Occupancy |
|---|---:|---:|---:|---:|
| Donor | 42 | 42 | 0.42 | 1.00 |
| Aromatic | 2 | 2 | 0.02 | 1.00 |
| LumpedHydrophobe | 2 | 2 | 0.02 | 1.00 |
| PosIonizable | 1 | 1 | 0.01 | 1.00 |
| PosIonizable | 1 | 1 | 0.01 | 1.00 |
| PosIonizable | 1 | 1 | 0.01 | 1.00 |
| PosIonizable | 1 | 1 | 0.01 | 1.00 |

See `pharmacophore.json` (model), `features.csv` (raw points + cluster ids), and `raw_features_*.png` (per-family point distributions, each kept peak annotated with its label and support).