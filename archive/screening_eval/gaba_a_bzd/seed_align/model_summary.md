# Pharmacophore — gaba_a_bzd/seed_align

- Ligands loaded: **50** (template=3)
- Skipped poses: 0
- Consensus method: `density`
- Representative ligand (viz): `OSSL_640118__p1`
- Features kept: **0**

> **Directional features (Acceptor, Donor) are low-confidence in this build (marked †).** Reconstructed from aligned poses, they inherit the docking pose/flip ambiguity — a correctly placed ring can present its H-bond atom in the wrong orientation. The cation/aromatic anchors are pose-invariant and trustworthy.

**Support** = fraction of the cell's ligands that contribute to a feature (≤ 1.0; features are kept only above the 0.5 support floor). **Occupancy** = points ÷ contributing ligands (points-per-ligand, uncapped: > 1.0 when a cluster is denser than one point per ligand). One row per feature / peak.

| Feature | Points | Ligands | Support | Occupancy |
|---|---:|---:|---:|---:|

## Below the support/size floor

Clusters that formed but never became candidates — below the 0.5 support floor or the minimum cluster size.

| Feature | Points | Ligands | Support | Occupancy |
|---|---:|---:|---:|---:|
| Acceptor | 23 | 23 | 0.46 | 1.00 |
| Aromatic | 22 | 22 | 0.44 | 1.00 |
| LumpedHydrophobe | 22 | 22 | 0.44 | 1.00 |
| Donor | 19 | 19 | 0.38 | 1.00 |
| Aromatic | 15 | 15 | 0.30 | 1.00 |
| PosIonizable | 14 | 14 | 0.28 | 1.00 |
| Aromatic | 14 | 14 | 0.28 | 1.00 |
| LumpedHydrophobe | 14 | 14 | 0.28 | 1.00 |
| LumpedHydrophobe | 14 | 14 | 0.28 | 1.00 |
| Acceptor | 12 | 12 | 0.24 | 1.00 |
| Acceptor | 9 | 9 | 0.18 | 1.00 |
| Donor | 1 | 1 | 0.02 | 1.00 |
| NegIonizable | 1 | 1 | 0.02 | 1.00 |

See `pharmacophore.json` (model), `features.csv` (raw points + cluster ids), and `raw_features_*.png` (per-family point distributions, each kept peak annotated with its label and support).