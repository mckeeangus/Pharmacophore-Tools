# Pharmacophore — ache/seed_align

- Ligands loaded: **50** (template=3)
- Skipped poses: 0
- Consensus method: `density`
- Representative ligand (viz): `Z1741977105__p1`
- Features kept: **5**

> **Directional features (Acceptor, Donor) are low-confidence in this build (marked †).** Reconstructed from aligned poses, they inherit the docking pose/flip ambiguity — a correctly placed ring can present its H-bond atom in the wrong orientation. The cation/aromatic anchors are pose-invariant and trustworthy.

**Support** = fraction of the cell's ligands that contribute to a feature (≤ 1.0; features are kept only above the 0.5 support floor). **Occupancy** = points ÷ contributing ligands (points-per-ligand, uncapped: > 1.0 when a cluster is denser than one point per ligand). One row per feature / peak.

| Feature | Points | Ligands | Support | Occupancy |
|---|---:|---:|---:|---:|
| Acceptor 1 † | 41 | 41 | 0.82 | 1.00 |
| Acceptor 2 † | 29 | 29 | 0.58 | 1.00 |
| Aromatic 1 | 43 | 43 | 0.86 | 1.00 |
| LumpedHydrophobe 1 | 43 | 43 | 0.86 | 1.00 |
| PosIonizable 1 | 33 | 33 | 0.66 | 1.00 |

## Below the support/size floor

Clusters that formed but never became candidates — below the 0.5 support floor or the minimum cluster size.

| Feature | Points | Ligands | Support | Occupancy |
|---|---:|---:|---:|---:|
| Aromatic | 22 | 22 | 0.44 | 1.00 |
| PosIonizable | 18 | 18 | 0.36 | 1.00 |
| LumpedHydrophobe | 13 | 13 | 0.26 | 1.00 |
| Donor | 10 | 10 | 0.20 | 1.00 |
| Aromatic | 7 | 7 | 0.14 | 1.00 |
| LumpedHydrophobe | 7 | 7 | 0.14 | 1.00 |
| Acceptor | 3 | 3 | 0.06 | 1.00 |
| Donor | 2 | 2 | 0.04 | 1.00 |
| Acceptor | 1 | 1 | 0.02 | 1.00 |
| PosIonizable | 1 | 1 | 0.02 | 1.00 |
| PosIonizable | 1 | 1 | 0.02 | 1.00 |
| LumpedHydrophobe | 1 | 1 | 0.02 | 1.00 |

See `pharmacophore.json` (model), `features.csv` (raw points + cluster ids), and `raw_features_*.png` (per-family point distributions, each kept peak annotated with its label and support).