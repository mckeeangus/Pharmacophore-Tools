# Pharmacophore construction — method

Stage 4 of the pipeline turns each grouped set of aligned active poses into a single
**ligand-based ensemble pharmacophore**: a small set of typed feature spheres (an
H-bond donor here, an aromatic ring there, …) that capture the chemistry the active
ligands share. The approach adapts the TeachOpenCADD **T009** workflow (extract RDKit
features → consensus per family → consensus positions become the model) with the
automation and clean-up changes described below.

Everything scientific lives in **`config/pharmacophore.yaml`**; the code is generic.
The method-defining parameter values quoted here are the current config defaults — the
config is the source of truth if they ever diverge.

### Two consensus strategies behind one flag

The step that turns per-molecule feature points into consensus features is pluggable
via `consensus_method`:

- **`kmeans`** (default) — cluster each family's points with silhouette-selected
  k-means; cluster centres become features (§4–§6).
- **`density`** — accumulate each family's points into a Gaussian-smoothed occupancy
  field and read features off its peaks (§11).

Both obey **one in/out contract** — in: aligned per-molecule feature points in the
binding-site-local frame; out: a list of consensus features `(family, position,
tolerance, optional direction)` — so every downstream artifact (JSON model, CSV, plots,
PyMOL session) is identical in form and the two are directly comparable. Swapping the
method changes feature *positions*, never the output *structure*. Outputs are written to
**separate namespaces** so they sit side by side: k-means →
`catalogue/<slug>/pharmacophores/`, density → `catalogue/<slug>/pharmacophores_density/`.
The default method is unchanged (k-means); select density with
`build-pharmacophores --consensus density` or `consensus_method: density` in config.
Sections 1–3 (build unit, loading, feature extraction) and the tolerance clamp (§6) are
**shared by both strategies**.

---

## 1. The build unit — one cell, one hypothesis

A model is built from one **cell**: `catalogue/<slug>/groups/<pocket>__<efficacy>/`.
Every pose in a cell is already superposed into a common reference frame (Stage 2/3),
sits in the **same verified pocket**, and carries the **same efficacy sign**. So one
cell = one coherent set of "molecules that do the same thing in the same place", which
is exactly what a single pharmacophore hypothesis should describe.

The build is general: the real entry point (`build_from_directory`) takes *any*
directory of aligned `*.mol2` and emits a model; the catalogue batch mode
(`build-pharmacophores --catalogue` / `--target <slug>`) is a convenience over it that
also supplies per-target SMILES. For a standalone directory there is a **local one-shot**
that runs the whole methodology end-to-end in one command — protonate (pH 7.4, `prep`
env) → build → render a PyMOL `.pse` + `.png`:

```
pixi run build-pharmacophores --input DIR --out DIR --smiles ligands.csv
```

`--smiles` (a `het_code,smiles` CSV) is required — the heavy-atom mol2 need it for both
protonation and template bond perception. Protonation is reused if already present in
`--out`; `--reference-pdb` enables density excluded volume, and `--force-protonate` /
`--allow-unprotonated` / `--no-render` tune the steps. It shells out across pixi envs, so
it is local-only.

### Minimum-ligands gate

A cell with **fewer than `selection.min_ligands` (= 3) ligands is skipped** and any
model previously written for it is deleted. Two or one ligands cannot define an
*ensemble* (a consensus needs something to be consensual about), so such a "model"
would be an over-fit of one or two molecules dressed up as a hypothesis. Skipping them
is an honest result, not a gap. Cells excluded on this basis at the last run:
`drd1/orthosteric__negative` (1), `chrm2/orthosteric__positive` (2),
`gaba_a/bzd_site__{negative,neutral}` (1 each), `nachr_a4b2/accessory__positive` (1).

> In our `groups/` cells there is exactly one pose per distinct ligand (HET), so
> "ligands" and "poses" coincide and the gate counts chemical diversity directly.

---

## 2. Loading poses (heavy-atom mol2 → RDKit)

Our catalogue mol2 are **heavy-atom-only** with OpenBabel Gasteiger charges. RDKit's
direct mol2 reader is lossy on them — it fails to kekulise aromatic rings and, with no
explicit hydrogens, misses H-bond donors. The loader therefore prefers a
**SMILES-template** path (`features/load.py`):

1. read the mol2 **connectivity** only, reduce it to a clean single-bond graph;
2. transfer the correct bond orders from the ligand's reference SMILES via RDKit's
   `AssignBondOrdersFromTemplate` (SMILES keyed by HET code — see protonation below);
