# Pharmacophore — adrb2/seed_align

- Ligands loaded: **50** (template=3)
- Skipped poses: 0
- Consensus method: `density`
- Representative ligand (viz): `Z1262591397__p6`
- Features kept: **6**

> **Directional features (Acceptor, Donor) are low-confidence in this build (marked †).** Reconstructed from aligned poses, they inherit the docking pose/flip ambiguity — a correctly placed ring can present its H-bond atom in the wrong orientation. The cation/aromatic anchors are pose-invariant and trustworthy.

**Support** = fraction of the cell's ligands that contribute to a feature (≤ 1.0; features are kept only above the 0.5 support floor). **Occupancy** = points ÷ contributing ligands (points-per-ligand, uncapped: > 1.0 when a cluster is denser than one point per ligand). One row per feature / peak.

| Feature | Points | Ligands | Support | Occupancy |
|---|---:|---:|---:|---:|
| Acceptor 1 † | 31 | 31 | 0.62 | 1.00 |
| Acceptor 2 † | 29 | 27 | 0.54 | 1.07 |
| Aromatic 1 | 52 | 50 | 1.00 | 1.04 |
| Donor 1 † | 32 | 30 | 0.60 | 1.07 |
| Donor 2 † | 29 | 29 | 0.58 | 1.00 |
| LumpedHydrophobe 1 | 52 | 50 | 1.00 | 1.04 |

## Below the support/size floor

Clusters that formed but never became candidates — below the 0.5 support floor or the minimum cluster size.

| Feature | Points | Ligands | Support | Occupancy |
|---|---:|---:|---:|---:|
| PosIonizable | 24 | 22 | 0.44 | 1.09 |
| NegIonizable | 10 | 3 | 0.06 | 3.33 |
| PosIonizable | 1 | 1 | 0.02 | 1.00 |
| PosIonizable | 1 | 1 | 0.02 | 1.00 |
| NegIonizable | 1 | 1 | 0.02 | 1.00 |

See `pharmacophore.json` (model), `features.csv` (raw points + cluster ids), and `raw_features_*.png` (per-family point distributions, each kept peak annotated with its label and support).