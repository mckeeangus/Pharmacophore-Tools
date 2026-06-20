# Prompt — literature efficacy curation, batch 2 (for a normal Claude session)

Copy everything below the line into a fresh Claude chat (one with PubMed / web
access), and attach `catalogue/literature_worklist_batch2.csv`. The output is
designed to paste straight back into this project's `config/efficacy.yaml`.

This is the **second target batch** (Nav1.7, glucocorticoid receptor, adenosine
A2A, muscarinic M2). It uses the same rules as the first batch; only the target
glossary and the ion-channel efficacy vocabulary are new.

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

The attached `literature_worklist_batch2.csv` has one row per unresolved ligand:

| column | meaning |
|---|---|
| `target` | model-system slug (the subtype / site that was crystallised) |
| `het` | 3–5 char PDB ligand code (the identifier I need keyed back) |
| `ligand_name` | IUPAC/chemical name from the PDB chemical component |
| `in_chembl` | `yes` = ChEMBL has binding data (it is a real ligand of the target) |
| `representative_pdb` | a PDB structure containing this ligand |
| `pubmed_id` | **primary citation of that structure — start here** |
| `doi`, `citation_title` | for locating / sanity-checking the paper |

`target` slugs in this batch:
- `nav1_7_vsd4` = **Nav1.7** voltage-gated sodium channel, **VSD4 aryl-sulfonamide**
  drug site (the voltage-sensor pocket of domain IV).
- `nav1_7_pore` = **Nav1.7**, **central-cavity / local-anaesthetic pore** site (the
  classical use-dependent channel-block site on the pore axis).
- `gr_nr3c1` = **glucocorticoid receptor** (NR3C1), steroid LBD pocket.
- `adora2a` = **adenosine A2A receptor** (GPCR), orthosteric pocket.
- `chrm2` = **muscarinic acetylcholine receptor M2** (GPCR); note the separate
  **extracellular allosteric vestibule** above the orthosteric ACh site.

## Task

For each row, read the primary citation (use the `pubmed_id`; fall back to
`doi`/title or a web search) and decide the ligand's efficacy **at the
crystallised target/subtype**, then assign:

**`efficacy`** (for reversible binders):
- `positive` — agonist, partial agonist, positive allosteric modulator (PAM),
  activator, **or — for the ion channels — a channel opener / activator** (e.g. a
  toxin or chemical that holds Nav1.7 open / blocks inactivation, like veratridine)
- `neutral` — neutral (silent) antagonist / pure competitive blocker with no
  reported intrinsic direction
- `negative` — inverse agonist, negative allosteric modulator (NAM), antagonist,
  enzyme inhibitor, **or — for the ion channels — a channel blocker / inhibitor**
  (local anaesthetics, aryl-sulfonamide VSD4 inhibitors, use-dependent blockers)

> **Ion-channel vocabulary.** Nav1.7 drugs are described as *blockers* vs
> *activators*, NOT agonist/antagonist. A pore or VSD4 **blocker/inhibitor →
> `negative`**; a channel **opener/activator → `positive`**. (This mirrors the
> transporter convention used for NET in batch 1.)

**`track: separate_state`** instead of an efficacy, when the ligand changes the
protein's *state* rather than reversibly occupying a resting pocket:
- covalent / irreversible warhead (tethered or bond-forming)
- degrader — SERD, PROTAC, molecular glue
- catalytic substrate / product / cofactor (e.g. an Hsp90-bound ATP/ADP in a GR
  chaperone complex is **not** a GR ligand — route it out or mark unknown)

**Leave it OUT (still unknown)** if the paper does not establish a direction for
*this* subtype/site.

## Rules (important — these protect the dataset's integrity)

1. **Subtype- and site-specific. Never cross boundaries.** Efficacy can flip
   between subtypes or sites. For `chrm2`, a compound characterised only at M1/M3/M4
   /M5 stays unknown. For Nav1.7, keep the VSD4 vs pore rows distinct — do not carry
   a sign from one site to the other. If the paper only characterises a *different*
   subtype/site than the `target` column, mark it unknown.
2. **No guessing.** If you cannot find a stated or strongly-implied direction,
   return `unknown`. A wrong sign is worse than a missing one.
3. **Cite your evidence.** Every call must reference the PMID (or DOI/URL) it came
   from, plus a 3–8 word rationale.
4. **Confidence flag** on every call:
   - `high` — the paper explicitly states the action for this subtype/site
   - `medium` — strong inference (named member of a well-established chemotype, or
     the title/abstract states the class)
   - `low` — indirect or partial evidence
5. **Watch for mismatches.** A few representative structures may be mis-paired
   (a row whose citation title is clearly about a *different* protein) — flag these
   as `unknown` with a note rather than forcing a call.

## Output

Group results **by target** as YAML ready to merge into `config/efficacy.yaml`
under each target's `ligands:` map. Quote any HET code that starts with a digit.

```yaml
# gr_nr3c1
"82H": {efficacy: positive, source: literature, note: "velsecorat selective GR agonist; PMID NNNNNN (conf: high)"}
HJ4:   {efficacy: negative, source: literature, note: "mifepristone-class GR antagonist; PMID NNNNNN (conf: medium)"}
# adora2a
JQ9:   {efficacy: negative, source: literature, note: "istradefylline-type A2A antagonist; PMID NNNNNN (conf: high)"}
# nav1_7_pore
A1E26: {efficacy: positive, source: literature, note: "veratridine, Nav channel activator; PMID NNNNNN (conf: high)"}
```

Then add:
- a **plain CSV block** `het,target,sign_or_track,confidence,pmid,evidence` for all
  rows you resolved (for traceability), and
- a short list of the HET codes you left `unknown`, with the reason (no PMID, only
  binding data, subtype/site mismatch, never functionally assayed, etc.).

Work through the list target by target. It's fine to do it in batches and ask me
to continue.
