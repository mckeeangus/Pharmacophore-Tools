# Stage 3 — effect groups: cdk2

_Generated 2026-06-15. Cell = (verified pocket) × (efficacy sign)._

- Poses carried from Stage 2: **100**
- In partition cells: **95** across **1** cells
- Routed to separate-state track: **3**
- Efficacy unknown (review): **0**
- Quarantined (not in pocket of interest): **2**

## Pocket verification

**Pockets found:** atp_site (expected: atp_site) — as expected

| Cluster | Label | Poses | Status | Consensus residues (sample) |
|--:|---|--:|---|---|
| 0 | atp_site | 98 | assigned | ALA144, ALA31, ASP145, ASP86, GLN131, GLN85, GLU81, HIS84 |
| 1 | _quarantined_ | 1 | quarantined | ALA137, ALA31, ASN125, ASP138, ASP79, GLN124, GLN78, GLU12 |
| 2 | _quarantined_ | 1 | quarantined | ALA308, ARG241, ASP305, CYS193, GLU57, LYS192, MET189 |

_Notes: ATP/hinge site. Allosteric binders were dropped by the Stage-2 filter._

## Partition cells

| Cell (pocket × efficacy) | Poses | Distinct ligands | Example HETs |
|---|--:|--:|---|
| `atp_site__negative` | 95 | 93 | 03K, 09K, 10K, 11K, 16K, 18K … |

## Separate-state ligands (routed out of cells)

**Separate-state** (3):

- `ATP` (2CCH_ATP_C1297, primary) — ATP cofactor/substrate, not an inhibitor
- `ATP` (4EOJ_ATP_A301, primary) — ATP cofactor/substrate, not an inhibitor
- `ATP` (8FP5_ATP_A302, primary) — ATP cofactor/substrate, not an inhibitor

## Efficacy review list

**Unknown efficacy:** none.

## Quarantined poses

**Quarantined** (2):

- `A1IE9` (9FR2_A1IE9_A301, primary) — candidate pocket: atp_site
- `SGM` (7QHL_SGM_B503, primary) — candidate pocket: atp_site

---

Cell mol2 sets: `groups/<pocket>__<efficacy>/`. Review sets: `review/{separate_state,unknown,quarantine}/`. Sessions: `cdk2_grouped.pse` (all cells) and per-cell `.pse` in each folder.
