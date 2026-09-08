# Pharmacophore — cox2/seed_align

- Ligands loaded: **50** (template=3)
- Skipped poses: 0
- Consensus method: `density`
- Representative ligand (viz): `STK985630__p2`
- Features kept: **6**

> **Directional features (Acceptor, Donor) are low-confidence in this build (marked †).** Reconstructed from aligned poses, they inherit the docking pose/flip ambiguity — a correctly placed ring can present its H-bond atom in the wrong orientation. The cation/aromatic anchors are pose-invariant and trustworthy.

**Support** = fraction of the cell's ligands that contribute to a feature (≤ 1.0; features are kept only above the 0.5 support floor). **Occupancy** = points ÷ contributing ligands (points-per-ligand, uncapped: > 1.0 when a cluster is denser than one point per ligand). One row per feature / peak.

| Feature | Points | Ligands | Support | Occupancy |
|---|---:|---:|---:|---:|
| Aromatic 1 | 41 | 41 | 0.82 | 1.00 |
| Aromatic 2 | 41 | 41 | 0.82 | 1.00 |
| Donor 1 † | 44 | 44 | 0.88 | 1.00 |
| LumpedHydrophobe 1 | 40 | 40 | 0.80 | 1.00 |
| LumpedHydrophobe 2 | 33 | 31 | 0.62 | 1.06 |
| NegIonizable 1 | 38 | 38 | 0.76 | 1.00 |

## Below the support/size floor

Clusters that formed but never became candidates — below the 0.5 support floor or the minimum cluster size.

| Feature | Points | Ligands | Support | Occupancy |
|---|---:|---:|---:|---:|
| Acceptor | 16 | 13 | 0.26 | 1.23 |
| Aromatic | 4 | 4 | 0.08 | 1.00 |
| Aromatic | 4 | 4 | 0.08 | 1.00 |
| LumpedHydrophobe | 4 | 4 | 0.08 | 1.00 |
| Donor | 1 | 1 | 0.02 | 1.00 |
| Donor | 1 | 1 | 0.02 | 1.00 |
| NegIonizable | 1 | 1 | 0.02 | 1.00 |
| NegIonizable | 1 | 1 | 0.02 | 1.00 |

See `pharmacophore.json` (model), `features.csv` (raw points + cluster ids), and `raw_features_*.png` (per-family point distributions, each kept peak annotated with its label and support).