# Pharmacophore — drd1/seed_align

- Ligands loaded: **50** (template=3)
- Skipped poses: 0
- Consensus method: `density`
- Representative ligand (viz): `Z1912620065__p3`
- Features kept: **4**

> **Directional features (Acceptor, Donor) are low-confidence in this build (marked †).** Reconstructed from aligned poses, they inherit the docking pose/flip ambiguity — a correctly placed ring can present its H-bond atom in the wrong orientation. The cation/aromatic anchors are pose-invariant and trustworthy.

**Support** = fraction of the cell's ligands that contribute to a feature (≤ 1.0; features are kept only above the 0.5 support floor). **Occupancy** = points ÷ contributing ligands (points-per-ligand, uncapped: > 1.0 when a cluster is denser than one point per ligand). One row per feature / peak.

| Feature | Points | Ligands | Support | Occupancy |
|---|---:|---:|---:|---:|
| Acceptor 1 † | 49 | 42 | 0.84 | 1.17 |
| Aromatic 1 | 46 | 39 | 0.78 | 1.18 |
| LumpedHydrophobe 1 | 28 | 28 | 0.56 | 1.00 |
| PosIonizable 1 | 27 | 27 | 0.54 | 1.00 |

## Below the support/size floor

Clusters that formed but never became candidates — below the 0.5 support floor or the minimum cluster size.

| Feature | Points | Ligands | Support | Occupancy |
|---|---:|---:|---:|---:|
| Acceptor | 23 | 23 | 0.46 | 1.00 |
| Donor | 18 | 18 | 0.36 | 1.00 |
| Donor | 17 | 17 | 0.34 | 1.00 |
| Donor | 14 | 14 | 0.28 | 1.00 |

See `pharmacophore.json` (model), `features.csv` (raw points + cluster ids), and `raw_features_*.png` (per-family point distributions, each kept peak annotated with its label and support).