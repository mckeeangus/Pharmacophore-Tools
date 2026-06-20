# Stage 3 — effect groups: nav1_7_pore

_Generated 2026-06-20. Cell = (verified pocket) × (efficacy sign)._

- Poses carried from Stage 2: **13**
- In partition cells: **13** across **1** cells
- Routed to separate-state track: **0**
- Efficacy unknown (review): **0**
- Quarantined (not in pocket of interest): **0**

## Pocket verification

**Pockets found:** pore_site (expected: pore_site) — as expected

| Cluster | Label | Poses | Status | Consensus residues (sample) |
|--:|---|--:|---|---|
| 0 | pore_site | 13 | assigned | ALA402, GLN410, GLU406, ILE1453, ILE1457, ILE1759, LEU398, LEU960 |

_Notes: Single central-cavity / local-anaesthetic pore site. As with the VSD4 slug, cross-construct numbering fragments the clusters, so they are merged._

## Partition cells

| Cell (pocket × efficacy) | Poses | Distinct ligands | Example HETs |
|---|--:|--:|---|
| `pore_site__negative` | 13 | 5 | 9Z9, IYJ, LQO, N6W, OJ0 |

## Separate-state ligands (routed out of cells)

**Separate-state:** none.

## Efficacy review list

**Unknown efficacy:** none.

## Quarantined poses

**Quarantined:** none.

---

Cell mol2 sets: `groups/<pocket>__<efficacy>/` (one representative pose per ligand). Review sets: `review/{separate_state,unknown,quarantine}/`. Sessions: `nav1_7_pore_grouped.pse` (all cells) and per-cell `.pse`. Pose pools: `datasets/all_poses/` (every kept pose) and `datasets/representative/` (one per ligand), each with a `.pml` + `.pse`.
