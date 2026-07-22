# Pharmacophore — esr1/lbp__positive

- Ligands loaded: **16** (direct=1, template=15)
- Skipped poses: 0
- Consensus method: `density`
- Representative ligand (viz): `9W12_A1ET8_A701`
- Features kept: **4**
- Excluded-volume spheres (receptor markers): **40**

**Support** = fraction of the cell's ligands that contribute to a feature (≤ 1.0; features are kept only above the 0.5 support floor). **Occupancy** = points ÷ contributing ligands (points-per-ligand, uncapped: > 1.0 when a cluster is denser than one point per ligand). One row per feature / peak.

| Feature | Points | Ligands | Support | Occupancy |
|---|---:|---:|---:|---:|
| Acceptor 1 | 18 | 10 | 0.62 | 1.80 |
| Aromatic 1 | 30 | 16 | 1.00 | 1.88 |
| Donor 1 | 20 | 16 | 1.00 | 1.25 |
| Donor 2 | 15 | 13 | 0.81 | 1.15 |

## Feature resolution

Co-incident dual classifications collapsed by the feature hierarchy (higher-priority family kept on the shared atom); the listed ligands each carried both types on one atom.

| Kept ← dropped | Events | Ligands |
|---|---:|---|
| Aromatic ← LumpedHydrophobe | 26 | 2B1V_458_B202, 2B1Z_17M_B202, 2QAB_EI1_B1, 2QSE_1HP_B1, 2QZO_KN1_B1, 4MG8_27J_A601, 4MGA_27L_B601, 4MGB_XDH_B601, 4TV1_36M_A601, 5TN4_7FZ_A601, 5TN5_7G0_B601, 7NEL_EST_A601, 7NFB_GEN_A601, 7RKE_5VP_B601, 9W11_ZHB_A701, 9W12_A1ET8_A701 |

## Merged away

Clusters that passed the support/size floor but were displaced by the 1 Å cross-family overlap merge — one feature per region, keeping the denser one. Each row states in favour of which kept feature it was removed.

| Feature | Points | Ligands | Support | Occupancy | In favour of |
|---|---:|---:|---:|---:|---|
| Acceptor | 19 | 16 | 1.00 | 1.19 | Donor 1 |
| Acceptor | 12 | 12 | 0.75 | 1.00 | Donor 2 |

## Below the support/size floor

Clusters that formed but never became candidates — below the 0.5 support floor or the minimum cluster size.

| Feature | Points | Ligands | Support | Occupancy |
|---|---:|---:|---:|---:|
| LumpedHydrophobe | 3 | 3 | 0.19 | 1.00 |
| PosIonizable | 1 | 1 | 0.06 | 1.00 |

See `pharmacophore.json` (model), `features.csv` (raw points + cluster ids), and `raw_features_*.png` (per-family point distributions, each kept peak annotated with its label and support).