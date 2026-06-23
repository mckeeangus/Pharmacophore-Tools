# Stage 3 — effect groups: drd1

_Generated 2026-06-23. Cell = (verified pocket) × (efficacy sign)._

- Poses carried from Stage 2: **35**
- In partition cells: **31** across **2** cells
- Routed to separate-state track: **4**
- Efficacy unknown (review): **0**
- Quarantined (not in pocket of interest): **0**

## Pocket verification

**Pockets found:** orthosteric (expected: orthosteric) — as expected

| Cluster | Label | Poses | Status | Consensus residues (sample) |
|--:|---|--:|---|---|
| 0 | orthosteric | 31 | assigned | ASN292, ASP103, ILE104, LEU190, PHE288, PHE289, SER107, SER198 |
| 1 | orthosteric | 4 | assigned | ALA366, ALA48, ASN292, ASN50, ASP295, ASP49, CYS365, GLY52 |

_Notes: Single orthosteric dopamine pocket. GPCR fusion-construct renumbering (BRIL/T4L) and active-state Gs-protein complexes fragment the geometric clusters across structures, so they are merged to one orthosteric label (as with adrb2/adora2a). G-protein nucleotides (GDP/GTP) and Mg are routed to separate_state in efficacy.yaml and in any case fall outside the Stage-2 orthosteric cutoff._

## Partition cells

| Cell (pocket × efficacy) | Poses | Distinct ligands | Example HETs |
|---|--:|--:|---|
| `orthosteric__negative` | 2 | 1 | A1EKL |
| `orthosteric__positive` | 29 | 16 | 7LD, 86W, A1IZU, A1IZV, ALE, G3C … |

## Separate-state ligands (routed out of cells)

**Separate-state** (4):

- `GDP` (7F1O_GDP_A402, primary) — Galpha-s cofactor in the active-state complex, not a D1 ligand
- `GDP` (7F1Z_GDP_A401, primary) — Galpha-s cofactor in the active-state complex, not a D1 ligand
- `GTP` (7F23_GTP_A401, primary) — Galpha-s cofactor in the active-state complex, not a D1 ligand
- `GTP` (7F24_GTP_A401, primary) — Galpha-s cofactor in the active-state complex, not a D1 ligand

## Efficacy review list

**Unknown efficacy:** none.

## Quarantined poses

**Quarantined:** none.

---

Cell mol2 sets: `groups/<pocket>__<efficacy>/` (one representative pose per ligand). Review sets: `review/{separate_state,unknown,quarantine}/`. Sessions: `drd1_grouped.pse` (all cells) and per-cell `.pse`. Pose pools: `datasets/all_poses/` (every kept pose) and `datasets/representative/` (one per ligand), each with a `.pml` + `.pse`.
