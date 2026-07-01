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
| Donor 1 | 4 | 2 | 0.67 |
| LumpedHydrophobe 1 | 4 | 3 | 1.00 |
| PosIonizable 1 | 3 | 3 | 1.00 |

See `pharmacophore.json` (model), `features.csv` (raw points + cluster ids), and `raw_features_*.png` (per-family point distributions, each kept peak annotated with its label and support).