3. fall back to a direct sanitised read; and finally
4. skip the pose and record the reason — one bad pose never aborts a build.

The per-pose outcome (`template` / `direct` / skipped) is reported in each
`model_summary.md`, so feature coverage is auditable.

### Protonation to the pH 7.4 microstate (preprocessing)

The catalogue SMILES are drawn **neutral**, but H-bond donor/acceptor and ±ionizable
perception depends on the protonation state the ligand actually adopts in the pocket — a
basic amine on an aminergic agonist is cationic at physiological pH and must read as a
`PosIonizable`/donor, a carboxylate as `NegIonizable`/acceptor. So before the build, a
preprocessing step replaces each HET's template SMILES with its **dominant microstate at
pH 7.4**:

- pKa values are predicted with **pkasolver** (Mayr *et al.*; a graph-neural-network
  ensemble), run once per unique HET (`scripts/protonate_ligands.py`).
- The dominant microstate is selected by **walking the predicted pKa ladder**
  (`pharmpipe/prep/protonate.py`, `dominant_microstate_at_ph`): from the fully
  protonated species, every site with `pKa ≤ 7.4` is deprotonated; the species reached
  when the next site's `pKa` exceeds 7.4 is taken (Henderson–Hasselbalch ordering). Note
  pkasolver's own "pH 7.4" shortcut is really a dimorphite-dl call at pH 7.0; we use the
  **ML pKa values** at the requested 7.4 instead.
- Output is cached per target in `catalogue/<slug>/protonated_ligands.csv`
  (HET → protonated SMILES + the predicted pKa list); the loader prefers it and falls
  back per-HET to the neutral SMILES for anything pkasolver can't process (salts are
  stripped to the largest fragment first; non-ionizable HETs, e.g. `Mg²⁺`, pass through).
- Because `AssignBondOrdersFromTemplate` carries the **template's formal charges** onto
  the pose, feeding the protonated SMILES is all that is needed — the perceived pose then
  has the correct charges and H-count, and this flows identically into **both** consensus
  strategies.

pkasolver's pretrained checkpoints need a pinned 2021-era stack (python 3.10 / torch
1.11 / torch-geometric 2.0.1), isolated in the pixi **`prep`** environment; pkasolver is
vendored under `external/` (not installed) so its bundled weights load via `__file__`.
The protonation step is the only networked/heavy-ML part and is run once up front
(`pixi run -e prep protonate-ligands`); the build pipeline itself stays offline and only
reads the cached CSV.

#### 2.1 Weak-acid guard (`config/protonation.yaml`)

pkasolver — like every current molecular-graph pKa GNN — is accurate for **isolated**
ionizable centres but systematically **over-deprotonates weak acids (O–H, N–H) that sit
on complex, poly-ionizable scaffolds**. The phenol was the most visible face of it; the
same failure produces the *conjugate base* at pH 7.4 for aliphatic/sugar alcohols,
amides, primary sulfonamides, and amino-heteroaromatics as well.

The mechanism is clearest on phenols (predicted vs experimental phenolic-OH pKa):

| Compound | 2nd group | exp pKa | pkasolver | error |
|---|---|---|---|---|
| phenol | — | 9.99 | 10.03 | +0.0 |
| p-cresol | — | 10.26 | 10.18 | −0.1 |
| 4-nitrophenol | — (EWG) | 7.15 | 8.19 | +1.0 |
| 4-hydroxybenzoic acid | *para* COOH | 9.32 | 6.54 | **−2.8** |
| 3-hydroxybenzoic acid | *meta* COOH | 9.92 | 6.13 | **−3.8** |
| salicylic acid | *ortho* COOH | 13.40 | 4.71 | **−8.7** |

