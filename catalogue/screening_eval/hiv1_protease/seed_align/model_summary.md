# Pharmacophore — hiv1_protease/seed_align

- Ligands loaded: **50** (direct=1, template=2)
- Skipped poses: 0
- Consensus method: `density`
- Representative ligand (viz): `OSSM_156250__p5`
- Features kept: **3**

> **Directional features (Acceptor, Donor) are low-confidence in this build (marked †).** Reconstructed from aligned poses, they inherit the docking pose/flip ambiguity — a correctly placed ring can present its H-bond atom in the wrong orientation. The cation/aromatic anchors are pose-invariant and trustworthy.

**Support** = fraction of the cell's ligands that contribute to a feature (≤ 1.0; features are kept only above the 0.5 support floor). **Occupancy** = points ÷ contributing ligands (points-per-ligand, uncapped: > 1.0 when a cluster is denser than one point per ligand). One row per feature / peak.

| Feature | Points | Ligands | Support | Occupancy |
|---|---:|---:|---:|---:|
| Acceptor 1 † | 32 | 32 | 0.64 | 1.00 |
| Aromatic 1 | 37 | 37 | 0.74 | 1.00 |
| LumpedHydrophobe 1 | 36 | 36 | 0.72 | 1.00 |

## Below the support/size floor

Clusters that formed but never became candidates — below the 0.5 support floor or the minimum cluster size.

| Feature | Points | Ligands | Support | Occupancy |
|---|---:|---:|---:|---:|
| LumpedHydrophobe | 24 | 24 | 0.48 | 1.00 |
| Aromatic | 22 | 22 | 0.44 | 1.00 |
| LumpedHydrophobe | 21 | 21 | 0.42 | 1.00 |
| LumpedHydrophobe | 12 | 12 | 0.24 | 1.00 |
| Donor | 11 | 11 | 0.22 | 1.00 |
| Acceptor | 13 | 9 | 0.18 | 1.44 |
| PosIonizable | 8 | 8 | 0.16 | 1.00 |
| Aromatic | 5 | 5 | 0.10 | 1.00 |
| Aromatic | 5 | 5 | 0.10 | 1.00 |
| Donor | 2 | 2 | 0.04 | 1.00 |
| Donor | 1 | 1 | 0.02 | 1.00 |
| Acceptor | 1 | 1 | 0.02 | 1.00 |
| PosIonizable | 1 | 1 | 0.02 | 1.00 |

See `pharmacophore.json` (model), `features.csv` (raw points + cluster ids), and `raw_features_*.png` (per-family point distributions, each kept peak annotated with its label and support).