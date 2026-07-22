# Pharmacophore — chrm2/orthosteric__negative

- Ligands loaded: **3** (template=3)
- Skipped poses: 0
- Consensus method: `kmeans`
- Representative ligand (viz): `5ZK3_QNB_A501`
- Features kept: **6**

**Support** = fraction of the cell's ligands that contribute to a feature (≤ 1.0; features are kept only above the 0.5 support floor). **Occupancy** = points ÷ contributing ligands (points-per-ligand, uncapped: > 1.0 when a cluster is denser than one point per ligand). One row per feature / peak.

| Feature | Points | Ligands | Support | Occupancy |
|---|---:|---:|---:|---:|
| Acceptor 1 | 5 | 3 | 1.00 | 1.67 |
| Acceptor 2 | 3 | 2 | 0.67 | 1.50 |
| Aromatic 1 | 3 | 3 | 1.00 | 1.00 |
| Aromatic 2 | 2 | 2 | 0.67 | 1.00 |
| Donor 1 | 3 | 3 | 1.00 | 1.00 |
| PosIonizable 1 | 3 | 3 | 1.00 | 1.00 |

## Feature resolution

Co-incident dual classifications collapsed by the feature hierarchy (higher-priority family kept on the shared atom); the listed ligands each carried both types on one atom.

| Kept ← dropped | Events | Ligands |
|---|---:|---|
| Aromatic ← LumpedHydrophobe | 4 | 5ZK3_QNB_A501, 5ZKB_82F_A1201, 5ZKC_3C0_A501 |
| PosIonizable ← Donor | 3 | 5ZK3_QNB_A501, 5ZKB_82F_A1201 |

## Below the support/size floor

Clusters that formed but never became candidates — below the 0.5 support floor or the minimum cluster size.

| Feature | Points | Ligands | Support | Occupancy |
|---|---:|---:|---:|---:|
| Acceptor | 2 | 1 | 0.33 | 2.00 |
| Donor | 1 | 1 | 0.33 | 1.00 |
| PosIonizable | 1 | 1 | 0.33 | 1.00 |

See `pharmacophore.json` (model), `features.csv` (raw points + cluster ids), and `raw_features_*.png` (per-family point distributions, each kept peak annotated with its label and support).