# Pharmacophore — adrb2

- Ligands loaded: **50** (sdf=50)
- Skipped poses: 0
- Consensus method: `density`
- Representative ligand (viz): `Z955123630`
- Features kept: **7**

**Support** = fraction of the cell's ligands that contribute to a feature (≤ 1.0; features are kept only above the 0.5 support floor). **Occupancy** = points ÷ contributing ligands (points-per-ligand, uncapped: > 1.0 when a cluster is denser than one point per ligand). One row per feature / peak.

| Feature | Points | Ligands | Support | Occupancy |
|---|---:|---:|---:|---:|
| Acceptor 1 | 52 | 50 | 1.00 | 1.04 |
| Acceptor 2 | 29 | 27 | 0.54 | 1.07 |
| Aromatic 1 | 51 | 49 | 0.98 | 1.04 |
| Donor 1 | 52 | 50 | 1.00 | 1.04 |
| Donor 2 | 32 | 29 | 0.58 | 1.10 |
| LumpedHydrophobe 1 | 52 | 50 | 1.00 | 1.04 |
| PosIonizable 1 | 50 | 48 | 0.96 | 1.04 |

## Feature resolution

Co-incident dual classifications collapsed by the feature hierarchy (higher-priority family kept on the shared atom); the listed ligands each carried both types on one atom.

| Kept ← dropped | Events | Ligands |
|---|---:|---|
| NegIonizable ← Acceptor | 16 | Z1556051334, Z2050038784, Z3071621361, Z955123630 |
| PosIonizable ← Donor | 61 | FCG2435177302, FCG2445467333, FCG2447641612, FCG2447674341, FCG3364299245, FCG3364299252, FCG928091309, FCG928091315, FCG928091479, FCG928091505, FCG928091521, OSSL_312470, OSSL_478049, OSSL_882694, OSSL_962902, OSSM_129722, OSSM_304587, STK618645, STK759203, STK803113, STL301903, STL377784, Z1198155517, Z1259339888, Z1262591397, Z1262658266, Z1556051334, Z1741977143, Z1815149210, Z203038576, Z2050038784, Z220327456, Z2301287926, Z2574937385, Z2752645466, Z295456854, Z3071621361, Z3215375352, Z3221821579, Z3324923673, Z3498594783, Z4119887033, Z4437707719, Z4574899614, Z4971220652, Z5219061923, Z56836691, Z57102382, Z9108933277, Z955123630 |

## Below the support/size floor

Clusters that formed but never became candidates — below the 0.5 support floor or the minimum cluster size.

| Feature | Points | Ligands | Support | Occupancy |
|---|---:|---:|---:|---:|
| NegIonizable | 13 | 4 | 0.08 | 3.25 |
| LumpedHydrophobe | 5 | 4 | 0.08 | 1.25 |

See `pharmacophore.json` (model), `features.csv` (raw points + cluster ids), and `raw_features_*.png` (per-family point distributions, each kept peak annotated with its label and support).