# Pharmacophore — adora2a/orthosteric__neutral

- Ligands loaded: **5** (template=5)
- Skipped poses: 0
- Consensus method: `density`
- Representative ligand (viz): `8CIC_U30_A1202`
- Features kept: **2**
- Excluded-volume spheres (receptor markers): **40**

Support is the fraction of the cell's ligands that contribute to a feature (one row per feature / peak; all features are kept only above the support floor).

| Feature | Points | Ligands | Support |
|---|---:|---:|---:|
| Acceptor 1 | 20 | 5 | 1.00 |
| Donor 1 | 4 | 4 | 0.80 |

## Feature resolution

Co-incident dual classifications collapsed by the feature hierarchy (higher-priority family kept on the shared atom); the listed ligands each carried both types on one atom.

| Kept ← dropped | Events | Ligands |
|---|---:|---|
| Aromatic ← LumpedHydrophobe | 5 | 5OLH_9XT_A1201, 5OLO_9XW_A1201, 6GT3_F9Q_A2401, 8CIC_U30_A1202, 8RW0_JQ9_A1201 |
| PosIonizable ← Donor | 1 | 5OLO_9XW_A1201 |

See `pharmacophore.json` (model), `features.csv` (raw points + cluster ids), and `raw_features_*.png` (per-family point distributions, each kept peak annotated with its label and support).