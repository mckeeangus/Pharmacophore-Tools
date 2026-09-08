# Pharmacophore — gaba_a_gaba/seed_align

- Ligands loaded: **49** (direct=2, template=1)
- Skipped poses: 0
- Consensus method: `density`
- Representative ligand (viz): `Z2522596660__p1`
- Features kept: **3**

> **Directional features (Acceptor, Donor) are low-confidence in this build (marked †).** Reconstructed from aligned poses, they inherit the docking pose/flip ambiguity — a correctly placed ring can present its H-bond atom in the wrong orientation. The cation/aromatic anchors are pose-invariant and trustworthy.

**Support** = fraction of the cell's ligands that contribute to a feature (≤ 1.0; features are kept only above the 0.5 support floor). **Occupancy** = points ÷ contributing ligands (points-per-ligand, uncapped: > 1.0 when a cluster is denser than one point per ligand). One row per feature / peak.

| Feature | Points | Ligands | Support | Occupancy |
|---|---:|---:|---:|---:|
| Acceptor 1 † | 39 | 34 | 0.69 | 1.15 |
| Aromatic 1 | 31 | 31 | 0.63 | 1.00 |
| PosIonizable 1 | 30 | 30 | 0.61 | 1.00 |

## Below the support/size floor

Clusters that formed but never became candidates — below the 0.5 support floor or the minimum cluster size.

| Feature | Points | Ligands | Support | Occupancy |
|---|---:|---:|---:|---:|
| Donor | 25 | 24 | 0.49 | 1.04 |
| NegIonizable | 15 | 15 | 0.31 | 1.00 |
| NegIonizable | 1 | 1 | 0.02 | 1.00 |

See `pharmacophore.json` (model), `features.csv` (raw points + cluster ids), and `raw_features_*.png` (per-family point distributions, each kept peak annotated with its label and support).