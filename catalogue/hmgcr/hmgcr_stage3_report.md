# Stage 3 — effect groups: hmgcr

_Generated 2026-06-18. Cell = (verified pocket) × (efficacy sign)._

- Poses carried from Stage 2: **22**
- In partition cells: **19** across **1** cells
- Routed to separate-state track: **3**
- Efficacy unknown (review): **0**
- Quarantined (not in pocket of interest): **0**

## Pocket verification

**Pockets found:** hmg_site (expected: hmg_site) — as expected

| Cluster | Label | Poses | Status | Consensus residues (sample) |
|--:|---|--:|---|---|
| 0 | hmg_site | 22 | assigned | ALA564, ALA751, ALA856, ARG568, ARG590, ASN686, ASN755, ASP690 |

_Notes: Statin / HMG site (the NADPH cofactor site is separate)._

## Partition cells

| Cell (pocket × efficacy) | Poses | Distinct ligands | Example HETs |
|---|--:|--:|---|
| `hmg_site__negative` | 19 | 18 | 114, 115, 116, 117, 3HI, 4HI … |

## Separate-state ligands (routed out of cells)

**Separate-state** (3):

- `HMG` (1DQ9_HMG_D104, primary) — HMG-CoA substrate/cofactor, not an inhibitor
- `MAH` (1DQ8_MAH_A200, primary) — HMG substrate/product analogue
- `MAH` (1DQA_MAH_B202, primary) — HMG substrate/product analogue

## Efficacy review list

**Unknown efficacy:** none.

## Quarantined poses

**Quarantined:** none.

---

Cell mol2 sets: `groups/<pocket>__<efficacy>/` (one representative pose per ligand). Review sets: `review/{separate_state,unknown,quarantine}/`. Sessions: `hmgcr_grouped.pse` (all cells) and per-cell `.pse`. Pose pools: `datasets/all_poses/` (every kept pose) and `datasets/representative/` (one per ligand), each with a `.pml` + `.pse`.
