# Stage 3 — effect groups: gaba_a

_Generated 2026-06-18. Cell = (verified pocket) × (efficacy sign)._

- Poses carried from Stage 2: **97**
- In partition cells: **93** across **4** cells
- Routed to separate-state track: **0**
- Efficacy unknown (review): **3**
- Quarantined (not in pocket of interest): **1**

## Pocket verification

**Pockets found:** bzd_site, orthosteric (expected: orthosteric, bzd_site) — as expected

| Cluster | Label | Poses | Status | Consensus residues (sample) |
|--:|---|--:|---|---|
| 0 | orthosteric | 89 | assigned | ARG67, GLU155, LEU118, PHE200, PHE65, SER156, THR130, THR202 |
| 1 | bzd_site | 7 | assigned | ASN60, GLN204, HIS102, PHE100, PHE77, SER159, SER205, SER206 |
| 2 | _quarantined_ | 1 | quarantined | ASP43, GLN64, GLU183, LYS229, PHE125, PHE234, SER184, SER230 |

_Notes: Orthosteric GABA site (beta(+)/alpha(-)) vs the benzodiazepine site (alpha(+)/gamma(-)). The BZ site is the stress-test split: PAM vs neutral antagonist vs inverse agonist. realign_global places each pose at its true subunit interface on the pentamer reference (the Stage-2 local fit stacks the BZ site onto the orthosteric one)._

## Partition cells

| Cell (pocket × efficacy) | Poses | Distinct ligands | Example HETs |
|---|--:|--:|---|
| `bzd_site__negative` | 1 | 1 | R63 |
| `bzd_site__neutral` | 1 | 1 | EIE |
| `bzd_site__positive` | 4 | 3 | 08H, A1ADG, DZP |
| `orthosteric__positive` | 87 | 3 | ABU, EI7, HSM |

## Separate-state ligands (routed out of cells)

**Separate-state:** none.

## Efficacy review list

**Unknown efficacy** (3):

- `BEN` (4COF_BEN_E500, primary)
- `BUA` (9HAA_BUA_B601, primary)
- `IYJ` (9DRX_IYJ_D402, primary)

## Quarantined poses

**Quarantined** (1):

- `EI7` (7QND_EI7_E501, primary) — candidate pocket: bzd_site

---

Cell mol2 sets: `groups/<pocket>__<efficacy>/` (one representative pose per ligand). Review sets: `review/{separate_state,unknown,quarantine}/`. Sessions: `gaba_a_grouped.pse` (all cells) and per-cell `.pse`. Pose pools: `datasets/all_poses/` (every kept pose) and `datasets/representative/` (one per ligand), each with a `.pml` + `.pse`.
