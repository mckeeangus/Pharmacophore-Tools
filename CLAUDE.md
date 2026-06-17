# CLAUDE.md — Pharmacophore Construction Pipeline

Persistent project context and instructions for Claude Code. Read this fully at the start of every session before acting.

## Project overview

This project builds an **automated pharmacophore-model construction pipeline**, generalised across diverse protein classes (work targeting a JCIM publication).

The intended downstream data-generation flow is: **DrugCLIP** virtual screening → ligand prep → **GNINA** docking → distance/score filtering → RDKit feature extraction → clustering → pharmacophore model. **That downstream pipeline is NOT in scope yet** — do not build or invoke DrugCLIP or GNINA now. The immediate work is project setup and assembling a curated set of experimentally-bound ligands from the PDB to feed pharmacophore construction.

Compute is intended to run downstream on **Gadi (NCI supercomputer)**, so all setup must stay HPC-portable and reproducible (see operating rules).

## Code quality

Hold all pipeline code to these standards. They override convenience; a reviewer
should be able to read a module top-to-bottom and understand its contract.

**Prefer:**

- **Low cyclomatic complexity** — small functions, early returns, flat control flow.
- **Low duplication / high reusability** — factor shared logic into one place; reuse
  the existing IO/parse/path helpers rather than re-implementing them.
- **Explicit contracts** — typed dataclasses and signatures; say what goes in and
  what comes out. No surprising side effects.
- **Testability** — pure functions where possible; keep IO/network at the edges so
  the core logic can be unit-tested offline.
- **Modularity** — one module = one responsibility; geometry, scientific annotation,
  orchestration, and visualisation stay separable.
- **Pythonic structures** — dataclasses, comprehensions, `pathlib`, context managers,
  standard library idioms.

**Avoid:**

- **Hidden assumptions** — no silent defaults that encode a scientific decision; no
  inferring meaning from incidental cues (e.g. guessing efficacy from a name substring).
- **Hardcoded scientific knowledge** — domain facts (efficacy signs, pocket/site
  identities, exclusion lists, anchors) live in versioned **config data files**, not
  in code logic, so they can be reviewed and corrected without touching the pipeline.
- **Unnecessary coupling** — modules depend on narrow interfaces, not on each other's
  internals; a heavy/brittle dependency must not block unrelated code.

## Environment & operating rules

This project uses **pixi** for dependency management. These rules apply in every session:

- Run Python and all tooling through pixi, e.g. `pixi run python script.py` or a defined `pixi run <task>`. Never invoke a bare `python` from an ambient environment.
- Add dependencies with `pixi add <package>` into the appropriate feature. Never `pip install` globally; for pip-only packages use pixi's `pypi-dependencies` for the relevant feature.
- Do **not** use the conda `base` environment for anything.
- Keep dependencies compartmentalised into pixi **features** composed into named **environments**, sharing a common `core`, so a heavy/brittle dep never blocks the rest.

### HPC / Gadi portability (keep these true even though we run locally for now)

- **Compute nodes on Gadi have no internet.** All network work (PDB/UniProt downloads, `git`, `pixi install`) must run on a login node, data-mover node, or copyq/analysis job — never inside a standard compute job. The PDB scraping task below is network-heavy and must run where there is internet.
- **`/home` is capped at 10 GiB.** The pixi environment (`.pixi/`) and the pixi cache must not live there. On Gadi, keep the repo + env on `/scratch/<project>/<user>` and set `PIXI_CACHE_DIR` off `/home`. Large persistent reference data belongs on `/g/data`.
- Be polite to external APIs: cap parallel downloads, add retries/backoff, and cache everything so re-runs are offline-friendly.

## Repository layout

```
.
├── CLAUDE.md
├── pixi.toml / pixi.lock
├── pyproject.toml
├── README.md
├── .gitignore                 # data/ is ignored (large); catalogue/ is tracked
├── config/
│   └── targets.yaml           # target list + resolved UniProt accessions + per-target options
├── src/pharmpipe/
│   ├── io/                    # structure & ligand parsing/writing (mmCIF, mol2)
│   ├── pdb/                   # RCSB/UniProt querying, ligand extraction  ← implement now
│   ├── catalogue/             # ligand cataloguing/reporting              ← implement now
│   ├── features/ clustering/ pharmacophore/   # downstream — scaffold only
│   └── ...                    # docking/, screening/ etc. — scaffold only
├── scripts/
│   └── scrape_pdb_ligands.py  # thin CLI wrapper over src/pharmpipe/pdb + catalogue
├── catalogue/                 # TRACKED human-readable + CSV outputs (the deliverable)
├── data/                      # GITIGNORED, large
│   └── targets/<target_slug>/
│       ├── structures/        # downloaded mmCIF (cache)
│       └── ligands/mol2/      # extracted bound-pose ligands for PyMOL
└── tests/
```

