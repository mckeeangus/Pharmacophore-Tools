# Pharmacophore — adora2a/orthosteric__positive

- Ligands loaded: **6** (template=6)
- Skipped poses: 1 (8RLN_A1H1S_A1211:fail)
- Consensus method: `density`
- Representative ligand (viz): `5WF5_UKA_A1201`
- Features kept: **5**
- Excluded-volume spheres (receptor markers): **40**

**Support** = fraction of the cell's ligands that contribute to a feature (≤ 1.0; features are kept only above the 0.5 support floor). **Occupancy** = points ÷ contributing ligands (points-per-ligand, uncapped: > 1.0 when a cluster is denser than one point per ligand). One row per feature / peak.

| Feature | Points | Ligands | Support | Occupancy |
|---|---:|---:|---:|---:|
| Acceptor 1 | 7 | 6 | 1.00 | 1.17 |
| Aromatic 1 | 10 | 5 | 0.83 | 2.00 |
| Donor 1 | 6 | 6 | 1.00 | 1.00 |
| Donor 2 | 5 | 5 | 0.83 | 1.00 |
| PosIonizable 1 | 5 | 5 | 0.83 | 1.00 |

## Feature resolution

Co-incident dual classifications collapsed by the feature hierarchy (higher-priority family kept on the shared atom); the listed ligands each carried both types on one atom.

| Kept ← dropped | Events | Ligands |
|---|---:|---|
| Aromatic ← LumpedHydrophobe | 5 | 4UHR_NGI_A1320, 5WF5_UKA_A1201, 7ARO_RVZ_A1201, 8WDT_WCH_A1000 |
| NegIonizable ← Acceptor | 1 | 4UHR_NGI_A1320 |
| PosIonizable ← Donor | 3 | 5WF5_UKA_A1201, 7ARO_RVZ_A1201 |

## Below the support/size floor

Clusters that formed but never became candidates — below the 0.5 support floor or the minimum cluster size.

| Feature | Points | Ligands | Support | Occupancy |
|---|---:|---:|---:|---:|
| Donor | 3 | 3 | 0.50 | 1.00 |
| Aromatic | 2 | 2 | 0.33 | 1.00 |
| Donor | 1 | 1 | 0.17 | 1.00 |
| Acceptor | 1 | 1 | 0.17 | 1.00 |
| Acceptor | 1 | 1 | 0.17 | 1.00 |
| PosIonizable | 1 | 1 | 0.17 | 1.00 |
| PosIonizable | 1 | 1 | 0.17 | 1.00 |
| Aromatic | 1 | 1 | 0.17 | 1.00 |
| Aromatic | 1 | 1 | 0.17 | 1.00 |
| NegIonizable | 1 | 1 | 0.17 | 1.00 |

See `pharmacophore.json` (model), `features.csv` (raw points + cluster ids), and `raw_features_*.png` (per-family point distributions, each kept peak annotated with its label and support).