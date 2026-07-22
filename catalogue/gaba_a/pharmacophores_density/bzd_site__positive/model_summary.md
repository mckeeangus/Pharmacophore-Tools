# Pharmacophore — gaba_a/bzd_site__positive

- Ligands loaded: **3** (template=3)
- Skipped poses: 0
- Consensus method: `density`
- Representative ligand (viz): `6HUO_08H_D501`
- Features kept: **1**
- Excluded-volume spheres (receptor markers): **40**

**Support** = fraction of the cell's ligands that contribute to a feature (≤ 1.0; features are kept only above the 0.5 support floor). **Occupancy** = points ÷ contributing ligands (points-per-ligand, uncapped: > 1.0 when a cluster is denser than one point per ligand). One row per feature / peak.

| Feature | Points | Ligands | Support | Occupancy |
|---|---:|---:|---:|---:|
| Acceptor 1 | 4 | 3 | 1.00 | 1.33 |

## Feature resolution

Co-incident dual classifications collapsed by the feature hierarchy (higher-priority family kept on the shared atom); the listed ligands each carried both types on one atom.

| Kept ← dropped | Events | Ligands |
|---|---:|---|
| Aromatic ← LumpedHydrophobe | 6 | 6HUO_08H_D501, 6X3X_DZP_D404, 8VQY_A1ADG_E401 |

## Below the support/size floor

Clusters that formed but never became candidates — below the 0.5 support floor or the minimum cluster size.

| Feature | Points | Ligands | Support | Occupancy |
|---|---:|---:|---:|---:|
| Aromatic | 4 | 3 | 1.00 | 1.33 |
| Aromatic | 4 | 3 | 1.00 | 1.33 |
| Acceptor | 1 | 1 | 0.33 | 1.00 |

See `pharmacophore.json` (model), `features.csv` (raw points + cluster ids), and `raw_features_*.png` (per-family point distributions, each kept peak annotated with its label and support).