---

## Pipeline stages (status)

The "known actives" work is built in stages; each writes tracked deliverables under `catalogue/<slug>/`. The downstream DrugCLIP→GNINA→features→model pipeline remains **out of scope**.

1. **Scrape & catalogue** (`scripts/scrape_pdb_ligands.py`, `src/pharmpipe/{pdb,catalogue}/`) — verified UniProt accessions, dated RCSB search, curated ligands, bound-pose mol2. Outputs: `unique_ligands.csv`, `per_structure.csv`, `resolved.json`, `ligand_catalogue.md`. **Done.**
2. **Site filtering & alignment** (`scripts/align_sites.py`, `src/pharmpipe/sites/`, `config/sites.yaml`) — keep only poses at each system's relevant site, superpose into one reference frame, per-target `.pse`. Output: `site_filter.csv`. **Done.**
3. **Effect-based grouping with pocket verification** (`scripts/group_effects.py`, `src/pharmpipe/groups/`, `config/pockets.yaml` + `config/efficacy.yaml`) — geometry-verified pockets (native contact fingerprints), efficacy signs from curated external pharmacology, partitioned into **cells = (pocket × efficacy)**. Outputs: `effect_groups.json`, `<slug>_stage3_report.md`, `groups/<pocket>__<efficacy>/` mol2 sets + per-cell sessions, `<slug>_grouped.pse`, `review/{separate_state,unknown,quarantine}/`. Three-stage report in `catalogue/run_summary.md`. **Done.** Stage 3 is offline (cached structures + catalogue); efficacy/pocket-naming knowledge lives in config, never in code. Quarantined poses, separate-state ligands, and `unknown` efficacy are first-class review outputs — not force-bucketed.
   - **3.3 — efficacy resolution + datasets** (`scripts/resolve_efficacy.py`, `src/pharmpipe/groups/{resolve,realign}.py`). `resolve-efficacy` (network → login node; caches `data/_cache/chembl/`) resolves previously-`unknown` ligands via HET→InChIKey (offline, from cached RCSB chem-comp) → ChEMBL parent → subtype-specific mechanism → action_type → sign, writing `catalogue/stage3_efficacy_resolved.csv` (consumed by the loader **below** curated config; SERDs/degraders auto-route to separate-state; conflicting subtypes stay `unknown`). adrb2 is collapsed to one orthosteric pocket; GABA-A uses `realign_global` to place the benzodiazepine vs orthosteric sites at their true subunit interfaces on the pentamer reference. Cell/grouped sessions show one representative pose per ligand; pose pools live under `catalogue/<slug>/datasets/{all_poses,representative}/` and the cross-target master `catalogue/datasets/`. **Done.**
   - **3.4 — literature efficacy curation** (manual, in a separate Claude session; offline merge back into config). The ChEMBL pass left most structural-biology ligands `unknown` (novel chemotypes with no curated MoA), so their efficacy *direction* was read from each structure's **primary publication** (worklist built by `scripts/make_literature_worklist.py`). 98/158 worklist ligands were resolved and merged into `config/efficacy.yaml` as `source: literature` — the **top** provenance tier (above `prelabelled`/`curated`, then the ChEMBL CSV fallback); PMID + confidence are recorded in each note, and full per-ligand `site`/`pose_source`/PMID provenance lives in `catalogue/{efficacy_curation_README.md,literature_curation_traceability.csv}`. The subtype rule is enforced: ligands characterised only at a different subtype (e.g. α7 not α4β2) stay `unknown`; wrong-target "mismatch" structures (C3aR/TAAR1/D1-D5/DAT pulled into adrb2/net) and additives stay `unknown` and so never enter cells. **Allosteric vs orthosteric is separated geometrically**, not from the `site` field: NS9283 (NSE) is an α4(+)/α4(−) PAM whose contacts merge with the orthosteric aromatic box, so a per-pose **marker override** (`config/pockets.yaml` `accessory.marker_hets: [NSE]`; `group._apply_marker_overrides`) places it in its own `accessory__positive` cell instead of pooling it with orthosteric agonists. Re-run `group-effects` (offline) to propagate; no new pipeline code beyond the marker override + worklist generator. **Done.**

