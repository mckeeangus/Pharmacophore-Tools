# Pharmacophore — chrm2/orthosteric__negative

- Ligands loaded: **3** (template=3)
- Skipped poses: 0
- Consensus method: `density`
- Representative ligand (viz): `5ZKB_82F_A1201`
- Features kept: **3**
- Excluded-volume spheres (receptor markers): **40**

Support is the fraction of the cell's ligands that contribute to a feature (one row per feature / peak; all features are kept only above the support floor).

| Feature | Points | Ligands | Support |
|---|---:|---:|---:|
| Acceptor 1 | 10 | 3 | 1.00 |
| Aromatic 1 | 3 | 3 | 1.00 |
| PosIonizable 1 | 4 | 3 | 1.00 |

## Feature resolution

Co-incident dual classifications collapsed by the feature hierarchy (higher-priority family kept on the shared atom); the listed ligands each carried both types on one atom.

| Kept ← dropped | Events | Ligands |
|---|---:|---|
| Aromatic ← LumpedHydrophobe | 4 | 5ZK3_QNB_A501, 5ZKB_82F_A1201, 5ZKC_3C0_A501 |
| PosIonizable ← Donor | 3 | 5ZK3_QNB_A501, 5ZKB_82F_A1201 |

## Not selected

Clusters/peaks that formed but did not enter the model — below the support or size floor, or displaced by the cross-family overlap merge — with their mean support (fraction of the cell's ligands contributing).

| Feature | Points | Ligands | Mean support |
|---|---:|---:|---:|
| Donor | 3 | 3 | 1.00 |
| Aromatic | 2 | 2 | 0.67 |
| Donor | 1 | 1 | 0.33 |

See `pharmacophore.json` (model), `features.csv` (raw points + cluster ids), and `raw_features_*.png` (per-family point distributions, each kept peak annotated with its label and support).