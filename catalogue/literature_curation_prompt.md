# Prompt — literature efficacy curation (for a normal Claude session)

Copy everything below the line into a fresh Claude chat (one with PubMed / web
access), and attach `catalogue/literature_worklist.csv`. The output is designed to
paste straight back into this project's `config/efficacy.yaml`.

---

You are helping curate a pharmacophore dataset. I have a set of ligands that were
**experimentally co-crystallised** with their protein targets (structures pulled
from the PDB). For each, I need the ligand's **functional effect on that target**
— its efficacy *direction* — which a prior automated pass against ChEMBL's
mechanism table could **not** find, because these are research-grade compounds
(fragments, med-chem series, tool compounds) rather than approved drugs. That
information almost always lives in the **primary publication of the structure**,
which I've provided as a PubMed ID.

## Input

The attached `literature_worklist.csv` has one row per unresolved ligand:

| column | meaning |
|---|---|
| `target` | model-system slug (the subtype that was crystallised) |
| `het` | 3–5 char PDB ligand code (the identifier I need keyed back) |
| `ligand_name` | IUPAC/chemical name from the PDB chemical component |
| `in_chembl` | `yes` = ChEMBL has binding data (it is a real ligand of the target) |
| `representative_pdb` | a PDB structure containing this ligand |
| `pubmed_id` | **primary citation of that structure — start here** |
| `doi`, `citation_title` | for locating / sanity-checking the paper |

`target` slugs: `nachr_a4b2` = neuronal nicotinic acetylcholine receptor α4β2;
`esr1` = estrogen receptor α; `adrb2` = β2-adrenoceptor; `net_slc6a2` =
norepinephrine transporter (SLC6A2); `gaba_a` = GABA-A receptor; `cdk2`, `cavab`
as named.

## Task

For each row, read the primary citation (use the `pubmed_id`; fall back to
`doi`/title or a web search) and decide the ligand's efficacy **at the
crystallised target/subtype**, then assign:

**`efficacy`** (for reversible binders):
- `positive` — agonist, partial agonist, positive allosteric modulator (PAM),
  activator, or transporter substrate / releasing agent
- `neutral` — neutral (silent) antagonist / pure competitive blocker with no
  reported intrinsic direction
- `negative` — inverse agonist, negative allosteric modulator (NAM), enzyme
  inhibitor, or reuptake inhibitor

**`track: separate_state`** instead of an efficacy, when the ligand changes the
protein's *state* rather than reversibly occupying a resting pocket:
- covalent / irreversible warhead (tethered or bond-forming)
- degrader — SERD, PROTAC, molecular glue
- catalytic substrate / product / cofactor

**Leave it OUT (still unknown)** if the paper does not establish a direction for
*this* subtype.

## Rules (important — these protect the dataset's integrity)

1. **Subtype-specific. Never cross subtypes.** Efficacy can flip between subtypes
   (e.g. 4BP-TQS is an α7 agonist but an α4β2 antagonist). If the paper only
   characterises a *different* subtype than the `target` column, mark it unknown —
   do not transfer the other subtype's sign.
2. **No guessing.** If you cannot find a stated or strongly-implied direction,
   return `unknown`. A wrong sign is worse than a missing one.
3. **Cite your evidence.** Every call must reference the PMID (or DOI/URL) it came
   from, plus a 3–8 word rationale.
4. **Confidence flag** on every call:
   - `high` — the paper explicitly states the action for this subtype
   - `medium` — strong inference (e.g. it's a named member of a well-established
     chemotype, or the title/abstract states the class)
   - `low` — indirect or partial evidence
5. **Watch for mismatches.** A few representative structures may be mis-paired
   (e.g. a row whose citation title is clearly about a *different* protein) — flag
   these as `unknown` with a note rather than forcing a call.

## Output

Group results **by target** as YAML ready to merge into `config/efficacy.yaml`
under each target's `ligands:` map. Quote any HET code that starts with a digit.

```yaml
# nachr_a4b2
"4P0": {efficacy: positive, source: literature, note: "X agonist; PMID 26959852 (conf: high)"}
TKT:   {efficacy: neutral,  source: literature, note: "competitive antagonist; PMID 20881060 (conf: high)"}
# esr1
L5B:   {track: separate_state, source: literature, reason: "SERD/degrader; PMID 31495970 (conf: high)"}
```

Then add:
- a **plain CSV block** `het,target,sign_or_track,confidence,pmid,evidence` for all
  rows you resolved (for traceability), and
- a short list of the HET codes you left `unknown`, with the reason (no PMID, only
  binding data, subtype mismatch, never functionally assayed, etc.).

Work through the list target by target. It's fine to do it in batches and ask me
to continue.
