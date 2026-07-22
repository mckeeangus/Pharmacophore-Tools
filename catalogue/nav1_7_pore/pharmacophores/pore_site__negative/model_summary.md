# Pharmacophore — nav1_7_pore/pore_site__negative

- Ligands loaded: **5** (template=5)
- Skipped poses: 0
- Consensus method: `kmeans`
- Representative ligand (viz): `8THH_IYJ_A2004`
- Features kept: **3**

**Support** = fraction of the cell's ligands that contribute to a feature (≤ 1.0; features are kept only above the 0.5 support floor). **Occupancy** = points ÷ contributing ligands (points-per-ligand, uncapped: > 1.0 when a cluster is denser than one point per ligand). One row per feature / peak.

| Feature | Points | Ligands | Support | Occupancy |
|---|---:|---:|---:|---:|
| Acceptor 1 | 8 | 5 | 1.00 | 1.60 |
| Aromatic 1 | 3 | 3 | 0.60 | 1.00 |
| Donor 1 | 4 | 3 | 0.60 | 1.33 |

## Feature resolution

Co-incident dual classifications collapsed by the feature hierarchy (higher-priority family kept on the shared atom); the listed ligands each carried both types on one atom.

| Kept ← dropped | Events | Ligands |
|---|---:|---|
| Aromatic ← LumpedHydrophobe | 5 | 8I5B_OJ0_A2021, 8S9B_LQO_A2003, 8S9C_N6W_A2003, 8THH_IYJ_A2004 |
| PosIonizable ← Donor | 1 | 8I5B_OJ0_A2021 |

## Below the support/size floor

Clusters that formed but never became candidates — below the 0.5 support floor or the minimum cluster size.

| Feature | Points | Ligands | Support | Occupancy |
|---|---:|---:|---:|---:|
| Acceptor | 3 | 2 | 0.40 | 1.50 |
| Donor | 2 | 2 | 0.40 | 1.00 |
| Aromatic | 2 | 2 | 0.40 | 1.00 |
| Acceptor | 2 | 1 | 0.20 | 2.00 |
| LumpedHydrophobe | 1 | 1 | 0.20 | 1.00 |
| PosIonizable | 1 | 1 | 0.20 | 1.00 |
| Aromatic | 1 | 1 | 0.20 | 1.00 |

See `pharmacophore.json` (model), `features.csv` (raw points + cluster ids), and `raw_features_*.png` (per-family point distributions, each kept peak annotated with its label and support).