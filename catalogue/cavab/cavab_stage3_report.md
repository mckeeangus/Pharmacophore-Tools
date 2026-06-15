# Stage 3 — effect groups: cavab

_Generated 2026-06-15. Cell = (verified pocket) × (efficacy sign)._

- Poses carried from Stage 2: **6**
- In partition cells: **5** across **1** cells
- Routed to separate-state track: **0**
- Efficacy unknown (review): **0**
- Quarantined (not in pocket of interest): **1**

## Pocket verification

**Pockets found:** dhp_site (expected: dhp_site) — as expected

| Cluster | Label | Poses | Status | Consensus residues (sample) |
|--:|---|--:|---|---|
| 0 | dhp_site | 5 | assigned | GLU1165, GLY1164, ILE1199, LEU1163, PHE1167, PHE1171, THR1162, TYR1168 |
| 1 | _quarantined_ | 1 | quarantined | GLY1164, LEU1163, THR1162 |

_Notes: Central-cavity dihydropyridine drug site on the pore axis._

## Partition cells

| Cell (pocket × efficacy) | Poses | Distinct ligands | Example HETs |
|---|--:|--:|---|
| `dhp_site__negative` | 5 | 3 | 6U9, 6UB, 6UC |

## Separate-state ligands (routed out of cells)

**Separate-state:** none.

## Efficacy review list

**Unknown efficacy:** none.

## Quarantined poses

**Quarantined** (1):

- `G3P` (6JUH_G3P_C1305, primary) — candidate pocket: dhp_site

---

Cell mol2 sets: `groups/<pocket>__<efficacy>/`. Review sets: `review/{separate_state,unknown,quarantine}/`. Sessions: `cavab_grouped.pse` (all cells) and per-cell `.pse` in each folder.
