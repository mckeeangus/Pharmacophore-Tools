# Stage 3 — effect groups: chrm2

_Generated 2026-06-20. Cell = (verified pocket) × (efficacy sign)._

- Poses carried from Stage 2: **13**
- In partition cells: **13** across **2** cells
- Routed to separate-state track: **0**
- Efficacy unknown (review): **0**
- Quarantined (not in pocket of interest): **0**

## Pocket verification

**Pockets found:** orthosteric (expected: orthosteric, allosteric) — **DEPARTS from expectation**

| Cluster | Label | Poses | Status | Consensus residues (sample) |
|--:|---|--:|---|---|
| 0 | orthosteric | 13 | assigned | ALA191, ALA194, ASN108, ASN404, ASP103, CYS429, PHE195, SER107 |

_Notes: Orthosteric ACh pocket vs the extracellular-vestibule allosteric site. The allosteric modulator (2CU) is co-crystallised with orthosteric ACh in the same structure, so its HET marker overrides the label per pose (like the nAChR NSE accessory marker); GPCR renumbering otherwise collapses to the orthosteric label. If the allosteric poses fall outside the Stage-2 cutoff they simply do not appear — the marker only acts on poses that survive the filter._

## Partition cells

| Cell (pocket × efficacy) | Poses | Distinct ligands | Example HETs |
|---|--:|--:|---|
| `orthosteric__negative` | 6 | 3 | 3C0, 82F, QNB |
| `orthosteric__positive` | 7 | 2 | ACH, IXO |

## Separate-state ligands (routed out of cells)

**Separate-state:** none.

## Efficacy review list

**Unknown efficacy:** none.

## Quarantined poses

**Quarantined:** none.

---

Cell mol2 sets: `groups/<pocket>__<efficacy>/` (one representative pose per ligand). Review sets: `review/{separate_state,unknown,quarantine}/`. Sessions: `chrm2_grouped.pse` (all cells) and per-cell `.pse`. Pose pools: `datasets/all_poses/` (every kept pose) and `datasets/representative/` (one per ligand), each with a `.pml` + `.pse`.