Isolated centres (even large ones, even with a strong EWG like *p*-nitro) are predicted
within ~1 unit; the error appears only once a **second ionizable centre** is present and
grows monotonically as the two centres approach (para → meta → ortho). It decomposes
into (i) a ~3-unit baseline error from **adjacent-charge electrostatics / polyprotic
reference-state handling** — the weak acid is a *second* deprotonation, on a species that
already bears a charge, which the model pushes toward acidic values instead of raising —
and (ii) a further ~5–6 units at *ortho* from an **intramolecular H-bond** (e.g.
phenol-OH···⁻OOC, lifting salicylate's phenol to pKa ≈ 13.4). Both are through-space /
charged-state effects invisible to a 2-D molecular-graph model. This is a **data +
inductive-bias limitation shared across graph pKa GNNs**; we confirmed **QupKake** (a GNN
with added xTB/semi-empirical features + a tautomer front end) gives no material
improvement for its extra cost, because the missing physics is coupled inter-centre /
macrostate behaviour, not the local electronic description it refines.

Because the failure is confined to identifiable classes while isolated-centre prediction
is excellent, the fix is a **general structural prior, not a heavier model and not a
per-compound literature pKa assignment**. Weak-acid classes whose aqueous pKa is well
above 7.4 are re-protonated after the ladder walk; each is a config entry with an
**anion SMARTS** (first atom = the conjugate-base heteroatom) and an optional list of
genuinely-acidic **structural exceptions** that keep pkasolver's deprotonation:

| Class | Guarded (→ neutral at 7.4) | Exceptions (stay deprotonated) |
|---|---|---|
| **phenol** | Ar–OH, pKa ~10 | *o/p*-nitrophenol (⇒ all polynitro), *o/p*-cyanophenol, 2,4,6-tri/perhalophenol |
| **alcohol** | aliphatic/sugar C–OH, pKa ~16 | — (sp3-C anchor already excludes carboxylate/phosphate) |
| **amide** | R–C(=O)–NH, pKa ~17 | imide & acylsulfonamide (excluded in the SMARTS itself) |
| **sulfonamide** | R–SO₂–NH, pKa ~10 | acylsulfonamide (excluded) |
| **aryl_amine** | exocyclic amino/anilino on (hetero)arene | — |

Mechanically the guard (`neutralize_weak_acids`) operates on the **final** microstate:
after the Henderson–Hasselbalch walk, any anion matching a class (and not an exception)
has its formal charge set to 0 and one H added. It is **purely additive** — it never
removes a proton — so it cannot disturb carboxylates, phosphates, protonated amines, or
anything pkasolver already handles correctly, and it is idempotent. Every re-protonated
group is recorded in the `guard_neutralized` column of `protonated_ligands.csv`
(`<class>:<count>`, e.g. `phenol:2;amide:1`) and flips the row's `method` to
`pkasolver+weak_acid_guard`, so the correction is fully auditable.

Deliberately **not** guarded (left to pkasolver, as genuinely acidic or irrelevant):
aromatic ring N–H (tetrazolate, imidazolate), enols / vinylogous acids (tropolones,
tetramic/tetronic acids, 4-hydroxycoumarins), and cofactor lactams (guanine/uracil) —
the last only ever occur in review-track cofactors that never enter a built cell.

> **Sulfonamides & carbonic anhydrase.** A primary arylsulfonamide has solution pKa ~10,
> so its pH-7.4 microstate is neutral — which is what the guard enforces. The one context
> where that is arguable is CA2, whose inhibitors bind the catalytic **Zn²⁺** as the
> deprotonated sulfonamide anion; the solution and bound states genuinely differ there.
> CA2 is out of scope for the intended publication for exactly this reason, so the guard
> applies the consistent solution-state convention everywhere.

---

## 3. Feature extraction (RDKit feature families)

Features are extracted with RDKit's `BaseFeatures.fdef` factory. The modelled families
(`features.families`) are:

`Donor`, `Acceptor`, `LumpedHydrophobe`, `Aromatic`, `PosIonizable`, `NegIonizable`.

Each extracted feature is a `(family, x, y, z)` point in the cell's common frame, tagged
with its source ligand.

**Why `LumpedHydrophobe`, not `Hydrophobe`.** RDKit's per-atom `Hydrophobe` emits one
point *per hydrophobic atom*, so a single alkyl chain or ring face produces a row of
near-duplicate points and hydrophobes swamp the model. `LumpedHydrophobe` collapses a
contiguous hydrophobic group into **one centroid feature**, which both matches how a
pharmacophore should treat a hydrophobic contact and stops that family being
over-represented relative to the others.

### 3.1 Feature hierarchy — resolving co-incident dual classifications

RDKit labels some atoms with **two families at once**: a protonated amine N is *both*
`PosIonizable` and `Donor`; a carboxylate O is *both* `NegIonizable` and `Acceptor`; an
aromatic ring is *both* `Aromatic` and `LumpedHydrophobe`. Left as-is this **double-counts
one atom as two feature points**, so a single protonated nitrogen contributes both a
PosIonizable *and* a Donor point to every ligand — and the more-specific type can then
lose the downstream support/size vote (§5) to its own redundant partner (the classic
symptom: a pocket that should read `PosIonizable` reports a `Donor`).

A curated **`features.feature_hierarchy`** (config, never code) fixes this at extraction,
per ligand, keyed on the **shared atom**. Each group is ordered highest-priority first;
when two families in the same group are perceived on a shared atom, only the higher one
is kept:

```
[PosIonizable, Donor]            [PosIonizable, LumpedHydrophobe]
[NegIonizable, Acceptor]         [NegIonizable, LumpedHydrophobe]
[Aromatic, LumpedHydrophobe]
```

Key properties:

- **Atom-scoped, not global.** A family is dropped only where it *shares an atom* with a
  higher-priority family (`hierarchy_pairs` expands each group into `(higher, lower)`
  subsumes-pairs; a family may head several groups, e.g. `PosIonizable` subsumes both
  Donor and LumpedHydrophobe). A lone aliphatic hydrophobe (no aromatic overlap) is kept.
- **Genuine dual roles are preserved.** `Donor`+`Acceptor` (a hydroxyl) and
  `Aromatic`+`Acceptor`/`Donor` (a pyridine/pyrrole ring heteroatom) are *not* grouped,
  so those atoms keep both features.
- **It never overrides a genuine count.** Its only job is to remove the redundant
  co-incident point; the cross-family merge (§5) stays purely support/size-based, so if a
  region genuinely has more (distinct-atom) donors than cations, the donor still wins.
- **Both consensus strategies benefit**, because the collapse happens upstream of
  clustering/density.

Every collapse is recorded (`kept ← dropped`, with the ligands that carried the dual
classification) in the model's `pharmacophore.json` provenance and a **Feature
resolution** section of `model_summary.md`.

---

## 4. Clustering points into consensus positions (k-means strategy)

> This and §5–§6's selection/merge apply to the **`kmeans`** consensus method (the
> default). The **`density`** method replaces §4–§5 with the occupancy-field procedure
> in §11 but shares §6's tolerance clamp.

