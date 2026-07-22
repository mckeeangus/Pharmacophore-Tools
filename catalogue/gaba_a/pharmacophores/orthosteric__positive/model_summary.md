# Pharmacophore — gaba_a/orthosteric__positive

- Ligands loaded: **3** (template=3)
- Skipped poses: 0
- Consensus method: `kmeans`
- Representative ligand (viz): `7A5V_HSM_A5408`
- Features kept: **2**

**Support** = fraction of the cell's ligands that contribute to a feature (≤ 1.0; features are kept only above the 0.5 support floor). **Occupancy** = points ÷ contributing ligands (points-per-ligand, uncapped: > 1.0 when a cluster is denser than one point per ligand). One row per feature / peak.

| Feature | Points | Ligands | Support | Occupancy |
|---|---:|---:|---:|---:|
| Aromatic 1 | 2 | 2 | 0.67 | 1.00 |
| PosIonizable 1 | 4 | 2 | 0.67 | 2.00 |

## Feature resolution

Co-incident dual classifications collapsed by the feature hierarchy (higher-priority family kept on the shared atom); the listed ligands each carried both types on one atom.

| Kept ← dropped | Events | Ligands |
|---|---:|---|
| NegIonizable ← Acceptor | 1 | 9EQG_ABU_E3205 |
| PosIonizable ← Donor | 5 | 7A5V_HSM_A5408, 7QNC_EI7_B503, 9EQG_ABU_E3205 |

## Below the support/size floor

Clusters that formed but never became candidates — below the 0.5 support floor or the minimum cluster size.

| Feature | Points | Ligands | Support | Occupancy |
|---|---:|---:|---:|---:|
| PosIonizable | 1 | 1 | 0.33 | 1.00 |
| Donor | 1 | 1 | 0.33 | 1.00 |
| Acceptor | 1 | 1 | 0.33 | 1.00 |
| NegIonizable | 1 | 1 | 0.33 | 1.00 |

See `pharmacophore.json` (model), `features.csv` (raw points + cluster ids), and `raw_features_*.png` (per-family point distributions, each kept peak annotated with its label and support).