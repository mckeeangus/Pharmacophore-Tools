# Stage 3 — effect groups: esr1

_Generated 2026-06-18. Cell = (verified pocket) × (efficacy sign)._

- Poses carried from Stage 2: **100**
- In partition cells: **70** across **2** cells
- Routed to separate-state track: **17**
- Efficacy unknown (review): **13**
- Quarantined (not in pocket of interest): **0**

## Pocket verification

**Pockets found:** lbp (expected: lbp) — as expected

| Cluster | Label | Poses | Status | Consensus residues (sample) |
|--:|---|--:|---|---|
| 0 | lbp | 100 | assigned | ALA350, ARG394, ASP351, GLU353, GLY521, HIS524, ILE424, LEU346 |

_Notes: Ligand-binding-domain hormone pocket._

## Partition cells

| Cell (pocket × efficacy) | Poses | Distinct ligands | Example HETs |
|---|--:|--:|---|
| `lbp__negative` | 47 | 42 | 29S, 4Q7, 53Q, 73I, 77I, 7AI … |
| `lbp__positive` | 23 | 16 | 17M, 1HP, 27J, 27L, 36M, 458 … |

## Separate-state ligands (routed out of cells)

**Separate-state** (17):

- `3YJ` (7R62_3YJ_A601, primary) — ICI164384/fulvestrant-class SERD; deposit title (conf: medium)
- `7I0` (7RS4_7I0_C601, primary) — degrader/SERD — separate state
- `86V` (5UFW_86V_B601, primary) — OP-1074 pure antiestrogen / SERD; PMID 29915250 (conf: medium)
- `F3D` (6CHW_F3D_A601, primary) — selective ER covalent antagonist; PMID 29991605 (conf: high)
- `F3D` (6CHZ_F3D_A601, primary) — selective ER covalent antagonist; PMID 29991605 (conf: high)
- `GQD` (5FQP_GQD_A1549, primary) — SERD (selective ER downregulator); PMID 26819673 (conf: high)
- `H09` (7QVJ_H09_B601, primary) — zwitterionic SERD-antagonist (degrader); PMID 36727211 (conf: high)
- `H8W` (6IAR_H8W_A601, primary) — tricyclic-indazole SERD-antagonist (degrader); PMID 30640465 (conf: high)
- `I0V` (7TE7_I0V_A601, primary) — degrader/SERD — separate state
- `KE9` (5ACC_KE9_A1546, primary) — AZD9496 SERD (degrader); PMID 26407012 (conf: high)
- `L5B` (6SBO_L5B_A4000, primary) — degrader/SERD — separate state
- `LRQ` (6SQ0_LRQ_A601, primary) — ER degrader (SERD); PMID 31620239 (conf: high)
- `LVH` (6SUO_LVH_B601, primary) — ER degrader (SERD); PMID 31620239 (conf: high)
- `ND1` (6OWC_ND1_B601, primary) — H3B-6545 covalent antagonist (Y537S); deposit title (conf: high)
- `QHG` (5FQR_QHG_A1546, primary) — SERD (selective ER downregulator); PMID 26819673 (conf: high)
- `QNE` (6ZOQ_QNE_B601, primary) — AZD9833/camizestrant SERD (degrader); PMID 32910656 (conf: high)
- `VQI` (5FQV_VQI_A1546, primary) — SERD (selective ER downregulator); PMID 26819673 (conf: high)

## Efficacy review list

**Unknown efficacy** (13):

- `86Y` (5UFX_86Y_B601, primary)
- `A1AHO` (8VZ0_A1AHO_D600, primary)
- `A1AHS` (8VZ1_A1AHS_C600, primary)
- `A1AHU` (8VYX_A1AHU_C600, primary)
- `A1AHV` (8VYT_A1AHV_A600, primary)
- `A1AHW` (8VZP_A1AHW_B601, primary)
- `A1AHX` (8VZQ_A1AHX_B600, primary)
- `A1AHY` (8W07_A1AHY_A601, primary)
- `A1AHZ` (8W07_A1AHZ_B601, primary)
- `A1AIZ` (9B25_A1AIZ_A600, primary)
- `WST` (2POG_WST_B301, primary)
- `WVR` (8EV1_WVR_A602, primary)
- `WVW` (8EV1_WVW_B601, primary)

## Quarantined poses

**Quarantined:** none.

---

Cell mol2 sets: `groups/<pocket>__<efficacy>/` (one representative pose per ligand). Review sets: `review/{separate_state,unknown,quarantine}/`. Sessions: `esr1_grouped.pse` (all cells) and per-cell `.pse`. Pose pools: `datasets/all_poses/` (every kept pose) and `datasets/representative/` (one per ligand), each with a `.pml` + `.pse`.
