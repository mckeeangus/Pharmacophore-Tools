# Stage 3 — effect groups: net_slc6a2

_Generated 2026-06-15. Cell = (verified pocket) × (efficacy sign)._

- Poses carried from Stage 2: **50**
- In partition cells: **25** across **2** cells
- Routed to separate-state track: **0**
- Efficacy unknown (review): **25**
- Quarantined (not in pocket of interest): **0**

## Pocket verification

**Pockets found:** central_s1 (expected: central_s1) — as expected

| Cluster | Label | Poses | Status | Consensus residues (sample) |
|--:|---|--:|---|---|
| 0 | central_s1 | 28 | assigned | ALA145, ASP75, GLY149, GLY320, GLY423, LEU319, PHE317, PHE323 |
| 1 | central_s1 | 22 | assigned | ALA117, ALA44, ASP46, GLY322, GLY425, PHE319, PHE325, PHE43 |

_Notes: Central S1 substrate/inhibitor site. Human NET and the dDAT surrogate use different numbering, so geometric clusters are merged to one S1 label; species/subtype is recorded per pose._

## Partition cells

| Cell (pocket × efficacy) | Poses | Distinct ligands | Example HETs |
|---|--:|--:|---|
| `central_s1__negative` | 12 | 7 | 1XR, 21B, 41U, A1LX4, COC, DSM … |
| `central_s1__positive` | 13 | 6 | 1WE, B40, E5E, LDP, LNR, YMN |

## Separate-state ligands (routed out of cells)

**Separate-state:** none.

## Efficacy review list

**Unknown efficacy** (25):

- `1WR` (7WLW_1WR_A704, surrogate)
- `29E` (6M38_29E_A601, surrogate)
- `41X` (4XNX_41X_A707, surrogate)
- `42F` (4XP5_42F_A602, surrogate)
- `42F` (4XPF_42F_A703, surrogate)
- `42J` (4XPA_42J_A703, surrogate)
- `42J` (4XPH_42J_A602, surrogate)
- `42J` (4XPT_42J_A602, surrogate)
- `42L` (4XPG_42L_A701, surrogate)
- `68P` (8I3V_68P_A701, primary)
- `9BC` (7WGT_9BC_A701, surrogate)
- `A1D5S` (9KDH_A1D5S_B709, primary)
- `A1D9Y` (8ZP1_A1D9Y_A702, primary)
- `A1EBN` (9JEL_A1EBN_A701, primary)
- `A1EBO` (9JF3_A1EBO_A701, primary)
- `A1EFR` (9KE3_A1EFR_B707, primary)
- `A1H8F` (9EUO_A1H8F_A701, surrogate)
- `A1LX3` (8Y8Z_A1LX3_E701, primary)
- `A1LX5` (8Y91_A1LX5_A701, primary)
- `A1LX6` (8Y90_A1LX6_A701, primary)
- `F0F` (6M3Z_F0F_A701, surrogate)
- `F1U` (6M47_F1U_A608, surrogate)
- `XEF` (8WTY_XEF_A701, primary)
- `Y60` (8WTX_Y60_A701, primary)
- `YNT` (8XB2_YNT_A702, primary)

## Quarantined poses

**Quarantined:** none.

---

Cell mol2 sets: `groups/<pocket>__<efficacy>/`. Review sets: `review/{separate_state,unknown,quarantine}/`. Sessions: `net_slc6a2_grouped.pse` (all cells) and per-cell `.pse` in each folder.
