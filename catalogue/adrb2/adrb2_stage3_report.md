# Stage 3 — effect groups: adrb2

_Generated 2026-06-20. Cell = (verified pocket) × (efficacy sign)._

- Poses carried from Stage 2: **100**
- In partition cells: **92** across **3** cells
- Routed to separate-state track: **2**
- Efficacy unknown (review): **3**
- Quarantined (not in pocket of interest): **3**

## Pocket verification

**Pockets found:** orthosteric (expected: orthosteric) — as expected

| Cluster | Label | Poses | Status | Consensus residues (sample) |
|--:|---|--:|---|---|
| 0 | orthosteric | 86 | assigned | ASN293, ASN312, ASP113, PHE193, PHE289, PHE290, SER203, SER204 |
| 1 | orthosteric | 9 | assigned | ASN1293, ASN1312, ASP1113, ASP1192, CYS1191, ILE1309, PHE1193, PHE1289 |
| 2 | orthosteric | 2 | assigned | ASN292, ASP103, ASP187, ASP314, CYS186, CYS96, ILE104, LEU190 |
| 3 | _quarantined_ | 1 | quarantined | ALA422, ARG161, ARG340, ASP417, GLY397, HIS418, HIS81, ILE102 |
| 4 | _quarantined_ | 1 | quarantined | ASN435, ASP113, PHE412, PHE413, SER203, SER207, TRP409, TYR439 |
| 5 | _quarantined_ | 1 | quarantined | ASP103, GLY293, ILE104, ILE290, LEU72, PHE186, PHE267, PHE268 |

_Notes: All kept poses bind the single orthosteric catecholamine pocket; fusion- construct renumbering (T4L/BRIL) and long-acting-agonist exosite reach fragment the geometric clusters across structures, so they are merged to one orthosteric label. The Stage-2 distance filter already restricts kept poses to this site._

## Partition cells

| Cell (pocket × efficacy) | Poses | Distinct ligands | Example HETs |
|---|--:|--:|---|
| `orthosteric__negative` | 16 | 7 | A1JHU, CAU, CVD, JRZ, JSZ, SNP … |
| `orthosteric__neutral` | 7 | 3 | A1AE2, BER, JTZ |
| `orthosteric__positive` | 69 | 11 | 68H, A1ASM, ALE, DZQ, G1I, GJ6 … |

## Separate-state ligands (routed out of cells)

**Separate-state** (2):

- `35V` (4QKX_35V_A1403, primary) — covalent thiol-tethered catechol agonist; PMID 25006259 (conf: high)
- `ERC` (3PDS_ERC_A1201, primary) — covalent tethered agonist (covalent)

## Efficacy review list

**Unknown efficacy** (3):

- `A1IZU` (9I52_A1IZU_R501, primary)
- `A1IZV` (9I54_A1IZV_R501, primary)
- `B40` (9U9V_B40_R401, primary)

## Quarantined poses

**Quarantined** (3):

- `A1D9A` (8ZWG_A1D9A_A601, primary) — no pocket match
- `E5E` (9CHU_E5E_A501, primary) — candidate pocket: orthosteric
- `WV8` (8UHB_WV8_A401, primary) — candidate pocket: orthosteric

---

Cell mol2 sets: `groups/<pocket>__<efficacy>/` (one representative pose per ligand). Review sets: `review/{separate_state,unknown,quarantine}/`. Sessions: `adrb2_grouped.pse` (all cells) and per-cell `.pse`. Pose pools: `datasets/all_poses/` (every kept pose) and `datasets/representative/` (one per ligand), each with a `.pml` + `.pse`.
