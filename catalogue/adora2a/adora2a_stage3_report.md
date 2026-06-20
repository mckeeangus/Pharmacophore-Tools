# Stage 3 — effect groups: adora2a

_Generated 2026-06-20. Cell = (verified pocket) × (efficacy sign)._

- Poses carried from Stage 2: **179**
- In partition cells: **172** across **3** cells
- Routed to separate-state track: **0**
- Efficacy unknown (review): **5**
- Quarantined (not in pocket of interest): **2**

## Pocket verification

**Pockets found:** orthosteric (expected: orthosteric) — as expected

| Cluster | Label | Poses | Status | Consensus residues (sample) |
|--:|---|--:|---|---|
| 0 | orthosteric | 172 | assigned | ASN253, GLU169, ILE274, LEU249, LEU85, MET177, MET270, PHE168 |
| 1 | orthosteric | 3 | assigned | ASN181, ASN349, GLU169, HIS346, HIS360, ILE370, LEU345, LEU363 |
| 2 | orthosteric | 2 | assigned | ASN358, GLU178, HIS355, HIS369, ILE379, LEU176, LEU354, LEU372 |
| 3 | _quarantined_ | 1 | quarantined | ASN374, GLU194, ILE395, LEU110, LEU370, MET202, MET391, PHE193 |
| 4 | _quarantined_ | 1 | quarantined | ASN505, GLU169, HIS502, LEU501, LEU519, LEU85, MET177, MET522 |

_Notes: Single orthosteric adenosine pocket. GPCR fusion-construct renumbering (BRIL/T4L) fragments the geometric clusters across structures, so they are merged to one orthosteric label (as with adrb2)._

## Partition cells

| Cell (pocket × efficacy) | Poses | Distinct ligands | Example HETs |
|---|--:|--:|---|
| `orthosteric__negative` | 146 | 28 | 6DV, 6DX, 6DY, 6DZ, 8D1, 8E2 … |
| `orthosteric__neutral` | 9 | 5 | 9XT, 9XW, F9Q, JQ9, U30 |
| `orthosteric__positive` | 17 | 7 | A1H1S, ADN, NEC, NGI, RVZ, UKA … |

## Separate-state ligands (routed out of cells)

**Separate-state:** none.

## Efficacy review list

**Unknown efficacy** (5):

- `9Y2` (5OLV_9Y2_A1201, primary)
- `9Y2` (8A2P_9Y2_A1201, primary)
- `A1COM` (7IN9_A1COM_A1234, primary)
- `A1COV` (7INI_A1COV_A1234, primary)
- `A1COY` (7INL_A1COY_A1234, primary)

## Quarantined poses

**Quarantined** (2):

- `TEP` (8PWN_TEP_A500, primary) — candidate pocket: orthosteric
- `ZMA` (9T9P_ZMA_B901, primary) — candidate pocket: orthosteric

---

Cell mol2 sets: `groups/<pocket>__<efficacy>/` (one representative pose per ligand). Review sets: `review/{separate_state,unknown,quarantine}/`. Sessions: `adora2a_grouped.pse` (all cells) and per-cell `.pse`. Pose pools: `datasets/all_poses/` (every kept pose) and `datasets/representative/` (one per ligand), each with a `.pml` + `.pse`.
