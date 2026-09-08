# Pharmacophore — cdk2/seed_align

- Ligands loaded: **50** (direct=1, template=2)
- Skipped poses: 0
- Consensus method: `density`
- Representative ligand (viz): `Z4912279979__p1`
- Features kept: **2**

> **Directional features (Acceptor, Donor) are low-confidence in this build (marked †).** Reconstructed from aligned poses, they inherit the docking pose/flip ambiguity — a correctly placed ring can present its H-bond atom in the wrong orientation. The cation/aromatic anchors are pose-invariant and trustworthy.

**Support** = fraction of the cell's ligands that contribute to a feature (≤ 1.0; features are kept only above the 0.5 support floor). **Occupancy** = points ÷ contributing ligands (points-per-ligand, uncapped: > 1.0 when a cluster is denser than one point per ligand). One row per feature / peak.

| Feature | Points | Ligands | Support | Occupancy |
|---|---:|---:|---:|---:|
| Aromatic 1 | 30 | 30 | 0.60 | 1.00 |
| LumpedHydrophobe 1 | 30 | 30 | 0.60 | 1.00 |

## Below the support/size floor

Clusters that formed but never became candidates — below the 0.5 support floor or the minimum cluster size.

| Feature | Points | Ligands | Support | Occupancy |
|---|---:|---:|---:|---:|
| Acceptor | 25 | 24 | 0.48 | 1.04 |
| Acceptor | 25 | 22 | 0.44 | 1.14 |
| Donor | 22 | 20 | 0.40 | 1.10 |
| Aromatic | 22 | 20 | 0.40 | 1.10 |
| Acceptor | 19 | 18 | 0.36 | 1.06 |
| Aromatic | 17 | 16 | 0.32 | 1.06 |
| LumpedHydrophobe | 14 | 14 | 0.28 | 1.00 |
| Acceptor | 13 | 13 | 0.26 | 1.00 |
| Donor | 11 | 11 | 0.22 | 1.00 |
| Donor | 8 | 8 | 0.16 | 1.00 |
| NegIonizable | 4 | 4 | 0.08 | 1.00 |
| NegIonizable | 4 | 4 | 0.08 | 1.00 |
| PosIonizable | 4 | 4 | 0.08 | 1.00 |
| PosIonizable | 3 | 3 | 0.06 | 1.00 |
| PosIonizable | 3 | 3 | 0.06 | 1.00 |
| Aromatic | 1 | 1 | 0.02 | 1.00 |
| LumpedHydrophobe | 1 | 1 | 0.02 | 1.00 |
| NegIonizable | 1 | 1 | 0.02 | 1.00 |
| NegIonizable | 1 | 1 | 0.02 | 1.00 |
| PosIonizable | 1 | 1 | 0.02 | 1.00 |
| PosIonizable | 1 | 1 | 0.02 | 1.00 |
| PosIonizable | 1 | 1 | 0.02 | 1.00 |
| PosIonizable | 1 | 1 | 0.02 | 1.00 |
| PosIonizable | 1 | 1 | 0.02 | 1.00 |

See `pharmacophore.json` (model), `features.csv` (raw points + cluster ids), and `raw_features_*.png` (per-family point distributions, each kept peak annotated with its label and support).