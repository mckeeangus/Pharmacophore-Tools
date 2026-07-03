# Pharmacophore — adrb2/orthosteric__neutral

- Ligands loaded: **3** (template=3)
- Skipped poses: 0
- Consensus method: `density`
- Representative ligand (viz): `8W1V_A1AE2_B1201`
- Features kept: **1**
- Excluded-volume spheres (receptor markers): **40**

Support is the fraction of the cell's ligands that contribute to a feature (one row per feature / peak; all features are kept only above the support floor).

| Feature | Points | Ligands | Support |
|---|---:|---:|---:|
| PosIonizable 1 | 3 | 3 | 1.00 |

## Feature resolution

Co-incident dual classifications collapsed by the feature hierarchy (higher-priority family kept on the shared atom); the listed ligands each carried both types on one atom.

| Kept ← dropped | Events | Ligands |
|---|---:|---|
| Aromatic ← LumpedHydrophobe | 5 | 6PS2_JTZ_A1201, 8W1V_A1AE2_B1201, 9W3F_BER_A1201 |
| PosIonizable ← Donor | 3 | 6PS2_JTZ_A1201, 8W1V_A1AE2_B1201 |

See `pharmacophore.json` (model), `features.csv` (raw points + cluster ids), and `raw_features_*.png` (per-family point distributions, each kept peak annotated with its label and support).