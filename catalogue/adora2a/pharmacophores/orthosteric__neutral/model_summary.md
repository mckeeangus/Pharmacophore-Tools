# Pharmacophore — adora2a/orthosteric__neutral

- Ligands loaded: **5** (template=5)
- Skipped poses: 0
- Consensus method: `density`
- Representative ligand (viz): `8CIC_U30_A1202`
- Features kept: **2**
- Excluded-volume spheres (receptor markers): **40**

**Support** = fraction of the cell's ligands that contribute to a feature (≤ 1.0; features are kept only above the 0.5 support floor). **Occupancy** = points ÷ contributing ligands (points-per-ligand, uncapped: > 1.0 when a cluster is denser than one point per ligand). One row per feature / peak.

| Feature | Points | Ligands | Support | Occupancy |
|---|---:|---:|---:|---:|
| Aromatic 1 | 5 | 4 | 0.80 | 1.25 |
| Donor 1 | 4 | 4 | 0.80 | 1.00 |

## Feature resolution

Co-incident dual classifications collapsed by the feature hierarchy (higher-priority family kept on the shared atom); the listed ligands each carried both types on one atom.

| Kept ← dropped | Events | Ligands |
|---|---:|---|
| Aromatic ← LumpedHydrophobe | 5 | 5OLH_9XT_A1201, 5OLO_9XW_A1201, 6GT3_F9Q_A2401, 8CIC_U30_A1202, 8RW0_JQ9_A1201 |
| PosIonizable ← Donor | 1 | 5OLO_9XW_A1201 |

## Below the support/size floor

Clusters that formed but never became candidates — below the 0.5 support floor or the minimum cluster size.

| Feature | Points | Ligands | Support | Occupancy |
|---|---:|---:|---:|---:|
| Acceptor | 2 | 2 | 0.40 | 1.00 |
| Donor | 1 | 1 | 0.20 | 1.00 |
| Donor | 1 | 1 | 0.20 | 1.00 |
| Donor | 1 | 1 | 0.20 | 1.00 |
| Acceptor | 1 | 1 | 0.20 | 1.00 |
| PosIonizable | 1 | 1 | 0.20 | 1.00 |
| PosIonizable | 1 | 1 | 0.20 | 1.00 |
| Acceptor | 0 | 0 | 0.00 | 0.00 |
| Aromatic | 0 | 0 | 0.00 | 0.00 |

See `pharmacophore.json` (model), `features.csv` (raw points + cluster ids), and `raw_features_*.png` (per-family point distributions, each kept peak annotated with its label and support).