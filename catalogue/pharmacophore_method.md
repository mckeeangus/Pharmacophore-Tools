# Pharmacophore construction — method

Stage 4 of the pipeline turns each grouped set of aligned active poses into a single
**ligand-based ensemble pharmacophore**: a small set of typed feature spheres (an
H-bond donor here, an aromatic ring there, …) that capture the chemistry the active
ligands share. The approach adapts the TeachOpenCADD **T009** workflow (extract RDKit
features → cluster per family → cluster centres become the model) with the automation
and clean-up changes described below.

Everything scientific lives in **`config/pharmacophore.yaml`**; the code is generic.
The method-defining parameter values quoted here are the current config defaults — the
config is the source of truth if they ever diverge.

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

## 4. Clustering points into consensus positions

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
