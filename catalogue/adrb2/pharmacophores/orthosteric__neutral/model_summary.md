# Pharmacophore — adrb2/orthosteric__neutral

- Ligands loaded: **3** (template=3)
- Skipped poses: 0
- Consensus method: `kmeans`
- Representative ligand (viz): `8W1V_A1AE2_B1201`
- Features kept: **5**

Support is the fraction of the cell's ligands that contribute to a feature (one row per feature / peak; all features are kept only above the support floor).

| Feature | Points | Ligands | Support |
|---|---:|---:|---:|
| Acceptor 1 | 6 | 3 | 1.00 |
| Acceptor 2 | 4 | 2 | 0.67 |
| Donor 1 | 2 | 2 | 0.67 |
| LumpedHydrophobe 1 | 2 | 2 | 0.67 |
| PosIonizable 1 | 3 | 3 | 1.00 |

## Feature resolution

Co-incident dual classifications collapsed by the feature hierarchy (higher-priority family kept on the shared atom); the listed ligands each carried both types on one atom.

| Kept ← dropped | Events | Ligands |
|---|---:|---|
| Aromatic ← LumpedHydrophobe | 5 | 6PS2_JTZ_A1201, 8W1V_A1AE2_B1201, 9W3F_BER_A1201 |
| PosIonizable ← Donor | 3 | 6PS2_JTZ_A1201, 8W1V_A1AE2_B1201 |

## Not selected

Clusters/peaks that formed but did not enter the model — below the support or size floor, or displaced by the cross-family overlap merge — with their mean support (fraction of the cell's ligands contributing).

| Feature | Points | Ligands | Mean support |
|---|---:|---:|---:|
| Aromatic | 3 | 3 | 1.00 |
| Aromatic | 4 | 2 | 0.67 |
| Acceptor | 2 | 1 | 0.33 |
| Donor | 1 | 1 | 0.33 |
| PosIonizable | 1 | 1 | 0.33 |

See `pharmacophore.json` (model), `features.csv` (raw points + cluster ids), and `raw_features_*.png` (per-family point distributions, each kept peak annotated with its label and support).