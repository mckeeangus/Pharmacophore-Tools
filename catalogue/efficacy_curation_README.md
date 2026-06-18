# Literature efficacy curation — dataset documentation

## What this is

Per-ligand **efficacy direction** for 158 co-crystallised ligands (the Stage 3.3
worklist of still-`unknown` actives, regenerable with
`scripts/make_literature_worklist.py`), assigned by reading each structure's primary
citation. This is the manual `efficacy-sign` curation step that feeds the Stage 3
`(subtype × site/mode × efficacy-sign)` partition key. It answers one question per
ligand — *which way does this molecule push the target?* — and records two
structural qualifiers (`site`, `pose_source`) needed before any pose is pooled into
a pharmacophore hypothesis.

Coverage: 7 of the 12 benchmark targets (the ones with unresolved actives in this
worklist) — `nachr_a4b2`, `esr1`, `adrb2`, `net_slc6a2`, `gaba_a`, `cdk2`, `cavab`.

## Status — integrated

These calls have been **merged into `config/efficacy.yaml`** (Stage 3.4) as
`source: literature` entries, the top provenance tier; the original merge-ready
`efficacy.yaml` staging file has been removed. The `site` / `pose_source` / `pdb` /
PMID / confidence qualifiers for every curated ligand are preserved here and in the
traceability CSV. Allosteric-vs-orthosteric separation is enforced **geometrically**
by Stage 3 pocket verification (NS9283/NSE carries an `accessory` pocket marker in
`config/pockets.yaml`), not by the `site` field.

## Files

| File | Contents |
|---|---|
| `literature_curation_traceability.csv` | Standalone table, **all 158 rows** (resolved + unknown), one row per ligand, with `site` / `pose_source` / `pmid` / `confidence`. |
| `efficacy_curation_README.md` | This file. |

## Per-ligand schema

YAML keys (and the matching CSV columns):

- **`efficacy`** — `positive` \| `neutral` \| `negative`, **or** **`track: separate_state`**.
- **`site`** — where the ligand binds (see vocabulary).
- **`pose_source`** — what the deposited structure actually is (see vocabulary).
- **`pdb`** / `representative_pdb` — the PDB the label attaches to (rejoin key).
- **`source`** — always `literature` here.
- **`note`** / **`reason`** — short rationale + `PMID NNNN (conf: high|medium|low)`.

`unknown` rows are deliberately **omitted** from the YAML mappings (a missing sign is
cheaper than a wrong one) and instead listed, with reasons, in the commented block at
the end of `efficacy.yaml`. They remain in the CSV for auditability.

## Efficacy rubric

| value | meaning |
|---|---|
| `positive` | agonist / partial agonist / PAM / activator / transporter substrate or releaser |
| `neutral` | silent or competitive antagonist with no intrinsic direction |
| `negative` | inverse agonist / NAM / enzyme inhibitor / reuptake inhibitor / full antagonist |
| `separate_state` (track) | covalent warhead, degrader (SERD/PROTAC/glue), or catalytic substrate/cofactor — a non-equilibrium or adduct geometry that must **not** enter an agonist or antagonist pharmacophore |
| `unknown` | direction not establishable for *this* target from this structure — excluded |

Subtype rule: a sign is never transferred across a subtype or system boundary
(e.g. α7 → α4β2, DAT → NET). Confidence reflects evidence strength, not the model's
certainty: `high` = explicit functional statement for this target; `medium` = strong
chemotype/named-drug inference; `low` = indirect or paper-context inference.

## `site` vocabulary  *(added this revision)*

Efficacy direction alone is not enough to pool poses — ligands acting at different
pockets produce geometrically incompatible feature maps.

| value | n | meaning / pharmacophore implication |
|---|---|---|
| `orthosteric` | 138 | canonical endogenous-ligand pocket (ACh interface, ER LBD, β2 catecholamine site, transporter S1). Poolable within a sign. |
| `allosteric` | 3 | distinct modulator pocket — **NS9283 (NSE)** at the α4(+)/α4(−) accessory interface, **galantamine (GNT)**, **lamotrigine (IYJ)**. Must form their own hypothesis; do **not** mix with orthosteric agonists. |
| `bitopic` | 1 | spans orthosteric + a secondary exosite (**A1AE2**). |
| `covalent` | 3 | covalent adduct (**35V, F3D, ND1**) — geometry is post-reaction. |
| `additive` | 4 | not a pharmacological ligand (**BEN, BUA, G3P, SGM**). |
| `na` | 9 | mismatched structures (see below) — site not applicable to the slug. |

