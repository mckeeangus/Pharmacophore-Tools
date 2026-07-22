# Pharmacophore — cox2/cox_channel__negative

- Ligands loaded: **5** (template=5)
- Skipped poses: 0
- Consensus method: `density`
- Representative ligand (viz): `5IKR_ID8_A601`
- Features kept: **4**
- Excluded-volume spheres (receptor markers): **40**

**Support** = fraction of the cell's ligands that contribute to a feature (≤ 1.0; features are kept only above the 0.5 support floor). **Occupancy** = points ÷ contributing ligands (points-per-ligand, uncapped: > 1.0 when a cluster is denser than one point per ligand). One row per feature / peak.

| Feature | Points | Ligands | Support | Occupancy |
|---|---:|---:|---:|---:|
| Aromatic 1 | 5 | 5 | 1.00 | 1.00 |
| Aromatic 2 | 3 | 3 | 0.60 | 1.00 |
| Donor 1 | 3 | 3 | 0.60 | 1.00 |
| NegIonizable 1 | 3 | 3 | 0.60 | 1.00 |

## Feature resolution

Co-incident dual classifications collapsed by the feature hierarchy (higher-priority family kept on the shared atom); the listed ligands each carried both types on one atom.

| Kept ← dropped | Events | Ligands |
|---|---:|---|
| Aromatic ← LumpedHydrophobe | 9 | 5F1A_SAL_A601, 5IKR_ID8_A601, 5IKT_TLF_B601, 5IKV_FLF_B601, 5KIR_RCX_A601 |
| NegIonizable ← Acceptor | 4 | 5F1A_SAL_A601, 5IKR_ID8_A601, 5IKT_TLF_B601, 5IKV_FLF_B601 |

## Below the support/size floor

Clusters that formed but never became candidates — below the 0.5 support floor or the minimum cluster size.

| Feature | Points | Ligands | Support | Occupancy |
|---|---:|---:|---:|---:|
| Acceptor | 2 | 1 | 0.20 | 2.00 |
| Acceptor | 2 | 1 | 0.20 | 2.00 |
| Acceptor | 1 | 1 | 0.20 | 1.00 |

See `pharmacophore.json` (model), `features.csv` (raw points + cluster ids), and `raw_features_*.png` (per-family point distributions, each kept peak annotated with its label and support).