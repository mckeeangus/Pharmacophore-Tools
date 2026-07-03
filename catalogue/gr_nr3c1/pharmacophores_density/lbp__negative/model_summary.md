# Pharmacophore — gr_nr3c1/lbp__negative

- Ligands loaded: **3** (template=3)
- Skipped poses: 0
- Consensus method: `density`
- Representative ligand (viz): `4MDD_29M_B801`
- Features kept: **2**
- Excluded-volume spheres (receptor markers): **40**

Support is the fraction of the cell's ligands that contribute to a feature (one row per feature / peak; all features are kept only above the support floor).

| Feature | Points | Ligands | Support |
|---|---:|---:|---:|
| Aromatic 1 | 6 | 3 | 1.00 |
| Donor 1 | 4 | 3 | 1.00 |

## Feature resolution

Co-incident dual classifications collapsed by the feature hierarchy (higher-priority family kept on the shared atom); the listed ligands each carried both types on one atom.

| Kept ← dropped | Events | Ligands |
|---|---:|---|
| Aromatic ← LumpedHydrophobe | 5 | 4MDD_29M_B801, 5UC3_486_B801, 6DXK_HJ4_A801 |
| PosIonizable ← Donor | 1 | 4MDD_29M_B801 |

## Not selected

Clusters/peaks that formed but did not enter the model — below the support or size floor, or displaced by the cross-family overlap merge — with their mean support (fraction of the cell's ligands contributing).

| Feature | Points | Ligands | Mean support |
|---|---:|---:|---:|
| Acceptor | 4 | 3 | 1.00 |
| Acceptor | 2 | 2 | 0.67 |
| LumpedHydrophobe | 2 | 2 | 0.67 |
| LumpedHydrophobe | 2 | 2 | 0.67 |
| Acceptor | 2 | 1 | 0.33 |
| PosIonizable | 1 | 1 | 0.33 |

See `pharmacophore.json` (model), `features.csv` (raw points + cluster ids), and `raw_features_*.png` (per-family point distributions, each kept peak annotated with its label and support).