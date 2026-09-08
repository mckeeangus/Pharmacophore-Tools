# Pharmacophore — adora2a/seed_align

- Ligands loaded: **50** (direct=1, template=2)
- Skipped poses: 0
- Consensus method: `density`
- Representative ligand (viz): `Z52665462__p2`
- Features kept: **4**

> **Directional features (Acceptor, Donor) are low-confidence in this build (marked †).** Reconstructed from aligned poses, they inherit the docking pose/flip ambiguity — a correctly placed ring can present its H-bond atom in the wrong orientation. The cation/aromatic anchors are pose-invariant and trustworthy.

**Support** = fraction of the cell's ligands that contribute to a feature (≤ 1.0; features are kept only above the 0.5 support floor). **Occupancy** = points ÷ contributing ligands (points-per-ligand, uncapped: > 1.0 when a cluster is denser than one point per ligand). One row per feature / peak.

| Feature | Points | Ligands | Support | Occupancy |
|---|---:|---:|---:|---:|
| Acceptor 1 † | 32 | 29 | 0.58 | 1.10 |
| Acceptor 2 † | 31 | 31 | 0.62 | 1.00 |
| Aromatic 1 | 34 | 34 | 0.68 | 1.00 |
| LumpedHydrophobe 1 | 30 | 30 | 0.60 | 1.00 |

## Merged away

Clusters that passed the support/size floor but were displaced by the 1 Å cross-family overlap merge — one feature per region, keeping the denser one. Each row states in favour of which kept feature it was removed.

| Feature | Points | Ligands | Support | Occupancy | In favour of |
|---|---:|---:|---:|---:|---|
| Aromatic | 30 | 29 | 0.58 | 1.03 | Acceptor 1 |

## Below the support/size floor

Clusters that formed but never became candidates — below the 0.5 support floor or the minimum cluster size.

| Feature | Points | Ligands | Support | Occupancy |
|---|---:|---:|---:|---:|
| Acceptor | 21 | 21 | 0.42 | 1.00 |
| Donor | 20 | 20 | 0.40 | 1.00 |
| PosIonizable | 14 | 14 | 0.28 | 1.00 |
| Donor | 12 | 12 | 0.24 | 1.00 |
| LumpedHydrophobe | 12 | 12 | 0.24 | 1.00 |
| LumpedHydrophobe | 12 | 12 | 0.24 | 1.00 |
| Donor | 10 | 10 | 0.20 | 1.00 |
| Acceptor | 10 | 10 | 0.20 | 1.00 |
| PosIonizable | 10 | 10 | 0.20 | 1.00 |
| Acceptor | 2 | 2 | 0.04 | 1.00 |
| Aromatic | 2 | 2 | 0.04 | 1.00 |
| LumpedHydrophobe | 2 | 2 | 0.04 | 1.00 |

See `pharmacophore.json` (model), `features.csv` (raw points + cluster ids), and `raw_features_*.png` (per-family point distributions, each kept peak annotated with its label and support).