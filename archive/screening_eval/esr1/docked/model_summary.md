# Pharmacophore — esr1/docked

- Ligands loaded: **1000** (direct=85, template=915)
- Skipped poses: 0
- Consensus method: `density`
- Representative ligand (viz): `Z57122655__p4`
- Features kept: **4**

**Support** = fraction of the cell's ligands that contribute to a feature (≤ 1.0; features are kept only above the 0.5 support floor). **Occupancy** = points ÷ contributing ligands (points-per-ligand, uncapped: > 1.0 when a cluster is denser than one point per ligand). One row per feature / peak.

| Feature | Points | Ligands | Support | Occupancy |
|---|---:|---:|---:|---:|
| Acceptor 1 | 653 | 653 | 0.65 | 1.00 |
| Aromatic 1 | 963 | 921 | 0.92 | 1.05 |
| Donor 1 | 671 | 671 | 0.67 | 1.00 |
| LumpedHydrophobe 1 | 893 | 893 | 0.89 | 1.00 |

## Feature resolution

Co-incident dual classifications collapsed by the feature hierarchy (higher-priority family kept on the shared atom); the listed ligands each carried both types on one atom.

| Kept ← dropped | Events | Ligands |
|---|---:|---|
| NegIonizable ← Acceptor | 22 | 8010-3908__p3, 8018-7212__p1, FCG2960642690__p1, OSSK_862262__p1, OSSL_312877__p1, OSSL_799773__p1, OSSM_007475__p7, OSSM_132853__p2, OSSM_330405__p3, STK045122__p1, STK664124__p1, Z2311627398__p2, Z3017825680__p3, Z355286690__p3, Z4477941235__p2, Z5020304500__p3, Z5356926257__p3, Z56921814__p1, Z9569553296__p2 |
| PosIonizable ← Donor | 155 | 0199-0139__p1, 6930-0037__p4, 8004-6615__p3, 8014-9350__p4, D210-0008__p4, FCG2850780141__p3, MCULE-9926015888__p2, OSSK_034897__p1, OSSK_091758__p4, OSSK_106000__p3, OSSK_293965__p8, OSSK_328418__p3, OSSK_404282__p1, OSSK_483907__p1, OSSK_557067__p9, OSSK_636394__p3, OSSK_800840__p1, OSSL_118279__p2, OSSL_304286__p1, OSSL_312915__p1, OSSL_328675__p5, OSSL_645321__p4, OSSL_745674__p9, OSSL_799773__p1, OSSM_007475__p7, OSSM_132853__p2, OSSM_235375__p1, OSSM_265832__p1, OSSM_277424__p1, OSSM_330405__p3, OSSM_335993__p1, STK099283__p1, STK100200__p4, STK538021__p1, STK682036__p4, STK768321__p1, STK840143__p6, STK856460__p1, STK888285__p1, STK888294__p1, STK943798__p1, STK995781__p1, STL034146__p2, STL338596__p1, STL369650__p1, STL512084__p4, STL522710__p4, STL558004__p1, Y510-9498__p1, Z1021595596__p1, Z1491384068__p7, Z1505702194__p2, Z1575344353__p1, Z1615987200__p6, Z1884112192__p2, Z1978166560__p3, Z2180011388__p3, Z220358226__p1, Z2347654474__p1, Z234809846__p4, Z2351421152__p7, Z2568587997__p4, Z2723038127__p1, Z2748120970__p1, Z276557792__p6, Z286066022__p1, Z3018642594__p1, Z3234877418__p1, Z3446459971__p1, Z44306290__p1, Z4477941235__p2, Z4497298517__p2, Z4562301813__p3, Z48847305__p1, Z48858350__p1, Z5020304292__p2, Z5020304823__p3, Z5020305524__p7, Z5020306075__p2, Z5020306635__p1, Z5020307598__p4, Z5020307765__p2, Z5356926257__p3, Z5397881883__p7, Z56877935__p5, Z56921814__p1, Z56983122__p4, Z57122655__p4, Z600416096__p5, Z648617410__p4, Z7165653335__p8, Z7268012804__p2, Z8341357351__p1, Z8426832521__p2, Z8592435007__p1, Z8794927884__p1, Z8922382709__p4, Z9339800463__p3, Z9485322278__p2, Z991569498__p1 |
| PosIonizable ← LumpedHydrophobe | 6 | OSSM_343454__p1, STL146979__p1, Z1496559703__p4, Z1527392498__p1, Z2940294639__p1, Z8773063478__p2 |

## Below the support/size floor

Clusters that formed but never became candidates — below the 0.5 support floor or the minimum cluster size.

| Feature | Points | Ligands | Support | Occupancy |
|---|---:|---:|---:|---:|
| LumpedHydrophobe | 388 | 348 | 0.35 | 1.11 |
| Acceptor | 128 | 123 | 0.12 | 1.04 |
| PosIonizable | 46 | 44 | 0.04 | 1.05 |
| Donor | 36 | 36 | 0.04 | 1.00 |
| NegIonizable | 5 | 5 | 0.01 | 1.00 |
| NegIonizable | 4 | 4 | 0.00 | 1.00 |
| NegIonizable | 3 | 3 | 0.00 | 1.00 |
| NegIonizable | 1 | 1 | 0.00 | 1.00 |

See `pharmacophore.json` (model), `features.csv` (raw points + cluster ids), and `raw_features_*.png` (per-family point distributions, each kept peak annotated with its label and support).