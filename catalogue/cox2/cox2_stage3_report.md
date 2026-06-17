# Stage 3 — effect groups: cox2

_Generated 2026-06-18. Cell = (verified pocket) × (efficacy sign)._

- Poses carried from Stage 2: **6**
- In partition cells: **5** across **1** cells
- Routed to separate-state track: **0**
- Efficacy unknown (review): **0**
- Quarantined (not in pocket of interest): **1**

## Pocket verification

**Pockets found:** cox_channel (expected: cox_channel) — as expected

| Cluster | Label | Poses | Status | Consensus residues (sample) |
|--:|---|--:|---|---|
| 0 | cox_channel | 5 | assigned | ALA527, ARG120, GLY526, LEU352, LEU359, LEU384, LEU531, MET522 |
| 1 | _quarantined_ | 1 | quarantined | ALA528, ARG121, GLY527, LEU353, LEU385, LEU532, MET523, PHE382 |

_Notes: Cyclooxygenase channel (the heme site is separate and was filtered out)._

## Partition cells

| Cell (pocket × efficacy) | Poses | Distinct ligands | Example HETs |
|---|--:|--:|---|
| `cox_channel__negative` | 5 | 5 | FLF, ID8, RCX, SAL, TLF |

## Separate-state ligands (routed out of cells)

**Separate-state:** none.

## Efficacy review list

**Unknown efficacy:** none.

## Quarantined poses

**Quarantined** (1):

- `JMS` (5IKQ_JMS_B602, primary) — candidate pocket: cox_channel

---

Cell mol2 sets: `groups/<pocket>__<efficacy>/` (one representative pose per ligand). Review sets: `review/{separate_state,unknown,quarantine}/`. Sessions: `cox2_grouped.pse` (all cells) and per-cell `.pse`. Pose pools: `datasets/all_poses/` (every kept pose) and `datasets/representative/` (one per ligand), each with a `.pml` + `.pse`.
