# Pharmacophore — drd1

- Ligands loaded: **50** (sdf=50)
- Skipped poses: 0
- Consensus method: `density`
- Representative ligand (viz): `Z2312594102`
- Features kept: **5**

**Support** = fraction of the cell's ligands that contribute to a feature (≤ 1.0; features are kept only above the 0.5 support floor). **Occupancy** = points ÷ contributing ligands (points-per-ligand, uncapped: > 1.0 when a cluster is denser than one point per ligand). One row per feature / peak.

| Feature | Points | Ligands | Support | Occupancy |
|---|---:|---:|---:|---:|
| Acceptor 1 | 59 | 48 | 0.96 | 1.23 |
| Acceptor 2 | 28 | 28 | 0.56 | 1.00 |
| Aromatic 1 | 43 | 43 | 0.86 | 1.00 |
| Donor 1 | 29 | 29 | 0.58 | 1.00 |
| LumpedHydrophobe 1 | 40 | 40 | 0.80 | 1.00 |

## Feature resolution

Co-incident dual classifications collapsed by the feature hierarchy (higher-priority family kept on the shared atom); the listed ligands each carried both types on one atom.

| Kept ← dropped | Events | Ligands |
|---|---:|---|
| PosIonizable ← Donor | 60 | 8012-9271, 8015-2101, FCG2878104926, FCG2879657833, FCG2880127876, FCG2946094125, FCG2947887977, FCG3559872553, MCULE-1064508720, MCULE-1296496099, MCULE-1995617555, MCULE-3005884355, MCULE-3716360067, MCULE-4357750750, MCULE-4411896303, MCULE-4460325065, MCULE-4554608817, MCULE-4880777263, MCULE-5351999624, MCULE-6052560004, MCULE-6364997021, MCULE-6774338267, MCULE-7309126653, MCULE-8173341992, MCULE-8317582243, OSSK_467174, OSSK_860993, OSSL_639641, OSSL_941018, OSSM_044765, OSSM_120554, OSSM_336093, STK632659, STK657641, STL032978, STL426080, STL520190, STL520269, Z1317909945, Z1317932814, Z1623981649, Z1912578086, Z1912620065, Z1993819341, Z204712526, Z2312594102, Z3522831516, Z56801208 |

## Below the support/size floor

Clusters that formed but never became candidates — below the 0.5 support floor or the minimum cluster size.

| Feature | Points | Ligands | Support | Occupancy |
|---|---:|---:|---:|---:|
| PosIonizable | 24 | 24 | 0.48 | 1.00 |
| Donor | 22 | 22 | 0.44 | 1.00 |
| Acceptor | 6 | 6 | 0.12 | 1.00 |
| Aromatic | 4 | 4 | 0.08 | 1.00 |
| PosIonizable | 1 | 1 | 0.02 | 1.00 |
| PosIonizable | 1 | 1 | 0.02 | 1.00 |
| LumpedHydrophobe | 1 | 1 | 0.02 | 1.00 |

See `pharmacophore.json` (model), `features.csv` (raw points + cluster ids), and `raw_features_*.png` (per-family point distributions, each kept peak annotated with its label and support).