For **each family independently**, the family's points (pooled across all the cell's
ligands) are clustered in 3D. The clusterer is injected behind a one-method
`Clusterer` protocol (`fit_predict(coords) -> labels`), so the method is swappable
without changing the output format; methods are registered in
`clustering/registry.py`.

The default is **`kmeans_silhouette`** (`clustering/kmeans.py`): k-means where the
number of clusters *k* is chosen automatically rather than hand-tuned.

**How *k* is chosen.** For every candidate `k ∈ [k_min, min(k_max, n−1)]` (defaults
`k_min = 2`, `k_max = 8`; `n` = number of points in the family) we run k-means
(`n_init = 10` restarts, fixed `random_state` for reproducibility) and score the
resulting partition by its **mean silhouette coefficient**. For a point *i* the
silhouette is

```
s(i) = (b(i) − a(i)) / max(a(i), b(i))
```

where `a(i)` is *i*'s mean (Euclidean) distance to the other points **in its own
cluster** and `b(i)` is its mean distance to the points of the **nearest other
cluster**. `s(i)` runs from −1 (likely misassigned) through 0 (on a boundary) to +1
(tight, well separated); the score for a given *k* is the mean of `s(i)` over all
points. We keep the *k* with the **highest mean silhouette** — the partition whose
clusters are simultaneously most compact and best separated — and return its labels. A
*k* that collapses to a single occupied cluster, or for which the silhouette is
undefined, is skipped. T009 instead fixes `k = ceil(n / kq)` with a hand-tuned `kq`;
its own discussion flags that as the obstacle to automation, so we remove the
hand-tuning. Degenerate inputs (≤ 2 points, or effectively coincident points) collapse
to a single cluster. The chosen method and its parameters are recorded in each model's
provenance block.

Each cluster's **centre** is the (unweighted) **mean of its member points** — a
candidate feature position.

---

## 5. Cluster → kept feature (selection)

A candidate cluster becomes a pharmacophore feature only if it is both **populous** and
**recurrent** (`selection`):

- **support** = (distinct ligands contributing to the cluster) / (ligands in the cell)
  ≥ `min_support_fraction` (= 0.5). This is the T009 "present in most molecules" idea,
  made relative to the cell size — a feature must be shared, not the quirk of one
  ligand. **This 0.5 support floor applies to *both* consensus strategies**: the density
  path enforces the same `min_support_fraction` on each peak (§11.4), so every feature in
  every model — k-means or density — is present in at least half the cell's ligands.
- **size** = number of feature points in the cluster ≥ `min_cluster_size` (= 2).

