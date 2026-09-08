# Pharmacophore — hmgcr

- Ligands loaded: **50** (sdf=50)
- Skipped poses: 0
- Consensus method: `density`
- Representative ligand (viz): `V030-1754`
- Features kept: **10**

**Support** = fraction of the cell's ligands that contribute to a feature (≤ 1.0; features are kept only above the 0.5 support floor). **Occupancy** = points ÷ contributing ligands (points-per-ligand, uncapped: > 1.0 when a cluster is denser than one point per ligand). One row per feature / peak.

| Feature | Points | Ligands | Support | Occupancy |
|---|---:|---:|---:|---:|
| Acceptor 1 | 45 | 45 | 0.90 | 1.00 |
| Acceptor 2 | 39 | 39 | 0.78 | 1.00 |
| Aromatic 1 | 43 | 43 | 0.86 | 1.00 |
| Aromatic 2 | 39 | 39 | 0.78 | 1.00 |
| Donor 1 | 42 | 42 | 0.84 | 1.00 |
| Donor 2 | 38 | 38 | 0.76 | 1.00 |
| Donor 3 | 36 | 36 | 0.72 | 1.00 |
| LumpedHydrophobe 1 | 44 | 44 | 0.88 | 1.00 |
| LumpedHydrophobe 2 | 27 | 27 | 0.54 | 1.00 |
| NegIonizable 1 | 37 | 37 | 0.74 | 1.00 |

## Feature resolution

Co-incident dual classifications collapsed by the feature hierarchy (higher-priority family kept on the shared atom); the listed ligands each carried both types on one atom.

| Kept ← dropped | Events | Ligands |
|---|---:|---|
| NegIonizable ← Acceptor | 100 | FCG223613171, FCG2296016965, FCG2296052867, STL458084, STL534049, STL541517, STL545808, V004-9878, V005-3120, V005-3132, V005-3144, V005-3154, V005-3202, V005-5095, V007-7694, V007-7712, V007-7729, V007-7738, V007-7762, V007-7764, V007-7771, V007-7784, V008-1848, V025-9447, V027-2568, V027-3760, V027-3772, V027-3799, V027-3820, V027-3902, V027-3903, V027-3914, V027-3952, V027-6137, V027-7724, V027-7761, V027-7822, V028-1587, V028-1648, V029-4999, V029-9694, V030-1729, V030-1754, V030-1764, V030-1765, V030-1799, Y042-8054, Y042-8055, Z223223430, Z2295663126 |
| PosIonizable ← Donor | 4 | FCG223613171, Z223223430 |
| PosIonizable ← LumpedHydrophobe | 2 | FCG223613171, Z223223430 |

## Below the support/size floor

Clusters that formed but never became candidates — below the 0.5 support floor or the minimum cluster size.

| Feature | Points | Ligands | Support | Occupancy |
|---|---:|---:|---:|---:|
| LumpedHydrophobe | 23 | 23 | 0.46 | 1.00 |
| Acceptor | 22 | 22 | 0.44 | 1.00 |
| LumpedHydrophobe | 15 | 15 | 0.30 | 1.00 |
| Acceptor | 14 | 14 | 0.28 | 1.00 |
| LumpedHydrophobe | 2 | 2 | 0.04 | 1.00 |
| PosIonizable | 2 | 2 | 0.04 | 1.00 |

See `pharmacophore.json` (model), `features.csv` (raw points + cluster ids), and `raw_features_*.png` (per-family point distributions, each kept peak annotated with its label and support).