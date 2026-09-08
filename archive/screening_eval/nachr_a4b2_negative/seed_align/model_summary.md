# Pharmacophore — nachr_a4b2_negative/seed_align

- Ligands loaded: **50** (template=3)
- Skipped poses: 0
- Consensus method: `density`
- Representative ligand (viz): `V024-1254__p1`
- Features kept: **2**

> **Directional features (Acceptor, Donor) are low-confidence in this build (marked †).** Reconstructed from aligned poses, they inherit the docking pose/flip ambiguity — a correctly placed ring can present its H-bond atom in the wrong orientation. The cation/aromatic anchors are pose-invariant and trustworthy.

**Support** = fraction of the cell's ligands that contribute to a feature (≤ 1.0; features are kept only above the 0.5 support floor). **Occupancy** = points ÷ contributing ligands (points-per-ligand, uncapped: > 1.0 when a cluster is denser than one point per ligand). One row per feature / peak.

| Feature | Points | Ligands | Support | Occupancy |
|---|---:|---:|---:|---:|
| Aromatic 1 | 25 | 25 | 0.50 | 1.00 |
| LumpedHydrophobe 1 | 29 | 29 | 0.58 | 1.00 |

## Below the support/size floor

Clusters that formed but never became candidates — below the 0.5 support floor or the minimum cluster size.

| Feature | Points | Ligands | Support | Occupancy |
|---|---:|---:|---:|---:|
| Donor | 22 | 22 | 0.44 | 1.00 |
| Acceptor | 22 | 22 | 0.44 | 1.00 |
| Acceptor | 31 | 21 | 0.42 | 1.48 |
| Aromatic | 21 | 21 | 0.42 | 1.00 |
| LumpedHydrophobe | 21 | 21 | 0.42 | 1.00 |
| Donor | 32 | 20 | 0.40 | 1.60 |
| PosIonizable | 20 | 20 | 0.40 | 1.00 |
| Acceptor | 19 | 19 | 0.38 | 1.00 |
| Acceptor | 16 | 16 | 0.32 | 1.00 |
| Aromatic | 14 | 14 | 0.28 | 1.00 |
| LumpedHydrophobe | 14 | 14 | 0.28 | 1.00 |
| Acceptor | 13 | 13 | 0.26 | 1.00 |
| Aromatic | 12 | 12 | 0.24 | 1.00 |
| LumpedHydrophobe | 12 | 12 | 0.24 | 1.00 |
| Donor | 11 | 11 | 0.22 | 1.00 |
| Acceptor | 9 | 9 | 0.18 | 1.00 |
| PosIonizable | 2 | 2 | 0.04 | 1.00 |
| PosIonizable | 1 | 1 | 0.02 | 1.00 |
| PosIonizable | 1 | 1 | 0.02 | 1.00 |
| Aromatic | 1 | 1 | 0.02 | 1.00 |

See `pharmacophore.json` (model), `features.csv` (raw points + cluster ids), and `raw_features_*.png` (per-family point distributions, each kept peak annotated with its label and support).