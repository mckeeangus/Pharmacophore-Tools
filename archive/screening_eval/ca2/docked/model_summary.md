# Pharmacophore — ca2/docked

- Ligands loaded: **1000** (direct=361, template=639)
- Skipped poses: 0
- Consensus method: `density`
- Representative ligand (viz): `Z285136922__p1`
- Features kept: **0**

**Support** = fraction of the cell's ligands that contribute to a feature (≤ 1.0; features are kept only above the 0.5 support floor). **Occupancy** = points ÷ contributing ligands (points-per-ligand, uncapped: > 1.0 when a cluster is denser than one point per ligand). One row per feature / peak.

| Feature | Points | Ligands | Support | Occupancy |
|---|---:|---:|---:|---:|

## Feature resolution

Co-incident dual classifications collapsed by the feature hierarchy (higher-priority family kept on the shared atom); the listed ligands each carried both types on one atom.

| Kept ← dropped | Events | Ligands |
|---|---:|---|
| NegIonizable ← Acceptor | 26 | FCG1445171457__p2, FCG1455701916__p1, FCG44785004__p3, J023-0461__p2, MCULE-1848428330__p5, MCULE-2775606256__p1, MCULE-8104835082__p1, STK636100__p4, STK985429__p1, STK985467__p2, STK985510__p4, Z1455312175__p1, Z2723092069__p2, Z44395263__p1, Z5409106842__p8 |
| PosIonizable ← Donor | 189 | 8014-9736__p2, 8014-9747__p2, D364-1250__p1, D364-1320__p2, D364-1321__p1, D364-1402__p1, D364-1416__p1, D364-1495__p3, D364-1602__p1, G016-1189__p1, J023-0053__p4, J023-0071__p1, J023-0187__p1, J023-0191__p2, J023-0328__p1, J023-0337__p7, J023-0407__p6, J023-0411__p2, M980-0106__p2, MCULE-1579459332__p8, MCULE-6360538479__p2, OSSK_297164__p4, OSSK_633393__p1, OSSK_853952__p2, OSSK_853976__p1, OSSK_934007__p9, OSSL_645565__p1, OSSL_682753__p1, OSSM_010946__p1, OSSM_025374__p4, OSSM_044781__p1, OSSM_075633__p1, OSSM_135043__p1, OSSM_145177__p1, OSSM_319446__p5, P590-0565__p1, SB18-0341__p1, STK201870__p1, STK505526__p1, STK561452__p1, STK571492__p8, STK581468__p1, STK636100__p4, STK657267__p3, STK844043__p5, STK867088__p1, STK942856__p1, STL046207__p1, STL170700__p1, STL261528__p6, STL304638__p1, STL583184__p1, STL583187__p1, STL583481__p1, Y505-7018__p3, Y507-4959__p2, Z1041019566__p3, Z104524498__p1, Z1117758086__p2, Z1123357939__p2, Z1123384177__p6, Z1245135478__p1, Z1255361267__p3, Z1255362476__p5, Z1291065383__p4, Z1441746596__p1, Z1528722698__p2, Z1629036979__p1, Z1728199334__p1, Z17792216__p4, Z1921678945__p4, Z196107964__p7, Z2224108332__p1, Z22755830__p1, Z2708759799__p1, Z28292915__p4, Z285136922__p1, Z30926332__p1, Z3756270692__p1, Z384751656__p1, Z384755464__p1, Z384757836__p5, Z384913862__p3, Z4444470649__p1, Z4690854379__p4, Z55525495__p2, Z55525582__p1, Z55526079__p3, Z56782744__p5, Z56785957__p1, Z56792823__p4, Z637289610__p1, Z637292076__p1, Z637293504__p3, Z637298690__p3, Z637304222__p2, Z637304226__p1, Z729307008__p1, Z729937000__p7, Z732446696__p8, Z822540956__p1, Z8405392544__p7, Z9305664281__p1, Z9331621033__p6 |
| PosIonizable ← LumpedHydrophobe | 59 | 7682-0102__p1, 8020-2136__p2, D053-0467__p2, D212-0165__p1, D718-0216__p7, J023-0206__p1, MCULE-7667184495__p2, MCULE-9162415915__p1, OSSK_633393__p1, OSSK_676281__p1, OSSK_983719__p2, OSSL_258358__p7, OSSL_322115__p1, OSSM_010946__p1, OSSM_071493__p1, OSSM_073841__p2, OSSM_137396__p1, OSSM_145177__p1, STK201870__p1, STK263098__p2, STK499220__p7, STK561452__p1, STK936757__p1, STL046207__p1, STL300480__p1, STL304638__p1, Z1041019566__p3, Z1245135478__p1, Z1291065383__p4, Z1441746596__p1, Z1528722698__p2, Z1609322323__p1, Z1629036979__p1, Z1728199334__p1, Z1921678945__p4, Z2228617434__p1, Z384751656__p1, Z384755464__p1, Z384757836__p5, Z384913862__p3, Z4690854379__p4, Z55525495__p2, Z55525582__p1, Z55526079__p3, Z55527360__p6, Z56771527__p2, Z56782744__p5, Z56792823__p4, Z637289610__p1, Z637292076__p1, Z637293504__p3, Z637298690__p3, Z637304222__p2, Z637304226__p1, Z729307008__p1, Z729937000__p7, Z7689451577__p1, Z818810220__p1, Z822540956__p1 |

## Below the support/size floor

Clusters that formed but never became candidates — below the 0.5 support floor or the minimum cluster size.

| Feature | Points | Ligands | Support | Occupancy |
|---|---:|---:|---:|---:|
| Acceptor | 481 | 445 | 0.45 | 1.08 |
| Aromatic | 391 | 378 | 0.38 | 1.03 |
| Aromatic | 356 | 339 | 0.34 | 1.05 |
| LumpedHydrophobe | 275 | 275 | 0.28 | 1.00 |
| Donor | 215 | 210 | 0.21 | 1.02 |
| LumpedHydrophobe | 203 | 203 | 0.20 | 1.00 |
| Aromatic | 174 | 171 | 0.17 | 1.02 |
| LumpedHydrophobe | 130 | 130 | 0.13 | 1.00 |
| PosIonizable | 37 | 37 | 0.04 | 1.00 |
| NegIonizable | 5 | 5 | 0.01 | 1.00 |
| NegIonizable | 4 | 4 | 0.00 | 1.00 |
| PosIonizable | 1 | 1 | 0.00 | 1.00 |
| Aromatic | 1 | 1 | 0.00 | 1.00 |
| LumpedHydrophobe | 1 | 1 | 0.00 | 1.00 |
| NegIonizable | 1 | 1 | 0.00 | 1.00 |

See `pharmacophore.json` (model), `features.csv` (raw points + cluster ids), and `raw_features_*.png` (per-family point distributions, each kept peak annotated with its label and support).