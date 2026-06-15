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

---

## CURRENT OBJECTIVE — PDB ligand scrape & catalogue

(Trim this section once complete; everything above is durable.)

Scaffold the project directory per the layout above, then build and run a reproducible scraper that, for each target below:

1. **Resolve the target to verified UniProt accession(s).** Do not trust the hints in the table below — confirm each programmatically against UniProt/RCSB and record the accession(s) used. Record the **search date** alongside results (structure counts must be reproducible from dated, UniProt-keyed RCSB advanced searches).
2. **Query RCSB for all ligand-bound structures** mapped to those accession(s), using the RCSB Search API (consider the `rcsbsearchapi` package). Capture per structure: PDB ID, resolution, method (X-ray/cryo-EM/etc.), bound ligand HET codes, and the UniProt mapping.
3. **Curate ligands.** Filter out crystallographic additives, buffers, cryoprotectants, and waters using a maintained exclusion list (e.g. HOH, GOL, EDO, PEG/PG4, SO4, PO4, ACT, DMS, MES, TRS, FMT, CL, NA, K, etc.). **Keep genuine catalytic cofactors** (e.g. the Zn²⁺ in carbonic anhydrase, heme in COX-2) — do not blanket-drop all metals/ions; treat cofactors as ligands and flag borderline cases in a report rather than silently dropping.
4. **Build the catalogue document.** Per target, produce (a) a **unique-ligand** table — HET code, chemical name, SMILES, count of structures it appears in, a representative PDB ID — and (b) a **per-structure** table mapping PDB ID → ligand(s). Output machine-readable CSV (tracked, under `catalogue/`) **and** a neat combined human-readable summary (`catalogue/ligand_catalogue.md`, one section per target). An optional `.xlsx` workbook (one sheet per target) is welcome.
5. **Extract bound ligands as mol2** for PyMOL. Extract the **actual bound-pose instance coordinates** from each structure (these are what matter for pharmacophore work — NOT the idealised CCD coordinates). Assign correct bond orders using the RCSB Chemical Component Dictionary entry for each HET code as a template (RDKit `AssignBondOrdersFromTemplate`), falling back to OpenBabel perception only when no template applies; log fallbacks. Write one mol2 per bound instance, named `<PDBID>_<HET>_<chain><resseq>.mol2`, under `data/targets/<slug>/ligands/mol2/`. Make "all instances" vs "one representative per unique ligand" a config switch (default: all instances).
6. **Organise & report.** Per-target subdirectories as in the layout. Emit a run summary: structures found, ligands kept vs excluded, mol2 files written, and any failures.

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

### Definition of done

- `pixi install` succeeds (core/dev); scraper runs via `pixi run scrape-pdb-ligands --config config/targets.yaml`.
- For each confirmed target: verified UniProt accession(s) + dated search recorded; CSV + markdown catalogue produced under `catalogue/`; bound-pose mol2 files written under `data/targets/<slug>/ligands/mol2/` and openable in PyMOL.
- `data/` is gitignored; `catalogue/` is tracked. Run summary printed and logged.
- Before any bulk download, **confirm the remaining ambiguous targets** (AChE/COX-2 species, carbonic anhydrase isoform, GABA-A subunit scope) with the user. What needs to be achieved next: Do not move forward with implementing the pipeline, we are still looking at known actives. Organise those structures that we have found such that only ligands that bind at the relevant location on the protein are included. For instance, for nAChR, we should only include ligands that bind where acetycholine binds. Furthermore, the mol2 files should be aligned with a structure (one for each model system) which can then be used to compare each one relative to one another. Organise each model system into a pymol visualisation file, for ease of visual comparison.
