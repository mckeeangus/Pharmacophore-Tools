# Pharmacophore — adora2a/orthosteric__positive

- Ligands loaded: **6** (template=6)
- Skipped poses: 1 (8RLN_A1H1S_A1211:fail)
- Consensus method: `density`
- Representative ligand (viz): `5WF5_UKA_A1201`
- Features kept: **3**
- Excluded-volume spheres (receptor markers): **40**

Support is the fraction of the cell's ligands that contribute to a feature (one row per feature / peak; all features are kept only above the support floor).

| Feature | Points | Ligands | Support |
|---|---:|---:|---:|
| Acceptor 1 | 20 | 5 | 0.83 |
| Acceptor 2 | 19 | 6 | 1.00 |
| PosIonizable 1 | 5 | 5 | 0.83 |

## Feature resolution

Co-incident dual classifications collapsed by the feature hierarchy (higher-priority family kept on the shared atom); the listed ligands each carried both types on one atom.

| Kept ← dropped | Events | Ligands |
|---|---:|---|
| Aromatic ← LumpedHydrophobe | 5 | 4UHR_NGI_A1320, 5WF5_UKA_A1201, 7ARO_RVZ_A1201, 8WDT_WCH_A1000 |
| NegIonizable ← Acceptor | 1 | 4UHR_NGI_A1320 |
| PosIonizable ← Donor | 3 | 5WF5_UKA_A1201, 7ARO_RVZ_A1201 |

## Not selected

Clusters/peaks that formed but did not enter the model — below the support or size floor, or displaced by the cross-family overlap merge — with their mean support (fraction of the cell's ligands contributing).

| Feature | Points | Ligands | Mean support |
|---|---:|---:|---:|
| Aromatic | 12 | 6 | 1.00 |
| Donor | 7 | 6 | 1.00 |
| Donor | 10 | 5 | 0.83 |
| Donor | 4 | 4 | 0.67 |
| Aromatic | 4 | 4 | 0.67 |
| Donor | 3 | 1 | 0.17 |
| Acceptor | 1 | 1 | 0.17 |
| PosIonizable | 1 | 1 | 0.17 |
| PosIonizable | 1 | 1 | 0.17 |
| Aromatic | 1 | 1 | 0.17 |
| Aromatic | 1 | 1 | 0.17 |
| NegIonizable | 1 | 1 | 0.17 |

See `pharmacophore.json` (model), `features.csv` (raw points + cluster ids), and `raw_features_*.png` (per-family point distributions, each kept peak annotated with its label and support).