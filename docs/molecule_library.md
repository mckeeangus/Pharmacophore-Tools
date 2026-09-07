# Molecule library — the DrugCLIP screening source

The full vendor compound library that DrugCLIP screens against to produce the ranked hit lists
(`website_output/<slug>_output.csv`) that seed the Stage-4 docked/seed-alignment builds. It is the
*upstream* input to the whole DrugCLIP → GNINA → pharmacophore flow.

- **Location:** `molecule_library/` (repo root). **Gitignored** — ~48 GB of vendor SDFs, bulk input,
  never tracked. This file + `molecule_library_manifest.csv` are the tracked record of it.
- **Format:** one SDF per vendor chunk (`<mol_id>` records, `$$$$`-delimited). Files are 0.5–4.8 GB
  each; do **not** open them with an editor/Read — stream them (`grep`, RDKit `SDMolSupplier`,
  `split`) so memory stays bounded.
- **HPC note:** on Gadi this belongs on `/g/data` (not `/home`, not `/scratch` long-term); DrugCLIP
  embedding/screening runs against it there, not locally.

## Summary statistics

**31 files · 18,611,129 molecule records · 48.4 GB** (raw records — see the dedup caveat below).

| Vendor | Files | Molecules | Size |
|---|--:|--:|--:|
| mcule | 10 | 7,058,744 | 15.7 GB |
| Enamine | 10 | 4,736,323 | 11.9 GB |
| FCHGroup | 1 | 2,244,487 | 5.1 GB |
| ChemDiv | 4 | 1,649,761 | 6.3 GB |
| Princeton | 3 | 1,532,542 | 4.3 GB |
| STK / Vitas-M | 3 | 1,389,272 | 5.1 GB |
| **Total** | **31** | **18,611,129** | **48.4 GB** |

Per-file counts: `docs/molecule_library_manifest.csv`. (Counts are `$$$$` record counts, i.e. molecule
entries.)

## Link to the screening deposit

Every `library_name` in the DrugCLIP indexes maps to a vendor here, confirming this is the screening
source — a docked hit is traceable back to its library entry by `library_name` + `mol_id`:

| Index `library_name` | Library vendor |
|---|---|
| `ChemDiv` | ChemDiv |
| `Enamine_screening_collection_sdf_202504` | Enamine |
| `FCHGroup_SC_202007` | FCHGroup |
| `mcule_HTS_library_250308` | mcule |
| `Princeton_BioMolecular_Research` | Princeton |
| `Vitas-M` | STK / Vitas-M |

**Version caveat:** the deposited snapshots are close but not identical to the exact ones the current
indexes were screened from — Enamine is dated `202604` here vs `202504` in the index, and mcule
`260130` vs `250308`. FCHGroup, Princeton, ChemDiv, and Vitas-M match. Treat the library as the
screening source at the vendor level; for exact per-`mol_id` provenance, prefer the docked SDFs
(which already carry the screened structure) over re-looking-up in these newer snapshots.

## Caveats

- **Raw records, not unique molecules.** 18.6 M is the sum of SDF records; it is **not** deduplicated
  across vendors (the same purchasable compound is often sold by several) nor across salt/stereo/
  tautomer forms. A unique-molecule count would need an InChIKey pass over all 31 files (an offline
  batch job, not run here).
- **No property assumptions.** These stats are counts + sizes only; MW/logP/heavy-atom distributions
  would require a streaming RDKit pass (feasible but deferred — say the word).

## Reproducing these numbers

```
for f in molecule_library/*.sdf; do echo "$(basename "$f"),$(grep -c '^\$\$\$\$' "$f"),$(stat -c%s "$f")"; done
```
(streams each file; ~2 min for the full 48 GB). Aggregated by vendor into the table above.
