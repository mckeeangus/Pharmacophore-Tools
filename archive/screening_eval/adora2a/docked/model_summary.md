# Pharmacophore — adora2a/docked

- Ligands loaded: **1000** (direct=155, template=845)
- Skipped poses: 0
- Consensus method: `density`
- Representative ligand (viz): `Z1193296653__p1`
- Features kept: **1**

**Support** = fraction of the cell's ligands that contribute to a feature (≤ 1.0; features are kept only above the 0.5 support floor). **Occupancy** = points ÷ contributing ligands (points-per-ligand, uncapped: > 1.0 when a cluster is denser than one point per ligand). One row per feature / peak.

| Feature | Points | Ligands | Support | Occupancy |
|---|---:|---:|---:|---:|
| Aromatic 1 | 640 | 551 | 0.55 | 1.16 |

## Feature resolution

Co-incident dual classifications collapsed by the feature hierarchy (higher-priority family kept on the shared atom); the listed ligands each carried both types on one atom.

| Kept ← dropped | Events | Ligands |
|---|---:|---|
| NegIonizable ← Acceptor | 10 | FCG55911495__p6, MCULE-5568419083__p3, OSSM_279014__p7, STK871674__p6, STL132409__p2, Z3064666386__p2, Z55521754__p6, Z9477617871__p1 |
| PosIonizable ← Donor | 94 | E726-0062__p9, F813-0106__p2, FCG1689517393__p2, FCG55911495__p6, FCG646800715__p3, M503-1598__p1, M503-1888__p2, M503-1889__p4, M503-1892__p1, MCULE-4484987949__p1, MCULE-5389391722__p2, MCULE-5999694150__p4, MCULE-7733321387__p3, OSSK_983278__p1, OSSL_921933__p1, OSSL_921946__p4, OSSL_921951__p4, OSSL_921952__p1, OSSM_090629__p4, OSSM_183302__p3, OSSM_267791__p1, OSSM_279014__p7, STK009273__p1, STK618193__p1, STK804407__p3, STK854892__p1, STL132363__p4, STL132364__p1, STL132365__p1, STL167635__p3, STL167639__p1, STL167640__p4, STL167641__p1, Y600-2839__p1, Z1172970972__p4, Z1225464734__p2, Z1343316418__p1, Z1434154375__p3, Z1434156576__p2, Z1449993178__p6, Z1450023803__p6, Z1450031871__p2, Z1689127652__p2, Z1770253642__p1, Z1779811624__p1, Z1883197912__p1, Z1895052803__p1, Z193535310__p3, Z224610476__p1, Z27332683__p1, Z3075443514__p6, Z3268555165__p2, Z3333528020__p4, Z4002430149__p3, Z4131950844__p1, Z4233485298__p1, Z4238487743__p4, Z4312448510__p1, Z4518256527__p2, Z5004880598__p1, Z52660414__p1, Z52665462__p2, Z52665806__p3, Z55521754__p6, Z644931974__p1, Z646410974__p3, Z7228327968__p3, Z9006000524__p1, Z9477617871__p1 |
| PosIonizable ← LumpedHydrophobe | 3 | Z193535310__p3, Z224610476__p1, Z4518256527__p2 |

## Below the support/size floor

Clusters that formed but never became candidates — below the 0.5 support floor or the minimum cluster size.

| Feature | Points | Ligands | Support | Occupancy |
|---|---:|---:|---:|---:|
| Acceptor | 428 | 398 | 0.40 | 1.08 |
| Donor | 322 | 322 | 0.32 | 1.00 |
| Donor | 254 | 251 | 0.25 | 1.01 |
| LumpedHydrophobe | 171 | 171 | 0.17 | 1.00 |
| LumpedHydrophobe | 144 | 144 | 0.14 | 1.00 |
| LumpedHydrophobe | 146 | 140 | 0.14 | 1.04 |
| PosIonizable | 51 | 51 | 0.05 | 1.00 |
| PosIonizable | 21 | 21 | 0.02 | 1.00 |
| NegIonizable | 2 | 2 | 0.00 | 1.00 |
| NegIonizable | 2 | 2 | 0.00 | 1.00 |
| NegIonizable | 1 | 1 | 0.00 | 1.00 |
| NegIonizable | 1 | 1 | 0.00 | 1.00 |

See `pharmacophore.json` (model), `features.csv` (raw points + cluster ids), and `raw_features_*.png` (per-family point distributions, each kept peak annotated with its label and support).