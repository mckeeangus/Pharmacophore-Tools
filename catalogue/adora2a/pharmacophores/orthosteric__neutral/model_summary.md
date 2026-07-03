# Pharmacophore — adora2a/orthosteric__neutral

- Ligands loaded: **5** (template=5)
- Skipped poses: 0
- Consensus method: `kmeans`
- Representative ligand (viz): `8CIC_U30_A1202`
- Features kept: **5**

Support is the fraction of the cell's ligands that contribute to a feature (one row per feature / peak; all features are kept only above the support floor).

| Feature | Points | Ligands | Support |
|---|---:|---:|---:|
| Acceptor 1 | 7 | 5 | 1.00 |
| Acceptor 2 | 6 | 5 | 1.00 |
| Aromatic 1 | 12 | 5 | 1.00 |
| Aromatic 2 | 4 | 3 | 0.60 |
| Donor 1 | 5 | 4 | 0.80 |

## Feature resolution

Co-incident dual classifications collapsed by the feature hierarchy (higher-priority family kept on the shared atom); the listed ligands each carried both types on one atom.

| Kept ← dropped | Events | Ligands |
|---|---:|---|
| Aromatic ← LumpedHydrophobe | 5 | 5OLH_9XT_A1201, 5OLO_9XW_A1201, 6GT3_F9Q_A2401, 8CIC_U30_A1202, 8RW0_JQ9_A1201 |
| PosIonizable ← Donor | 1 | 5OLO_9XW_A1201 |

## Not selected

Clusters/peaks that formed but did not enter the model — below the support or size floor, or displaced by the cross-family overlap merge — with their mean support (fraction of the cell's ligands contributing).

| Feature | Points | Ligands | Mean support |
|---|---:|---:|---:|
| Acceptor | 5 | 5 | 1.00 |
| Acceptor | 4 | 2 | 0.40 |
| Donor | 2 | 2 | 0.40 |
| Acceptor | 2 | 2 | 0.40 |
| PosIonizable | 2 | 2 | 0.40 |
| Acceptor | 1 | 1 | 0.20 |

See `pharmacophore.json` (model), `features.csv` (raw points + cluster ids), and `raw_features_*.png` (per-family point distributions, each kept peak annotated with its label and support).