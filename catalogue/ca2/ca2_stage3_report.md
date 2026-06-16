# Stage 3 — effect groups: ca2

_Generated 2026-06-16. Cell = (verified pocket) × (efficacy sign)._

- Poses carried from Stage 2: **100**
- In partition cells: **87** across **1** cells
- Routed to separate-state track: **12**
- Efficacy unknown (review): **0**
- Quarantined (not in pocket of interest): **1**

## Pocket verification

**Pockets found:** active_site (expected: active_site) — as expected

| Cluster | Label | Poses | Status | Consensus residues (sample) |
|--:|---|--:|---|---|
| 0 | active_site | 99 | assigned | GLN92, GLU106, HIS119, HIS94, HIS96, LEU198, PHE131, SER197 |
| 1 | _quarantined_ | 1 | quarantined | GLN90, GLU104, HIS117, HIS62, HIS92, HIS94, ILE89, LEU138 |

_Notes: Catalytic zinc / active-site funnel._

## Partition cells

| Cell (pocket × efficacy) | Poses | Distinct ligands | Example HETs |
|---|--:|--:|---|
| `active_site__negative` | 87 | 76 | 0VV, 0VW, 0VX, 0VY, 0VZ, 25X … |

## Separate-state ligands (routed out of cells)

**Separate-state** (12):

- `BCT` (3U7C_BCT_A303, primary) — catalytic product (bicarbonate)
- `BCT` (6KLZ_BCT_A303, primary) — catalytic product (bicarbonate)
- `BCT` (6KM0_BCT_A303, primary) — catalytic product (bicarbonate)
- `BCT` (6KM1_BCT_A304, primary) — catalytic product (bicarbonate)
- `BCT` (6KM2_BCT_A304, primary) — catalytic product (bicarbonate)
- `CO2` (3D92_CO2_A301, primary) — catalytic substrate (CO2)
- `CO2` (3D93_CO2_A301, primary) — catalytic substrate (CO2)
- `CO2` (3U7C_CO2_A301, primary) — catalytic substrate (CO2)
- `CO2` (5Y2R_CO2_A302, primary) — catalytic substrate (CO2)
- `CO2` (5Y2S_CO2_A302, primary) — catalytic substrate (CO2)
- `CO2` (6KM1_CO2_A305, primary) — catalytic substrate (CO2)
- `CO2` (6KM2_CO2_A305, primary) — catalytic substrate (CO2)

## Efficacy review list

**Unknown efficacy:** none.

## Quarantined poses

**Quarantined** (1):

- `Q3E` (6YZT_Q3E_A302, primary) — candidate pocket: active_site

---

Cell mol2 sets: `groups/<pocket>__<efficacy>/` (one representative pose per ligand). Review sets: `review/{separate_state,unknown,quarantine}/`. Sessions: `ca2_grouped.pse` (all cells) and per-cell `.pse`. Pose pools: `datasets/all_poses/` (every kept pose) and `datasets/representative/` (one per ligand), each with a `.pml` + `.pse`.
