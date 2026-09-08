# Pharmacophore — ache

- Ligands loaded: **50** (sdf=50)
- Skipped poses: 0
- Consensus method: `density`
- Representative ligand (viz): `OSSM_117313`
- Features kept: **6**

**Support** = fraction of the cell's ligands that contribute to a feature (≤ 1.0; features are kept only above the 0.5 support floor). **Occupancy** = points ÷ contributing ligands (points-per-ligand, uncapped: > 1.0 when a cluster is denser than one point per ligand). One row per feature / peak.

| Feature | Points | Ligands | Support | Occupancy |
|---|---:|---:|---:|---:|
| Acceptor 1 | 37 | 37 | 0.74 | 1.00 |
| Acceptor 2 | 33 | 33 | 0.66 | 1.00 |
| Aromatic 1 | 44 | 44 | 0.88 | 1.00 |
| Aromatic 2 | 27 | 27 | 0.54 | 1.00 |
| LumpedHydrophobe 1 | 43 | 43 | 0.86 | 1.00 |
| PosIonizable 1 | 34 | 34 | 0.68 | 1.00 |

## Feature resolution

Co-incident dual classifications collapsed by the feature hierarchy (higher-priority family kept on the shared atom); the listed ligands each carried both types on one atom.

| Kept ← dropped | Events | Ligands |
|---|---:|---|
| PosIonizable ← Donor | 70 | MCULE-2169066108, MCULE-2451548413, MCULE-2656552248, MCULE-4412719064, MCULE-5121538438, MCULE-5760115115, MCULE-6708544121, MCULE-7397041861, MCULE-7606492205, MCULE-7731031692, MCULE-9049988220, MCULE-9416529564, MCULE-9960679025, OSSM_025582, OSSM_029404, OSSM_114841, OSSM_117313, OSSM_165332, OSSM_168027, OSSM_359540, S420-0307, S420-0610, STK038806, STK085425, STK095172, STK589147, STK597514, STK601271, STK605378, STK606127, STK614783, STK614978, STK616659, STL018562, STL349826, Y511-6540, Z1535677966, Z1741977105, Z4244368765, Z4493401842, Z4493401875, Z4493402112, Z4493402179, Z4493402181, Z4493402195, Z4580714056, Z85145044, Z8679812633, Z90651290, Z999693592 |

## Below the support/size floor

Clusters that formed but never became candidates — below the 0.5 support floor or the minimum cluster size.

| Feature | Points | Ligands | Support | Occupancy |
|---|---:|---:|---:|---:|
| LumpedHydrophobe | 21 | 21 | 0.42 | 1.00 |
| Acceptor | 5 | 5 | 0.10 | 1.00 |
| LumpedHydrophobe | 5 | 5 | 0.10 | 1.00 |
| Donor | 4 | 4 | 0.08 | 1.00 |
| Donor | 4 | 4 | 0.08 | 1.00 |
| PosIonizable | 3 | 3 | 0.06 | 1.00 |
| Acceptor | 1 | 1 | 0.02 | 1.00 |
| PosIonizable | 1 | 1 | 0.02 | 1.00 |
| PosIonizable | 1 | 1 | 0.02 | 1.00 |
| Donor | 1 | 1 | 0.02 | 1.00 |
| Donor | 1 | 1 | 0.02 | 1.00 |

See `pharmacophore.json` (model), `features.csv` (raw points + cluster ids), and `raw_features_*.png` (per-family point distributions, each kept peak annotated with its label and support).