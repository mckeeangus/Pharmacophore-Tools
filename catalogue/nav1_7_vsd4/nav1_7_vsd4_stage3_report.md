# Stage 3 — effect groups: nav1_7_vsd4

_Generated 2026-06-20. Cell = (verified pocket) × (efficacy sign)._

- Poses carried from Stage 2: **5**
- In partition cells: **3** across **1** cells
- Routed to separate-state track: **0**
- Efficacy unknown (review): **0**
- Quarantined (not in pocket of interest): **2**

## Pocket verification

**Pockets found:** vsd4_site (expected: vsd4_site) — as expected

| Cluster | Label | Poses | Status | Consensus residues (sample) |
|--:|---|--:|---|---|
| 0 | vsd4_site | 3 | assigned | ALA1251, ALA1270, ARG1268, ARG1271, ARG1274, ASN1206, ASP1252, GLU1200 |
| 1 | _quarantined_ | 1 | quarantined | ALA1585, ALA1604, ARG1602, ARG1605, ARG1608, ASN1540, ASP1586, GLU1534 |
| 2 | _quarantined_ | 1 | quarantined | ALA1596, ALA1615, ARG1613, ARG1616, ARG1619, ASN1551, ASP1597, GLU1545 |

_Notes: Single VSD4 aryl-sulfonamide site (the Stage-2 anchor already isolates it). Cryo-EM constructs differ in beta-subunit content and numbering, so geometric clusters are merged to one label._

## Partition cells

| Cell (pocket × efficacy) | Poses | Distinct ligands | Example HETs |
|---|--:|--:|---|
| `vsd4_site__negative` | 3 | 3 | X7L, X7W, X80 |

## Separate-state ligands (routed out of cells)

**Separate-state:** none.

## Efficacy review list

**Unknown efficacy:** none.

## Quarantined poses

**Quarantined** (2):

- `5P2` (5EK0_5P2_C1805, primary) — candidate pocket: vsd4_site
- `T70` (8I5G_T70_A2005, primary) — candidate pocket: vsd4_site

---

Cell mol2 sets: `groups/<pocket>__<efficacy>/` (one representative pose per ligand). Review sets: `review/{separate_state,unknown,quarantine}/`. Sessions: `nav1_7_vsd4_grouped.pse` (all cells) and per-cell `.pse`. Pose pools: `datasets/all_poses/` (every kept pose) and `datasets/representative/` (one per ligand), each with a `.pml` + `.pse`.
