# Stage-4 tools reference — DrugCLIP pharmacophore construction & evaluation

A one-stop index of the tools built for constructing pharmacophores from DrugCLIP → GNINA
screening output and evaluating them. Full method write-up: `catalogue/pharmacophore_method.md`;
project context: `CLAUDE.md` (Stage 4). All Python runs through **pixi** (`pixi run …`), never a
bare `python`.

## Construction — `pixi run build-pharmacophores` (scripts/build_pharmacophores.py)

| Mode | What it does |
|---|---|
| `--catalogue` / `--target <slug>` | Known-actives build: one model per `(pocket × efficacy)` cell from the curated catalogue. |
| `--input DIR --out DIR --smiles csv` | One-shot from any directory of aligned `*.mol2` (protonate → build → render). |
| `--docked-dir DIR --out DIR --top-hits N [--top-poses n] [--pose-score cnnaffinity] [--max-vina 0]` | **Full-docking**: build one hypothesis from a whole DrugCLIP→GNINA hit set (`<mol_id>_docked.sdf` + `index_*.csv`), poses chosen by binding quality. |
| `--seed-docked DIR --out DIR --top-hits 100 [--seedless \| --seed s.sdf \| --seed-k 5] [--align-only]` | **Feature-alignment engine** (recommended `--seedless`): conformer ensembles → iterative feature-clique alignment (relative intra-molecular distances → Bron–Kerbosch → Kabsch) with EM refinement and directional (orientation-aware) matching → KDE model. `--align-only` emits just the aligned compound set. |
| `--render-sweeps` | Bake the support-sweep `.pse` for every built catalogue model (viz env). |

Key knobs live in `config/pharmacophore.yaml` (`density`, `selection`, `tolerance`, `alignment`).
The `alignment:` block (conformers, clique `dist_tol`/`min_clique`, `max_align_rmsd`,
`em_iterations`, `use_directions`, `seed_k`) is consumed **only** by `--seed-docked`, keeping it
orthogonal to the catalogue build.

**Seeding is engine-agnostic.** Seed poses are any docked SDFs; `docs/adfr_seeding.md` gives the
AutoDockFR procedure + the seed-pose input contract. A seed is optional and generally **less
effective** than `--seedless` (a docked/crystal frame can import a bad pose).

## Screening organisation & evaluation (src/pharmpipe/screening/, scripts/)

| Script | Purpose → output |
|---|---|
| `organise_screening.py` | Organise the raw `out/` + `website_output/` deposit into `data/screening/<key>/` via the curated crosswalk (`config/screening.yaml`), each pairing validated by ≥99% mol_id overlap. |
| `eval_align_depth.py` | Choose the seed-alignment depth against the known-actives models → sets `alignment_depth`. |
| `evaluate_screening.py` | Build **both** methods (full-docking + seed-alignment) per target and score vs known-actives + literature → `catalogue/screening_eval/comparison_report.md`, `analysis.md`. |
| `eval_geometry_limit.py` | Chemistry-vs-geometry decomposition (is the chemistry there but the alignment off?) → `geometry_limit_report.md`. |
| `troubleshoot_seed_align.py` | 5KXI parameter sweep + benchmark of the seed-alignment recipe → `nachr_a4b2_positive/seed5_benchmark.md`. |
| `seed_necessity.py` | nAChR 3-way (crystal / docked / seedless) — is a seed necessary for correct convergence? → `nachr_a4b2_positive/seed_necessity.md`. |
| `seed_necessity_all.py` | Generalises the above (docked vs seedless) across all known-actives targets → `seed_necessity_report.md`. |
| `directional_benchmark.py` | A/B of orientation-aware matching on the acceptor → `nachr_a4b2_positive/directional_benchmark.md`. |
| `alignment_vs_reference.py` | Seedless model vs the crystal (known-actives) **and** literature pharmacophores → `alignment_vs_reference.md`. |

Comparison metric: `screening/compare.py` (feature-family recall + frame-independent internal
geometry vs a reference; family composition vs literature). Curated inputs are config:
`config/screening.yaml` (crosswalk, depth) and `config/literature_pharmacophores.yaml`.

## Data & references (gitignored bulk, documented here)

- `docs/molecule_library.md` (+ `molecule_library_manifest.csv`) — the ~18.6 M-molecule DrugCLIP
  source library (`molecule_library/`, ~48 GB, gitignored).
- `docs/adfr_seeding.md` — producing seed poses with AutoDockFR (Gadi), and the seed-pose contract.
- Raw docking deposit (`out/`, `website_output/`) and organised sets (`data/screening/`) are
  gitignored; the tracked deliverable is `catalogue/screening_eval/` (models + reports).

## Tests

Offline unit tests (`pixi run -e dev pytest`): `test_dock_load` (pose selection/quality),
`test_align` (clique alignment, EM, directionality, conformers, aligned-SDF), `test_screening`
(crosswalk validation, comparison metric), plus the existing feature/density/pharmacophore tests.

## Method animation

`docs/method_animation/` — an explanatory animation of the construction method (the 9 signposted
steps, conformer generation → seedless alignment → EM refinement → directional matching →
feature abstraction → KDE → final model): `pharmacophore_method.html` (interactive, self-contained)
plus linear `pharmacophore_method.gif` / `.mp4` renders. Regenerate with `pixi run python
docs/method_animation/render_animation.py` (the MP4 step needs `imageio-ffmpeg` or a system ffmpeg;
the GIF always works). Excluded from lint (standalone viz tooling, not pipeline code).
