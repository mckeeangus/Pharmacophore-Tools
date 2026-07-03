# Pharmacophore — gaba_a/orthosteric__positive

- Ligands loaded: **3** (template=3)
- Skipped poses: 0
- Consensus method: `kmeans`
- Representative ligand (viz): `7A5V_HSM_A5408`
- Features kept: **2**

Support is the fraction of the cell's ligands that contribute to a feature (one row per feature / peak; all features are kept only above the support floor).

| Feature | Points | Ligands | Support |
|---|---:|---:|---:|
| Aromatic 1 | 2 | 2 | 0.67 |
| PosIonizable 1 | 4 | 2 | 0.67 |

## Feature resolution

Co-incident dual classifications collapsed by the feature hierarchy (higher-priority family kept on the shared atom); the listed ligands each carried both types on one atom.

| Kept ← dropped | Events | Ligands |
|---|---:|---|
| NegIonizable ← Acceptor | 1 | 9EQG_ABU_E3205 |
| PosIonizable ← Donor | 5 | 7A5V_HSM_A5408, 7QNC_EI7_B503, 9EQG_ABU_E3205 |

## Not selected

Clusters/peaks that formed but did not enter the model — below the support or size floor, or displaced by the cross-family overlap merge — with their mean support (fraction of the cell's ligands contributing).

| Feature | Points | Ligands | Mean support |
|---|---:|---:|---:|
| PosIonizable | 1 | 1 | 0.33 |
| Donor | 1 | 1 | 0.33 |
| Acceptor | 1 | 1 | 0.33 |
| NegIonizable | 1 | 1 | 0.33 |

See `pharmacophore.json` (model), `features.csv` (raw points + cluster ids), and `raw_features_*.png` (per-family point distributions, each kept peak annotated with its label and support).