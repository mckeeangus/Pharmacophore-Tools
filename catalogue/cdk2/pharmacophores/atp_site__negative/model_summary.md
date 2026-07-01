# Pharmacophore — cdk2/atp_site__negative

- Ligands loaded: **87** (direct=4, template=83)
- Skipped poses: 5 (7SA0_8KQ_A305:fail, 8FP0_RRC_A303:fail, 9JJ5_A1EB0_A301:fail, 9UAU_A1EOM_A301:fail, 9UGF_A1EO5_A301:fail)
- Consensus method: `kmeans`
- Representative ligand (viz): `1H00_FAP_A1300`
- Features kept: **3**

Support is the fraction of the cell's ligands that contribute to a feature (one row per feature / peak; all features are kept only above the support floor).

| Feature | Points | Ligands | Support |
|---|---:|---:|---:|
| Acceptor 1 | 218 | 86 | 0.99 |
| Acceptor 2 | 91 | 55 | 0.63 |
| Donor 1 | 71 | 70 | 0.80 |

See `pharmacophore.json` (model), `features.csv` (raw points + cluster ids), and `raw_features_*.png` (per-family point distributions, each kept peak annotated with its label and support).