## `pose_source` vocabulary  *(added this revision)*

Whether the deposited coordinates are the actual target. A label can be
target-valid while the *pose* comes from something else — that pose describes the
surrogate's pocket, not the target's.

| value | n | meaning |
|---|---|---|
| `native` | 94 | structure **is** the target (incl. point mutants, e.g. ERα Y537S). |
| `surrogate` | 50 | accepted stand-in per project convention — **AChBP** for nAChR, **dDAT** for NET, **CaVAb** for the Ca channel. Pose geometry is the surrogate's pocket; treat with care. |
| `chimera` | 4 | engineered hybrid — AChBP/α3-loopC chimeras (7LB, TII); engineered GABA transporter (1WR, 9BC). |
| `mismatch` | 10 | the `representative_pdb` is a **different protein** than the slug: C3aR / D1 / D5 / TAAR1 in `adrb2`; granisetron→5-HT3, glycine→GlyR, bicuculline→GABA-A, sulfoxaflor→insect nAChR, paraherquamide→*C. elegans* nAChR in `nachr_a4b2`; hDAT in `net_slc6a2`. |

## Summary counts

| target (n) | positive | negative | neutral | separate_state | unknown |
|---|---|---|---|---|---|
| nachr_a4b2 (52) | 14 | – | 5 | – | 33 |
| esr1 (71) | 12 | 33 | – | 13 | 13 |
| adrb2 (12) | 3 | 1 | 2 | 1 | 5 |
| net_slc6a2 (18) | – | 14 | – | – | 4 |
| gaba_a (3) | – | – | – | – | 3 |
| cdk2 (1) | – | – | – | – | 1 |
| cavab (1) | – | – | – | – | 1 |
| **total (158)** | **29** | **48** | **7** | **14** | **60** |

Resolved 98 / unknown 60 (38%). The large `nachr_a4b2` unknown count is honest
subtype/structure caution, not missing effort — mostly AChBP binding/biosensor/
fragment studies with no α4β2 functional readout, α7-only characterisation, or
mismatched structures.

## Caveats before building pharmacophores

1. **Filter on `site` first.** Pool only same-`site`, same-sign ligands. The three
   `allosteric` rows and the `bitopic` row will smear orthosteric feature positions
   if pooled — NS9283 in particular is `positive` but binds a different pocket than
   the orthosteric agonists.
2. **`separate_state` is not a pharmacophore class.** Covalent adducts and degraders
   carry non-equilibrium geometry; exclude from both agonist and antagonist maps.
3. **`pose_source` gates the geometry, not the label.** `surrogate`/`chimera` poses
   describe AChBP/dDAT/CaVAb pockets — any hypothesis built from them inherits the
   surrogate's pocket shape. `mismatch` rows mean wrong-target structures are present
   in the upstream pool; the labels exclude them, but a geometry pipeline that pulls
   poses independently should drop these PDBs explicitly.
4. **Threshold on confidence.** `low`/no-PMID positives (neonicotinoids at *vertebrate*
   α4β2, A1EFR, deposit-title-only calls) should be down-weighted or held out, not
   treated as ground truth.
5. **Receptor conformer is not encoded.** For ESR1 the same ligand can be crystallised
   in the agonist vs antagonist H12 conformer; pocket shape differs more than the
   efficacy label implies. Track conformer separately if pose geometry matters.
6. **Partial vs full agonism is collapsed** into `positive`; efficacy magnitude is lost.

## Upstream worklist hygiene (recommended)

Two systematic issues surfaced during curation, worth fixing before the next batch:

- **Mismatched representative PDBs** — `adrb2` pulled C3aR/D1/D5/TAAR1 structures;
  `net_slc6a2` pulled an hDAT structure. Check the rep-PDB protein matches the slug.
- **Additives as ligands** — G3P, monothioglycerol, benzamidine, butanoic acid entered
  as if they were target ligands. Filter HET codes against a common-additives list.

Together these account for ~13 of the 60 unknowns and would be removed pre-curation.