Support is a **per-feature** quantity, and `model_summary.md` reports it that way — one
row per feature (peak), labelled `<Family> <n>` (e.g. `Donor 1`, `Donor 2`) so two
features of the same family are distinguished. The same label + support annotates each
kept peak in the `raw_features_<family>.png` plots and names the feature objects in the
`.pml` session, so the tables and the visualisations line up.

Candidate features that pass these filters from **every family** are then pooled and
sorted **largest first** (more points, then higher support). The merge (next) and an
optional `top_n_per_family` cap (default off, keeps only the strongest N per family)
are applied to that pooled, sorted list.

### Merging overlapping clusters (within *and across* families)

Two distinct things can put two feature spheres in the same place, and neither should
survive as two features:

- k-means can split one genuinely single dense lobe into two adjacent **same-family**
  clusters; and
- two **different** families can land on the same atoms — a spot cannot be both an
  H-bond donor *and* an acceptor (or a hydrophobe *and* an aromatic) at once, so two
  overlapping features of different families are mutually exclusive too.

So after selection we **collapse overlapping features regardless of family, keeping the
dominant one** (`selection.merge_overlapping`, default on). Working down the pooled
largest-first list, a candidate is dropped if it overlaps any feature already kept —
the first (largest, then highest-support) feature accepted for a region wins, whatever
its family. This is why the merge runs over the pooled set rather than per family.

"Overlap" uses a **non-arbitrary, geometry-derived threshold** rather than a magic
number: two features overlap when their centre-to-centre distance is **less than the
larger of their two tolerance radii** — i.e. one centre lies *inside* the other's
sphere. Because the radius is each cluster's own spatial spread (§6), the merge
distance scales with the data instead of being a fixed cutoff. (An absolute cutoff can
still be forced with `selection.merge_radius`, e.g. `0.75` Å, if a fixed value is ever
wanted.) Dropped clusters also lose their "kept" flag, so the diagnostic plots (§7)
show the merge.

---

## 6. Tolerance radius — the size of a feature sphere

Each kept feature carries a **tolerance radius** = the radius of the **dense core** of
its cluster: the distance from the centre that encloses a fraction `quantile` (= 0.75)
of the feature's density (`tolerance.method: density_quantile`), clamped to
`[min, max] = [1.0, 3.0]` Å.

**How the radius is computed.** For a cluster of member points `pᵢ` with centre `c`
(§4), take the point-to-centre distances `dᵢ = ‖pᵢ − c‖`, weight each by its density
mass `wᵢ` (equal weights for k-means; the molecule-weighted field value for density,
§11), and return the smallest `d` below which a fraction `quantile` of the total weight
lies — a **density-weighted quantile of the distances**:

```
radius = d(q)  such that  Σ_{dᵢ ≤ d(q)} wᵢ  =  q · Σᵢ wᵢ,   q = 0.75,  clamped to [1.0, 3.0] Å
```

This is deliberately **robust to the cluster's tail**: the far points that were still
assigned to the cluster set the last 25% of the mass, not the sphere size, so a few
outliers no longer inflate the radius (contrast the earlier root-mean-square radius,
where every point — including the farthest — entered the mean; that `rmsd` mode is still
available via `tolerance.method`). Lowering `quantile` tightens every sphere uniformly;
raising it toward 1.0 approaches the full extent. The clamp keeps a near-coincident
cluster at ≥ 1 Å and a diffuse one at ≤ 3 Å.

This radius is the **model's** tolerance and the `radius` field in `pharmacophore.json`.
It is a spread measure, but a **core-density** one: a *tight, dense* cluster gives a
*small* radius, a *diffuse* one a *larger* radius (governed by where 75% of the density
sits, not the outermost members).

**Note — it is no longer the PyMOL sphere size.** Drawing each sphere at its tolerance
radius (up to 3 Å) swamped the scene and buried the ligand, so the PyMOL views
(`pharmacophore.pml` and `scripts/pymol_pharmacophore.py`) now render every ligand feature
as a **fixed-radius sphere (`PH4_SPHERE_RADIUS = 0.5 Å`, i.e. a 1.0 Å-diameter ball)**
plus an **opaque centre pseudoatom** (a nonbonded-sphere point marker carrying the
`<Family> <n> (support)` label). The 0.5 Å radius mirrors the overlap-merge rule (§5):
two such spheres just touch when their centres are ~1 Å apart, i.e. exactly when the
model would have collapsed them into one feature. Excluded-volume markers keep their own
steric radius and get **no** centre point.
The true tolerance stays in the JSON; inspect it there (or via `model_summary.md`) rather
than by sphere size.

---

