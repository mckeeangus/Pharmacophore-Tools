# Pharmacophore — gr_nr3c1/seed_align

- Ligands loaded: **50** (template=3)
- Skipped poses: 0
- Consensus method: `density`
- Representative ligand (viz): `Z56815564__p8`
- Features kept: **3**

> **Directional features (Acceptor, Donor) are low-confidence in this build (marked †).** Reconstructed from aligned poses, they inherit the docking pose/flip ambiguity — a correctly placed ring can present its H-bond atom in the wrong orientation. The cation/aromatic anchors are pose-invariant and trustworthy.

**Support** = fraction of the cell's ligands that contribute to a feature (≤ 1.0; features are kept only above the 0.5 support floor). **Occupancy** = points ÷ contributing ligands (points-per-ligand, uncapped: > 1.0 when a cluster is denser than one point per ligand). One row per feature / peak.

| Feature | Points | Ligands | Support | Occupancy |
|---|---:|---:|---:|---:|
| Aromatic 1 | 39 | 39 | 0.78 | 1.00 |
| Aromatic 2 | 28 | 28 | 0.56 | 1.00 |
| LumpedHydrophobe 1 | 33 | 33 | 0.66 | 1.00 |

## Below the support/size floor

Clusters that formed but never became candidates — below the 0.5 support floor or the minimum cluster size.

| Feature | Points | Ligands | Support | Occupancy |
|---|---:|---:|---:|---:|
| Donor | 24 | 24 | 0.48 | 1.00 |
| LumpedHydrophobe | 24 | 24 | 0.48 | 1.00 |
| Acceptor | 23 | 22 | 0.44 | 1.05 |
| Acceptor | 20 | 19 | 0.38 | 1.05 |
| Acceptor | 19 | 18 | 0.36 | 1.06 |
| LumpedHydrophobe | 17 | 17 | 0.34 | 1.00 |
| Aromatic | 15 | 15 | 0.30 | 1.00 |
| Donor | 9 | 9 | 0.18 | 1.00 |
| LumpedHydrophobe | 8 | 8 | 0.16 | 1.00 |
| PosIonizable | 4 | 4 | 0.08 | 1.00 |
| Donor | 2 | 2 | 0.04 | 1.00 |
| Acceptor | 2 | 2 | 0.04 | 1.00 |
| Acceptor | 1 | 1 | 0.02 | 1.00 |
| Acceptor | 1 | 1 | 0.02 | 1.00 |
| Acceptor | 1 | 1 | 0.02 | 1.00 |
| Acceptor | 1 | 1 | 0.02 | 1.00 |
| PosIonizable | 1 | 1 | 0.02 | 1.00 |
| PosIonizable | 1 | 1 | 0.02 | 1.00 |
| PosIonizable | 1 | 1 | 0.02 | 1.00 |
| PosIonizable | 1 | 1 | 0.02 | 1.00 |
| PosIonizable | 1 | 1 | 0.02 | 1.00 |
| PosIonizable | 0 | 0 | 0.00 | 0.00 |

See `pharmacophore.json` (model), `features.csv` (raw points + cluster ids), and `raw_features_*.png` (per-family point distributions, each kept peak annotated with its label and support).