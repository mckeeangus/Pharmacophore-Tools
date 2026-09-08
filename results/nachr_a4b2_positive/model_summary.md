# Pharmacophore — nachr_a4b2_positive

- Ligands loaded: **39** (sdf=39)
- Skipped poses: 0
- Consensus method: `density`
- Representative ligand (viz): `H050-0001`
- Features kept: **3**

**Support** = fraction of the cell's ligands that contribute to a feature (≤ 1.0; features are kept only above the 0.5 support floor). **Occupancy** = points ÷ contributing ligands (points-per-ligand, uncapped: > 1.0 when a cluster is denser than one point per ligand). One row per feature / peak.

| Feature | Points | Ligands | Support | Occupancy |
|---|---:|---:|---:|---:|
| Acceptor 1 | 39 | 39 | 1.00 | 1.00 |
| Aromatic 1 | 39 | 39 | 1.00 | 1.00 |
| PosIonizable 1 | 39 | 39 | 1.00 | 1.00 |

## Feature resolution

Co-incident dual classifications collapsed by the feature hierarchy (higher-priority family kept on the shared atom); the listed ligands each carried both types on one atom.

| Kept ← dropped | Events | Ligands |
|---|---:|---|
| PosIonizable ← Donor | 48 | 3690-1011, FCG1837466864, H050-0001, MCULE-1517104178, MCULE-1931732981, MCULE-2253838370, MCULE-2640903763, MCULE-3270971174, MCULE-4609409020, MCULE-8195682194, MCULE-8695927329, MCULE-9140680577, MCULE-9278696945, OSSK_435001, OSSL_789650, OSSM_091763, STK051267, STL146319, STL553215, STL562305, Z1198150037, Z1198172584, Z1209979984, Z1558572494, Z1993626917, Z2240803613, Z2298167235, Z2373839498, Z2380440630, Z2517097759, Z3235143301, Z3243815051, Z3379559298, Z3770428479, Z5331825334, Z5872843793, Z9308261204, Z9478993253 |

## Below the support/size floor

Clusters that formed but never became candidates — below the 0.5 support floor or the minimum cluster size.

| Feature | Points | Ligands | Support | Occupancy |
|---|---:|---:|---:|---:|
| LumpedHydrophobe | 2 | 2 | 0.05 | 1.00 |

See `pharmacophore.json` (model), `features.csv` (raw points + cluster ids), and `raw_features_*.png` (per-family point distributions, each kept peak annotated with its label and support).