## 7. Outputs per model — `pharmacophores/<pocket>__<efficacy>/`

| File | What it is |
|---|---|
| `pharmacophore.json` | Canonical, schema-versioned model (`pharmpipe.pharmacophore/v1`): each feature's family, centre, **tolerance radius**, point count, ligand support, plus a provenance block (clustering method/params, selection/tolerance settings, load coverage, the representative ligand). Method-stable — swapping the clusterer changes positions, not structure. |
| `features.csv` | Every raw extracted point (family, source ligand, x/y/z, cluster id, **kept** flag) — the data behind the model, for auditing clustering quality. |
| `representative_ligand.sdf` | One real ligand from the cell, written from the RDKit-perceived molecule (correct bond orders + 3D coords), used as the visual scaffold (§8). |
| `raw_features_<family>.png` | Per-family 3D scatter of the raw points, coloured by cluster, with cluster centres marked and each kept peak annotated with its label + support (§9). |
| `pharmacophore.pml` | Lightweight self-contained PyMOL script: loads `representative_ligand.sdf` + the feature spheres (each object named `<Family>_<n>` and labelled with its support). |
| `model_summary.md` | Human-readable summary: load coverage, representative ligand, and one row **per feature (peak)** — its `<Family> <n>` label, point/ligand counts, and support — followed by a **Feature resolution** section (§3.1 hierarchy collapses) and a **Not selected** table listing clusters/peaks that formed but did not enter the model (below the support/size floor or displaced by the overlap merge) with their mean support. Excluded-volume spheres (density strategy, §11.6) are receptor markers with no peak or support, so they are reported as a single **count** line rather than listed in the per-feature table. |

Richer inspection (raw-point overlay):
`pixi run -e viz pymol -cq scripts/pymol_pharmacophore.py -- --pharmacophore … [--features … --compounds … --out …]`.
With no `--compounds`, the script shows the clean `representative_ligand.sdf` beside the
JSON.

---

## 8. The representative ligand (visual scaffold)

The cell's raw mol2 are heavy-atom-only and render with spurious bonds in PyMOL, so the
visualisation no longer dumps the whole malformed pose set. Instead one **real ligand
from the cell** is chosen as a clean scaffold to sit inside the feature spheres.

Selection (`best_representative`): the ligand whose own features **best fit the built
model** — scored as the fraction of kept features for which the ligand has a feature of
the same family inside that feature's tolerance sphere (ties broken toward the
richer ligand). It is written to `representative_ligand.sdf` from the
already-perceived RDKit molecule, so its bond orders and coordinates are correct and it
displays cleanly. (It is a viewing aid, not part of the model definition.)

---

## 9. Feature colours and cluster size in the plots

**Family colours** (shared by the PyMOL session and the matplotlib plots,
`features.colors`):

| Family | Meaning | Colour |
|---|---|---|
| `Donor` | H-bond donor (HBD) | pink |
| `Acceptor` | H-bond acceptor (HBA) | green |
| `LumpedHydrophobe` | hydrophobic | cyan |
| `Aromatic` | aromatic ring | yellow |
| `PosIonizable` | positive ionisable | red |
| `NegIonizable` | negative ionisable | orange |
| `ExcludedVolume` | receptor no-go region (density strategy only, §11) | grey |

**Sizes in the visualisations** encode two different, deliberately distinct things:

- **PyMOL feature spheres** — a **fixed 0.5 Å** radius (a 1.0 Å-diameter ball, matching
  the §5 overlap-merge rule — spheres just touch when features' centres are ~1 Å apart,
  i.e. when they would merge), with an opaque centre
  pseudoatom marking each feature's exact position (excluded-volume markers keep their
  own radius and get no centre point). (The feature's tolerance radius is *not* shown as
  sphere size any more — read it from the JSON / `model_summary.md`.)
- **`raw_features_<family>.png` cluster-centre markers** — the marker **area scales with
  the cluster's point count** (its population / local density): a bigger marker means
  more raw feature points were collapsed into that centre. Kept clusters are drawn as a
  filled "X", clusters dropped by selection or merging as a thin "x". This is the
  "sense of the data" view for judging whether the clustering suits the distribution.

So "cluster size" means *spread* on the model spheres and *population/density* on the
diagnostic markers — both are stated on the artifacts they appear on.

---

## 10. Scope

