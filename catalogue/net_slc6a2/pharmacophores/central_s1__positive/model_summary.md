# Pharmacophore — net_slc6a2/central_s1__positive

- Ligands loaded: **6** (direct=3, template=3)
- Skipped poses: 0
- Consensus method: `kmeans`
- Representative ligand (viz): `8ZOY_LNR_A701`
- Features kept: **3**

**Support** = fraction of the cell's ligands that contribute to a feature (≤ 1.0; features are kept only above the 0.5 support floor). **Occupancy** = points ÷ contributing ligands (points-per-ligand, uncapped: > 1.0 when a cluster is denser than one point per ligand). One row per feature / peak.

| Feature | Points | Ligands | Support | Occupancy |
|---|---:|---:|---:|---:|
| Aromatic 1 | 4 | 4 | 0.67 | 1.00 |
| Donor 1 | 3 | 3 | 0.50 | 1.00 |
| PosIonizable 1 | 4 | 4 | 0.67 | 1.00 |

## Feature resolution

Co-incident dual classifications collapsed by the feature hierarchy (higher-priority family kept on the shared atom); the listed ligands each carried both types on one atom.

| Kept ← dropped | Events | Ligands |
|---|---:|---|
| Aromatic ← LumpedHydrophobe | 6 | 4XP1_LDP_A708, 4XP6_B40_A601, 4XP9_1WE_C706, 8WTV_E5E_A704, 8XB3_YMN_A701, 8ZOY_LNR_A701 |
| PosIonizable ← Donor | 5 | 4XP1_LDP_A708, 4XP6_B40_A601, 4XP9_1WE_C706, 8WTV_E5E_A704, 8ZOY_LNR_A701 |

## Merged away

Clusters that passed the support/size floor but were displaced by the 1 Å cross-family overlap merge — one feature per region, keeping the denser one. Each row states in favour of which kept feature it was removed.

| Feature | Points | Ligands | Support | Occupancy | In favour of |
|---|---:|---:|---:|---:|---|
| Acceptor | 3 | 3 | 0.50 | 1.00 | Donor 1 |

## Below the support/size floor

Clusters that formed but never became candidates — below the 0.5 support floor or the minimum cluster size.

| Feature | Points | Ligands | Support | Occupancy |
|---|---:|---:|---:|---:|
| PosIonizable | 3 | 2 | 0.33 | 1.50 |
| Donor | 2 | 2 | 0.33 | 1.00 |
| Donor | 2 | 2 | 0.33 | 1.00 |
| Acceptor | 2 | 2 | 0.33 | 1.00 |
| Acceptor | 2 | 2 | 0.33 | 1.00 |
| Aromatic | 2 | 2 | 0.33 | 1.00 |
| Donor | 1 | 1 | 0.17 | 1.00 |
| Acceptor | 1 | 1 | 0.17 | 1.00 |

See `pharmacophore.json` (model), `features.csv` (raw points + cluster ids), and `raw_features_*.png` (per-family point distributions, each kept peak annotated with its label and support).