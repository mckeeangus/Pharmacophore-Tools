# Pharmacophore — nav1_7_pore/seed_align

- Ligands loaded: **50** (template=3)
- Skipped poses: 0
- Consensus method: `density`
- Representative ligand (viz): `8004-3784__p1`
- Features kept: **6**

> **Directional features (Acceptor, Donor) are low-confidence in this build (marked †).** Reconstructed from aligned poses, they inherit the docking pose/flip ambiguity — a correctly placed ring can present its H-bond atom in the wrong orientation. The cation/aromatic anchors are pose-invariant and trustworthy.

**Support** = fraction of the cell's ligands that contribute to a feature (≤ 1.0; features are kept only above the 0.5 support floor). **Occupancy** = points ÷ contributing ligands (points-per-ligand, uncapped: > 1.0 when a cluster is denser than one point per ligand). One row per feature / peak.

| Feature | Points | Ligands | Support | Occupancy |
|---|---:|---:|---:|---:|
| Acceptor 1 † | 37 | 37 | 0.74 | 1.00 |
| Aromatic 1 | 44 | 44 | 0.88 | 1.00 |
| Donor 1 † | 28 | 26 | 0.52 | 1.08 |
| LumpedHydrophobe 1 | 45 | 30 | 0.60 | 1.50 |
| LumpedHydrophobe 2 | 41 | 41 | 0.82 | 1.00 |
| LumpedHydrophobe 3 | 28 | 25 | 0.50 | 1.12 |

## Below the support/size floor

Clusters that formed but never became candidates — below the 0.5 support floor or the minimum cluster size.

| Feature | Points | Ligands | Support | Occupancy |
|---|---:|---:|---:|---:|
| PosIonizable | 13 | 13 | 0.26 | 1.00 |
| Acceptor | 12 | 12 | 0.24 | 1.00 |
| Aromatic | 10 | 10 | 0.20 | 1.00 |
| Acceptor | 7 | 7 | 0.14 | 1.00 |
| Acceptor | 4 | 4 | 0.08 | 1.00 |
| Acceptor | 2 | 2 | 0.04 | 1.00 |
| PosIonizable | 2 | 2 | 0.04 | 1.00 |
| PosIonizable | 2 | 2 | 0.04 | 1.00 |
| LumpedHydrophobe | 4 | 1 | 0.02 | 4.00 |
| LumpedHydrophobe | 4 | 1 | 0.02 | 4.00 |
| Donor | 1 | 1 | 0.02 | 1.00 |
| Donor | 1 | 1 | 0.02 | 1.00 |
| Donor | 1 | 1 | 0.02 | 1.00 |
| Donor | 1 | 1 | 0.02 | 1.00 |
| Acceptor | 1 | 1 | 0.02 | 1.00 |
| PosIonizable | 1 | 1 | 0.02 | 1.00 |
| PosIonizable | 1 | 1 | 0.02 | 1.00 |
| PosIonizable | 1 | 1 | 0.02 | 1.00 |
| NegIonizable | 1 | 1 | 0.02 | 1.00 |
| NegIonizable | 1 | 1 | 0.02 | 1.00 |

See `pharmacophore.json` (model), `features.csv` (raw points + cluster ids), and `raw_features_*.png` (per-family point distributions, each kept peak annotated with its label and support).