# Pharmacophore — seed_align

- Ligands loaded: **84** (direct=3, template=2)
- Skipped poses: 0
- Consensus method: `density`
- Representative ligand (viz): `OSSM_091763__p1`
- Features kept: **3**

> **Directional features (Acceptor, Donor) are low-confidence in this build (marked †).** Reconstructed from aligned poses, they inherit the docking pose/flip ambiguity — a correctly placed ring can present its H-bond atom in the wrong orientation. The cation/aromatic anchors are pose-invariant and trustworthy.

**Support** = fraction of the cell's ligands that contribute to a feature (≤ 1.0; features are kept only above the 0.5 support floor). **Occupancy** = points ÷ contributing ligands (points-per-ligand, uncapped: > 1.0 when a cluster is denser than one point per ligand). One row per feature / peak.

| Feature | Points | Ligands | Support | Occupancy |
|---|---:|---:|---:|---:|
| Acceptor 1 † | 55 | 52 | 0.62 | 1.06 |
| Aromatic 1 | 73 | 73 | 0.87 | 1.00 |
| PosIonizable 1 | 48 | 48 | 0.57 | 1.00 |

## Below the support/size floor

Clusters that formed but never became candidates — below the 0.5 support floor or the minimum cluster size.

| Feature | Points | Ligands | Support | Occupancy |
|---|---:|---:|---:|---:|
| Donor | 11 | 11 | 0.13 | 1.00 |
| LumpedHydrophobe | 9 | 9 | 0.11 | 1.00 |
| NegIonizable | 1 | 1 | 0.01 | 1.00 |

See `pharmacophore.json` (model), `features.csv` (raw points + cluster ids), and `raw_features_*.png` (per-family point distributions, each kept peak annotated with its label and support).