---

## Known-actives reference (Stages 1–3.4 complete)

The known-actives assembly (scrape → site-filter/align → effect grouping → efficacy
resolution + datasets) is **done** for all targets below; see the stages list above.
The downstream DrugCLIP→GNINA→features→model pipeline remains **out of scope** — do
not build it. The target table is retained as durable reference (organism scope,
surrogate caveats); UniProt hints were verified at scrape time and recorded in each
`catalogue/<slug>/resolved.json`.

### Targets

UniProt hints below are **starting points to VERIFY**, not authoritative. Resolve and record the real accessions at runtime.

| Target | UniProt hint (VERIFY) | Notes / flags |
|---|---|---|
| Nicotinic acetylcholine receptor (α4β2) | CHRNA4 P43681, CHRNB2 P17787 | "Acetylcholine receptor" is ambiguous — assuming **neuronal nicotinic α4β2** per project history. Pharmacophore ground truth often derives from **AChBP surrogate** co-crystals (e.g. *Lymnaea*/*Aplysia* AChBP), not native receptor holo structures — include AChBP-mapped structures and label them as surrogates. |
| Estrogen receptor α | ESR1 P03372 | Mostly ligand-binding-domain structures; large set. |
| HIV-1 protease | (from Gag-Pol, e.g. P04585) — verify | Very large set. **Bridging/structural waters** are functionally important — note in catalogue; downstream pipeline must consider them. |
| β2-adrenoceptor | ADRB2 P07550 | GPCR; many structures use **fusion partners** (T4 lysozyme, BRIL) and thermostabilising mutations — don't catalogue the fusion-partner ligand environment as target ligands. |
| CDK2 | P24941 | With and without cyclin A; **bridging water** in the hinge/ATP site is a known caveat. |
| Carbonic anhydrase | CA2 P00918 | Defaulting to **isoform II**; flag if other isoforms (CA I–XIV) should be included. Catalytic **Zn²⁺ is a cofactor — keep it.** |
| Acetylcholinesterase | human ACHE P22303 | **Species ambiguity** — *Torpedo* (P04058) and mouse (P21836) are heavily represented. Decide species scope before bulk download. |
| CavAb | NavAb (Arcobacter butzleri) ~A8EVM5 — verify | **Engineered surrogate** (Ca²⁺-selective mutant of bacterial Naᵥ channel). Small set; flag as surrogate in the catalogue. |
| Cyclooxygenase-2 (PTGS2) | human P35354 | **Species ambiguity** — murine (Q05769) and ovine COX are common. **Heme** is a cofactor — keep. Decide species scope. |
| HMG-CoA reductase | HMGCR P04035 | Statin/inhibitor complexes. |
| GABA-A receptor | GABRA1 P14867, GABRG2 P18507, + β subunits | Pentameric, **many subunit compositions**, mostly cryo-EM; lots of lipids/detergents to filter. Decide subunit scope (e.g. all human GABA-A-subunit-mapped structures, or a specific αβγ composition). |
| Norepinephrine transporter (NET) | SLC6A2 P23975 | Confirmed target: the **norepinephrine/noradrenaline transporter (NET, gene SLC6A2)** — the SLC6 transporter, *not* an adrenergic receptor. Human NET structures are recent cryo-EM (often inhibitor-bound). Note the **surrogate caveat**: *Drosophila* dopamine transporter (dDAT) has historically been used as a structural surrogate for SLC6 transporters including NET — include dDAT-/surrogate-mapped structures only if explicitly wanted, and label them as surrogates (cf. AChBP for nAChR). |

### Resolved scope decisions (durable)

- **Organism scope:** human where possible; surrogates included only as labelled
  gap-fillers (AChBP for nAChR, dDAT for NET) — see config + `resolved.json`.
- Species/isoform/subunit ambiguities (AChE, COX-2, carbonic anhydrase isoform,
  GABA-A composition) were resolved at scrape time and are recorded per target.
- `pixi install` succeeds (core/dev/viz); the stages run via
  `pixi run scrape-pdb-ligands` → `align-sites` → `resolve-efficacy` (network) →
  `group-effects` (offline; `-e viz` to bake `.pse`). Efficacy knowledge in
  `config/efficacy.yaml` is layered `literature` > `prelabelled` > `curated` >
  ChEMBL-CSV fallback (Stage 3.4). `data/` is gitignored, `catalogue/` is the
  tracked deliverable.