Batch modes build only the `groups/` cells — never the `separate_state` / `unknown` /
`quarantine` review tracks. Surrogate/chimera/mismatch poses must be gated per
`curation/efficacy_curation_README.md` before pooling (a surrogate pose carries the
surrogate's pocket geometry; `mismatch` poses are wrong-target structures). The
downstream DrugCLIP → docking flow is out of scope for this stage.

---

## 11. Density-based consensus strategy (`consensus_method: density`)

An alternative to the k-means path (§4–§5) that consumes the **same** per-molecule
feature points (§1–§3) and emits the **same** consensus-feature output (§6's tolerance
clamp included), so it is a drop-in behind the `consensus_method` flag and downstream
code never branches on it. It is implemented in `pharmpipe/pharmacophore/density.py`
and dispatched, alongside k-means, by `pharmacophore/consensus.py` — the single seam the
orchestrator calls.

**Motivation and lessons carried over from k-means.** The k-means write-up's core
lesson was *removing a hand-tuned knob* (T009's `kq` for k → silhouette automation,
§4). The density strategy takes that further: by reading features off the **peaks of a
smoothed density field**, the number of features of each type is *emergent* — each
conserved sub-site is its own peak — so **no `k` is chosen at all**. It also keeps the
other k-means lessons that still apply: the **min-ligands gate** (§1) and the
**heavy-atom-mol2 SMILES-template loading** (§2) are upstream and shared unchanged; the
**tolerance clamp** `[1.0, 3.0] Å` (§6) is reused; **`LumpedHydrophobe`** (§3) is still
the hydrophobic family; and determinism is preserved — like seeded k-means, the density
field uses a **fixed grid, bandwidth and threshold with no random seeding**, so a rerun
is bit-stable.

The strategy runs **independently per feature type** (HBD/Donor, HBA/Acceptor,
LumpedHydrophobe, Aromatic, PosIonizable, NegIonizable). For each type:

### 11.1 Pool points and weight by molecule, not by point

All of that type's points are pooled across the cell's aligned actives. Each point is
weighted by

```
w_i = 1 / (number of points molecule m(i) contributes to this type)
```

so **the unit of evidence is the distinct molecule**, not the raw point: a molecule that
happens to place six hydrophobe points and one that places one each count once. (With
`scaffold_weighting: true` the weight is additionally divided by the molecule's Murcko
scaffold frequency, so an over-represented scaffold does not bias the field; off by
default.) The weights of one molecule's points sum to 1, so the field is a map of
distinct-molecule occurrence — directly the "occurrence frequency" idea from dynophore
super-features.

### 11.2 Accumulate into a Gaussian-smoothed occupancy field

The weighted points are deposited into a fixed **voxel grid** spanning their bounding box
plus a margin of `3·bandwidth`, then convolved with a Gaussian of width `bandwidth`
(implemented as `scipy.ndimage.gaussian_filter` with `sigma = bandwidth / voxel`, which
is an exact, deterministic kernel-density estimate on the grid). **Voxel and bandwidth
are the single length knob** (~1.0–1.5 Å, ≈ the target feature tolerance). The result is
an **occupancy field**: high where many distinct molecules place that feature type.

### 11.3 Extract every local maximum; assign by nearest peak (watershed)

**All** local maxima of the field are found (a voxel whose value equals its 3×3×3
neighbourhood maximum and exceeds a tiny noise floor). Maxima closer than one `bandwidth`
cannot be physically resolved at that smoothing, so near-coincident peaks are collapsed
keeping the taller — the *only* post-filter on the field. Every above-floor voxel, and
every point, is then assigned to its **nearest maximum** (a proximity watershed), giving
one **basin** per peak. This is what yields multiple features of one type natively, with
no `k`.

The **minimum peak spacing is the `bandwidth` itself** — deliberately not a separate
knob. The Gaussian smoothing (sigma = bandwidth) is the field's resolution limit: two
maxima nearer than that are the same site, and a smaller spacing would only *over-split* a
single lobe into ripple sub-peaks that can each fall below the `occupancy_floor` (§11.4)
and be lost. To genuinely resolve sub-sites closer than the bandwidth, lower `bandwidth`
*and* `voxel` together, not a spacing knob.

### 11.4 Keep peaks that clear the occupancy floor *and* the support floor

A basin becomes a feature only if it clears **two** thresholds:

1. its **summed distinct-molecule weight** (Σ `w_i` over the points assigned to it) is at
   least `occupancy_floor` (default `2.0`, i.e. ~two distinct molecules of evidence) — the
   density's own knob. Because the weights are per-molecule, a single molecule's dense
   blob cannot clear a floor of 2 however many points it has; and
2. its **support** — (distinct ligands in the basin) / (ligands in the cell) — is at
   least `min_support_fraction` (= 0.5), the **same support floor as the k-means path**
   (§5), threaded in from `selection`. So a feature is present in ≥ half the cell's
   ligands whichever strategy built it.

The occupancy floor is an *absolute* molecule count and the support floor a *fraction*;
for a large cell the fraction is the stricter gate, for a tiny one the count is.

### 11.5 Collapse each kept basin to one feature

- **position** = the **density-weighted centroid** of the basin: `Σ f_v·x_v / Σ f_v`
  over the basin's voxels `v` (weights `f_v` = field value). This places the feature at
  the field's centre of mass, not a bare point mean.
- **tolerance** = the **density-quantile radius of the basin** (§6): the field values
  `f_v` are the density weights, and the radius is the field-weighted quantile of the
  voxel-to-centroid distances — the distance enclosing `quantile` (= 0.75) of the basin's
  field mass, clamped to `[1.0, 3.0] Å`. This reads the sphere off the **core** of the
  occupancy contour rather than its diffuse tail, using the identical `feature_radius`
  helper (and `tolerance` config) as the k-means path, so the sphere means the same thing
  in both strategies.
- **direction** — for projected families (HBD/HBA) the model carries an optional mean
  unit vector. Our current feature perception (heavy-atom mol2 → RDKit `BaseFeatures`)
  does not emit per-point projection vectors, and perception is upstream and out of
  scope to change here, so `direction` is `None` in practice; the field is plumbed
  through the model and the averaging will populate it the moment perception supplies
  per-point directions. (We do **not** fabricate a direction — that would encode a
  scientific decision in code, which the project rules forbid.)

### 11.6 Excluded-volume spheres from the receptor

Finally, **excluded-volume** spheres mark pocket regions the receptor occupies but no
ligand reaches — the steric complement of the ligand envelope. Using the aligned
reference receptor (`data/targets/<slug>/reference.pdb`, already in the ligands' frame),
a protein heavy atom qualifies when its nearest ligand atom is **within `ev_shell`**
(5 Å — it lines the pocket) yet **beyond `ev_clearance`** (2 Å — the ligand does not
reach it). Qualifying atoms are coarsened onto an `ev_voxel` (2 Å) grid — one sphere per
occupied cell at its atoms' mean, radius `ev_radius` (1 Å) — and the `ev_max` (40)
nearest the ligand cloud are kept, family `ExcludedVolume` (grey, §9). Excluded volume
needs a receptor, so it is built only in catalogue/target mode (where the reference is
available) and is skipped cleanly for a bare `--input` directory; toggle with
`density.excluded_volume`.

### 11.7 Knobs, determinism, and differences from k-means

**Only two scientific knobs of its own**: the length scale (`voxel`/`bandwidth`, which
also sets the minimum peak spacing, §11.3) and the `occupancy_floor`; the excluded-volume
parameters are a self-contained steric add-on. In
addition it honours the **shared `min_support_fraction` floor** from `selection` (§11.4),
so its features meet the same "present in ≥ half the ligands" bar as the k-means path —
this is a selection policy common to both strategies, not a density-specific knob.
Everything is deterministic — fixed grid, fixed bandwidth, fixed floors, no seeding —
so reruns are identical (asserted in `tests/test_density.py`).

**Cross-family overlap merge.** After the per-type peaks are selected, the density path
applies the **same family-agnostic overlap merge as k-means** (§5): the pooled features
are sorted dominant-first (points, then support) and any feature overlapping a stronger
one already kept is dropped — so a region of space yields **exactly one feature** even
when a donor and an acceptor field both peak on the same atoms (`density.merge_overlapping`,
default on; geometric threshold, or an absolute `density.merge_radius`). Excluded-volume
spheres are added *after* the merge and are exempt (they are receptor markers, not ligand
chemistry). The dropped basins lose their "kept" flag so the diagnostic plots show it.

The one deliberate difference from k-means that remains: features of one type emerge from
field peaks rather than a chosen `k`. The two methods are meant to be compared side by
side from their separate namespaces.

**Precedent** (the strategy is an automation of established field/consensus ideas):
dynophore cloud → super-feature with occurrence frequency (Wolber lab); field-maximum
extraction from interaction fields (GBPM; FLAPpharm, Baroni *et al.*); Gaussian
feature-density molecular representation (Tanrikulu & Schneider); occupancy/frequency
thresholding across multiple complexes (REPHARMBLE; SARS-CoV-2 Mpro consensus
pharmacophores). These are cited in the module docstrings (`density.py`).
