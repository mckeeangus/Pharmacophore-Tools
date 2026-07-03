# Pharmacophore — net_slc6a2/central_s1__positive

- Ligands loaded: **6** (direct=3, template=3)
- Skipped poses: 0
- Consensus method: `kmeans`
- Representative ligand (viz): `8ZOY_LNR_A701`
- Features kept: **3**

Support is the fraction of the cell's ligands that contribute to a feature (one row per feature / peak; all features are kept only above the support floor).

| Feature | Points | Ligands | Support |
|---|---:|---:|---:|
| Aromatic 1 | 4 | 4 | 0.67 |
| Donor 1 | 3 | 3 | 0.50 |
| PosIonizable 1 | 4 | 4 | 0.67 |

## Feature resolution

Co-incident dual classifications collapsed by the feature hierarchy (higher-priority family kept on the shared atom); the listed ligands each carried both types on one atom.

| Kept ← dropped | Events | Ligands |
|---|---:|---|
| Aromatic ← LumpedHydrophobe | 6 | 4XP1_LDP_A708, 4XP6_B40_A601, 4XP9_1WE_C706, 8WTV_E5E_A704, 8XB3_YMN_A701, 8ZOY_LNR_A701 |
| PosIonizable ← Donor | 5 | 4XP1_LDP_A708, 4XP6_B40_A601, 4XP9_1WE_C706, 8WTV_E5E_A704, 8ZOY_LNR_A701 |

## Not selected

Clusters/peaks that formed but did not enter the model — below the support or size floor, or displaced by the cross-family overlap merge — with their mean support (fraction of the cell's ligands contributing).

| Feature | Points | Ligands | Mean support |
|---|---:|---:|---:|
| Acceptor | 3 | 3 | 0.50 |
| PosIonizable | 3 | 2 | 0.33 |
| Donor | 2 | 2 | 0.33 |
| Donor | 2 | 2 | 0.33 |
| Acceptor | 2 | 2 | 0.33 |
| Acceptor | 2 | 2 | 0.33 |
| Aromatic | 2 | 2 | 0.33 |
| Donor | 1 | 1 | 0.17 |
| Acceptor | 1 | 1 | 0.17 |

See `pharmacophore.json` (model), `features.csv` (raw points + cluster ids), and `raw_features_*.png` (per-family point distributions, each kept peak annotated with its label and support).