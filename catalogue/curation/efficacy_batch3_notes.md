# Batch 3 literature efficacy curation — dopamine receptor D1 (drd1)

Date: 2026-06-23. Curated by a delegated literature session (PubMed access), then
merged into `config/efficacy.yaml` as `source: literature`. Per-ligand provenance
is in `efficacy_batch3_traceability.csv`.

## Scope

The Stage-3.3 ChEMBL pass left 15 D1 ligands `unknown`; all 15 were resolved here
from each structure's primary publication. (The endogenous agonist dopamine, LDP,
was already seeded `curated`; the G-protein nucleotides GDP/GTP are `separate_state`.)

## Key finding — an agonist-dominated set

Nearly every deposited human D1 structure is an **active-state Gs (or Gs-mimetic
legobody) complex**, which structurally captures **agonists**. Accordingly 14 of
the 15 curated ligands are agonists (`positive`); **Flupentixol (A1EKL, 9LLG)** is
the sole antagonist (`negative`). This is a property of the available structural
data, not a curation gap: the `orthosteric__negative` cell is real but degenerate
(one ligand), and the `orthosteric__positive` cell is large and well defined — the
better-determined pharmacophore, consistent with why D1 was chosen (richest set).

Agonist chemotypes represented: catechols (dopamine, fenoldopam G3C, A77636 G3O,
epinephrine ALE), benzazepines (SKF-class SK0/SK9/GBU), aporphine (apomorphine OR9),
ergoline (LSD 7LD), and non-catechol/Gs-biased scaffolds (PW0464 G3U, PF-6142 V6X,
tavapadon-class compound 1 VFP, Roche compounds 19B/24 A1IZU/A1IZV, rotigotine R5F).

## Provenance caveats

- **A1EKL (flupentixol)** and **ALE (epinephrine)** have no primary PMID; their
  signs rest on the RCSB deposit title plus established pharmacology (flupentixol is
  a textbook D1/D2 antagonist; epinephrine is a known lower-potency D1 agonist and
  is captured in an active-state miniGs complex). Both are flagged here for that
  reason; ALE is `conf: medium`.
- The **subtype rule** was applied: every sign is supported at D1 specifically
  (pan-dopaminergic agonists with explicit D1 activity, or D1/D5-characterised
  biased agonists). No sign was transferred from a D2/D3-only characterisation.

## Key sources

Xiao et al. Cell 2021 (PMID 33571431, 33571432) and Zhuang et al. Cell 2021
(PMID 34083522) — the foundational D1-Gs agonist/structure papers (each deposits
several of the catechol/benzazepine/non-catechol agonists); Xu et al. Cell Res 2023
(rotigotine series, PMID 37221270); Fan et al. 2024 (LSD/PF-6142, PMID 39094559);
Rodríguez Sarmiento et al. J Med Chem 2025 (Roche biased agonists, PMID 40552668).
