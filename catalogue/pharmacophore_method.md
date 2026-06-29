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
also supplies per-target SMILES.

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
   `AssignBondOrdersFromTemplate` (SMILES keyed by HET code from the target's
   `unique_ligands.csv`);
3. fall back to a direct sanitised read; and finally
4. skip the pose and record the reason — one bad pose never aborts a build.

The per-pose outcome (`template` / `direct` / skipped) is reported in each
`model_summary.md`, so feature coverage is auditable.

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
  ligand.
- **size** = number of feature points in the cluster ≥ `min_cluster_size` (= 2).

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

Each kept feature carries a **tolerance radius** = the **spatial spread of its
cluster's points about the centre**, measured as their root-mean-square distance
(`tolerance.method: rmsd`) and clamped to `[min, max] = [1.0, 3.0]` Å.

**How the spread is computed.** For a cluster of `m` member points `pᵢ` with centre
`c` (the mean point, §4), the radius is the RMS of the point-to-centre distances:

```
radius = sqrt( (1/m) · Σᵢ ‖pᵢ − c‖² ),  then clamped to [1.0, 3.0] Å
```

i.e. the square root of the mean squared Euclidean distance from each feature point to
the cluster centre (equivalently the standard deviation of the points' positions about
their mean, taken in 3D). It is **not** a fitted Gaussian or a max-radius — every
member point contributes, so one outlier widens it but cannot dominate, and the clamp
keeps a lone outlier from ballooning the sphere past 3 Å or a near-coincident cluster
from collapsing below 1 Å.

This radius is the feature's **size in every visualisation** — the PyMOL spheres are
drawn at exactly this radius. It is a **spread / dispersion** measure, so it is
inversely related to density: a *tight, dense* cluster (all ligands place that feature
in nearly the same spot) gives a *small* sphere, while a *diffuse, low-density* cluster
gives a *large* one (capped at 3 Å so a single outlier can't balloon it). Reading the
model, a small sphere = a geometrically well-agreed, confident feature; a large sphere =
a feature whose exact position the ligands agree on only loosely.

---

## 7. Outputs per model — `pharmacophores/<pocket>__<efficacy>/`

| File | What it is |
|---|---|
| `pharmacophore.json` | Canonical, schema-versioned model (`pharmpipe.pharmacophore/v1`): each feature's family, centre, **tolerance radius**, point count, ligand support, plus a provenance block (clustering method/params, selection/tolerance settings, load coverage, the representative ligand). Method-stable — swapping the clusterer changes positions, not structure. |
| `features.csv` | Every raw extracted point (family, source ligand, x/y/z, cluster id, **kept** flag) — the data behind the model, for auditing clustering quality. |
| `representative_ligand.sdf` | One real ligand from the cell, written from the RDKit-perceived molecule (correct bond orders + 3D coords), used as the visual scaffold (§8). |
| `raw_features_<family>.png` | Per-family 3D scatter of the raw points, coloured by cluster, with cluster centres marked (§9). |
| `pharmacophore.pml` | Lightweight self-contained PyMOL script: loads `representative_ligand.sdf` + the feature spheres. |
| `model_summary.md` | Human-readable summary: load coverage, representative ligand, features kept per family, mean support. |

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

- **PyMOL feature spheres** — radius = the feature's **tolerance radius** (§6), i.e. its
  spatial *spread* (small = dense/confident, large = diffuse).
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
neighbourhood maximum and exceeds a tiny noise floor). Maxima closer than one
`bandwidth` cannot be physically resolved at that smoothing, so near-coincident peaks
are collapsed keeping the taller — the *only* post-filter on the field. Every above-floor
voxel, and every point, is then assigned to its **nearest maximum** (a proximity
watershed), giving one **basin** per peak. This is what yields multiple features of one
type natively, with no `k`.

### 11.4 Keep peaks that clear the occupancy floor

A basin becomes a feature only if its **summed distinct-molecule weight** (Σ `w_i` over
the points assigned to it) is at least `occupancy_floor` (default `2.0`, i.e. ~two
distinct molecules of evidence). This is the density analogue of k-means' support
threshold (§5), and the **second and last knob**. Because the weights are per-molecule,
a single molecule's dense blob cannot clear a floor of 2 however many points it has.

### 11.5 Collapse each kept basin to one feature

- **position** = the **density-weighted centroid** of the basin: `Σ f_v·x_v / Σ f_v`
  over the basin's voxels `v` (weights `f_v` = field value). This places the feature at
  the field's centre of mass, not a bare point mean.
- **tolerance** = the **field spread at the basin**: the field-weighted RMS distance of
  the basin's voxels from that centroid,
  `sqrt( Σ f_v·‖x_v − centroid‖² / Σ f_v )`, clamped to `[1.0, 3.0] Å` (§6). This is the
  second moment of the occupancy contour — a tight peak → small sphere, a diffuse peak →
  large sphere — directly comparable to the k-means RMSD radius.
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

**Only two scientific knobs**: the length scale (`voxel`/`bandwidth`) and the
`occupancy_floor`; the excluded-volume parameters are a self-contained steric add-on.
Everything is deterministic — fixed grid, fixed bandwidth, fixed floor, no seeding —
so reruns are identical (asserted in `tests/test_density.py`).

Two deliberate differences from the k-means path: (1) features of one type emerge from
peaks rather than a chosen `k`; (2) density does **not** apply the cross-family overlap
merge that k-means does (§5) — its per-type fields are independent by construction, and a
group that is genuinely both a donor and an acceptor (e.g. a hydroxyl) is left as both,
which is chemically faithful. The two methods are meant to be compared side by side from
their separate namespaces, not reconciled.

**Precedent** (the strategy is an automation of established field/consensus ideas):
dynophore cloud → super-feature with occurrence frequency (Wolber lab); field-maximum
extraction from interaction fields (GBPM; FLAPpharm, Baroni *et al.*); Gaussian
feature-density molecular representation (Tanrikulu & Schneider); occupancy/frequency
thresholding across multiple complexes (REPHARMBLE; SARS-CoV-2 Mpro consensus
pharmacophores). These are cited in the module docstrings (`density.py`).
