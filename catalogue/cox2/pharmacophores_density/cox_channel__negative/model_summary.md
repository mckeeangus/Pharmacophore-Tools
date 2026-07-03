# Pharmacophore — cox2/cox_channel__negative

- Ligands loaded: **5** (template=5)
- Skipped poses: 0
- Consensus method: `density`
- Representative ligand (viz): `5KIR_RCX_A601`
- Features kept: **2**
- Excluded-volume spheres (receptor markers): **40**

Support is the fraction of the cell's ligands that contribute to a feature (one row per feature / peak; all features are kept only above the support floor).

| Feature | Points | Ligands | Support |
|---|---:|---:|---:|
| Aromatic 1 | 5 | 5 | 1.00 |
| Aromatic 2 | 4 | 4 | 0.80 |

## Feature resolution

Co-incident dual classifications collapsed by the feature hierarchy (higher-priority family kept on the shared atom); the listed ligands each carried both types on one atom.

| Kept ← dropped | Events | Ligands |
|---|---:|---|
| Aromatic ← LumpedHydrophobe | 9 | 5F1A_SAL_A601, 5IKR_ID8_A601, 5IKT_TLF_B601, 5IKV_FLF_B601, 5KIR_RCX_A601 |
| NegIonizable ← Acceptor | 4 | 5F1A_SAL_A601, 5IKR_ID8_A601, 5IKT_TLF_B601, 5IKV_FLF_B601 |

## Not selected

Clusters/peaks that formed but did not enter the model — below the support or size floor, or displaced by the cross-family overlap merge — with their mean support (fraction of the cell's ligands contributing).

| Feature | Points | Ligands | Mean support |
|---|---:|---:|---:|
| Donor | 4 | 4 | 0.80 |
| NegIonizable | 4 | 4 | 0.80 |
| Acceptor | 2 | 1 | 0.20 |
| Acceptor | 2 | 1 | 0.20 |
| Acceptor | 1 | 1 | 0.20 |

See `pharmacophore.json` (model), `features.csv` (raw points + cluster ids), and `raw_features_*.png` (per-family point distributions, each kept peak annotated with its label and support).