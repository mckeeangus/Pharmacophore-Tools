# Stage 3 — effect groups: gr_nr3c1

_Generated 2026-06-20. Cell = (verified pocket) × (efficacy sign)._

- Poses carried from Stage 2: **33**
- In partition cells: **32** across **2** cells
- Routed to separate-state track: **0**
- Efficacy unknown (review): **0**
- Quarantined (not in pocket of interest): **1**

## Pocket verification

**Pockets found:** lbp (expected: lbp) — as expected

| Cluster | Label | Poses | Status | Consensus residues (sample) |
|--:|---|--:|---|---|
| 0 | lbp | 32 | assigned | ALA605, ARG611, ASN564, CYS643, CYS736, GLN570, GLN642, GLY567 |
| 1 | _quarantined_ | 1 | quarantined | ARG41, ASN38, ASN42, ASP213, GLU113, GLY169, HIS164, ILE166 |

_Notes: Ligand-binding-domain steroid pocket (the GR analogue of the ESR1 LBP). One soluble human NR3C1 numbering, so no collapse is needed._

## Partition cells

| Cell (pocket × efficacy) | Poses | Distinct ligands | Example HETs |
|---|--:|--:|---|
| `lbp__negative` | 5 | 3 | 29M, 486, HJ4 |
| `lbp__positive` | 27 | 20 | 82H, 866, 8W5, 8W8, A1ACE, B9Q … |

## Separate-state ligands (routed out of cells)

**Separate-state:** none.

## Efficacy review list

**Unknown efficacy:** none.

## Quarantined poses

**Quarantined** (1):

- `QJK` (8A9G_QJK_B303, primary) — no pocket match

---

Cell mol2 sets: `groups/<pocket>__<efficacy>/` (one representative pose per ligand). Review sets: `review/{separate_state,unknown,quarantine}/`. Sessions: `gr_nr3c1_grouped.pse` (all cells) and per-cell `.pse`. Pose pools: `datasets/all_poses/` (every kept pose) and `datasets/representative/` (one per ligand), each with a `.pml` + `.pse`.
