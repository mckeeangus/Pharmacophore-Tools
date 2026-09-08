# Pharmacophore — cdk2

- Ligands loaded: **49** (sdf=49)
- Skipped poses: 0
- Consensus method: `density`
- Representative ligand (viz): `Z8462111514`
- Features kept: **3**

**Support** = fraction of the cell's ligands that contribute to a feature (≤ 1.0; features are kept only above the 0.5 support floor). **Occupancy** = points ÷ contributing ligands (points-per-ligand, uncapped: > 1.0 when a cluster is denser than one point per ligand). One row per feature / peak.

| Feature | Points | Ligands | Support | Occupancy |
|---|---:|---:|---:|---:|
| Acceptor 1 | 31 | 31 | 0.63 | 1.00 |
| Aromatic 1 | 30 | 27 | 0.55 | 1.11 |
| Donor 1 | 26 | 26 | 0.53 | 1.00 |

## Feature resolution

Co-incident dual classifications collapsed by the feature hierarchy (higher-priority family kept on the shared atom); the listed ligands each carried both types on one atom.

| Kept ← dropped | Events | Ligands |
|---|---:|---|
| NegIonizable ← Acceptor | 20 | MCULE-1747195129, MCULE-2334703321, MCULE-2687269303, MCULE-2752453438, MCULE-4193810350, MCULE-4920035048, MCULE-6110905834, MCULE-8219326142, MCULE-9373509363, Z8315143560 |
| PosIonizable ← Donor | 33 | MCULE-1390089024, MCULE-1528614132, MCULE-1747195129, MCULE-1966235308, MCULE-2334703321, MCULE-2683983486, MCULE-2687269303, MCULE-2752453438, MCULE-3368426694, MCULE-3438514248, MCULE-3957554977, MCULE-4134263693, MCULE-4193810350, MCULE-4920035048, MCULE-5517028926, MCULE-6110905834, MCULE-8219326142, MCULE-9139726948, MCULE-9373509363, MCULE-9624909007, Z5379192500, Z7684145496, Z8315143560, Z9061388696, Z9304513747, Z9304513756, Z9304515688 |

## Below the support/size floor

Clusters that formed but never became candidates — below the 0.5 support floor or the minimum cluster size.

| Feature | Points | Ligands | Support | Occupancy |
|---|---:|---:|---:|---:|
| LumpedHydrophobe | 24 | 24 | 0.49 | 1.00 |
| Aromatic | 23 | 23 | 0.47 | 1.00 |
| Acceptor | 28 | 22 | 0.45 | 1.27 |
| Aromatic | 22 | 22 | 0.45 | 1.00 |
| LumpedHydrophobe | 20 | 20 | 0.41 | 1.00 |
| Donor | 19 | 18 | 0.37 | 1.06 |
| Donor | 5 | 5 | 0.10 | 1.00 |
| Donor | 4 | 4 | 0.08 | 1.00 |
| NegIonizable | 3 | 3 | 0.06 | 1.00 |
| Acceptor | 2 | 2 | 0.04 | 1.00 |
| LumpedHydrophobe | 2 | 2 | 0.04 | 1.00 |
| PosIonizable | 2 | 2 | 0.04 | 1.00 |
| PosIonizable | 2 | 2 | 0.04 | 1.00 |
| PosIonizable | 2 | 2 | 0.04 | 1.00 |
| PosIonizable | 2 | 2 | 0.04 | 1.00 |
| Donor | 1 | 1 | 0.02 | 1.00 |
| Donor | 1 | 1 | 0.02 | 1.00 |
| Donor | 1 | 1 | 0.02 | 1.00 |
| Donor | 1 | 1 | 0.02 | 1.00 |
| Donor | 1 | 1 | 0.02 | 1.00 |
| Acceptor | 1 | 1 | 0.02 | 1.00 |
| Acceptor | 1 | 1 | 0.02 | 1.00 |
| Acceptor | 1 | 1 | 0.02 | 1.00 |
| Aromatic | 1 | 1 | 0.02 | 1.00 |
| Aromatic | 1 | 1 | 0.02 | 1.00 |
| Aromatic | 1 | 1 | 0.02 | 1.00 |
| LumpedHydrophobe | 1 | 1 | 0.02 | 1.00 |
| LumpedHydrophobe | 1 | 1 | 0.02 | 1.00 |
| LumpedHydrophobe | 1 | 1 | 0.02 | 1.00 |
| LumpedHydrophobe | 1 | 1 | 0.02 | 1.00 |
| LumpedHydrophobe | 1 | 1 | 0.02 | 1.00 |
| LumpedHydrophobe | 1 | 1 | 0.02 | 1.00 |
| LumpedHydrophobe | 1 | 1 | 0.02 | 1.00 |
| NegIonizable | 1 | 1 | 0.02 | 1.00 |
| NegIonizable | 1 | 1 | 0.02 | 1.00 |
| NegIonizable | 1 | 1 | 0.02 | 1.00 |
| NegIonizable | 1 | 1 | 0.02 | 1.00 |
| NegIonizable | 1 | 1 | 0.02 | 1.00 |
| NegIonizable | 1 | 1 | 0.02 | 1.00 |
| PosIonizable | 1 | 1 | 0.02 | 1.00 |
| PosIonizable | 1 | 1 | 0.02 | 1.00 |
| PosIonizable | 1 | 1 | 0.02 | 1.00 |
| PosIonizable | 1 | 1 | 0.02 | 1.00 |

See `pharmacophore.json` (model), `features.csv` (raw points + cluster ids), and `raw_features_*.png` (per-family point distributions, each kept peak annotated with its label and support).