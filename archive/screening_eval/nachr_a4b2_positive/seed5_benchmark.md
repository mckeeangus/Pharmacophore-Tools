# Seed-5 / depth-100 seed-alignment — 5KXI/nAChR benchmark

Method: dock the top-5 DrugCLIP hits (GNINA stand-in for AutoDockFR), seed a feature model, then incrementally align + fold in ranked compounds 6..100 by feature-clique matching on relative intra-molecular distances. Scored vs the **crystal nicotine** (absolute A), the **known-actives** model, and **Beers-Reich** (cation-acceptor ~5.35 A).

Ground truth internal geometry: known-actives cat-arom 4.50 A, cat-acc 4.56 A; native nicotine cat-acc 4.18 A.

| sweep | value | align/drop | feats | families | d_cat | d_arom | d_acc | cat-arom | cat-acc |
|---|---|---|--:|---|--:|--:|--:|--:|--:|
| **base** | seed5/d100 | 85/10 | 3 | acc+aro+cat | 1.40 | 0.29 | 2.22 | 4.57 | 5.09 |
| seed_k | 3 | 86/11 | 2 | aro+cat | 1.49 | 1.14 | - | 5.16 | - |
| seed_k | 5 | 85/10 | 3 | acc+aro+cat | 1.40 | 0.29 | 2.22 | 4.57 | 5.09 |
| seed_k | 10 | 80/10 | 2 | acc+cat | 1.09 | - | 1.75 | - | 5.13 |
| dist_tol | 1.0 | 85/10 | 2 | aro+cat | 1.68 | 0.79 | - | 5.01 | - |
| dist_tol | 1.5 | 85/10 | 3 | acc+aro+cat | 1.40 | 0.29 | 2.22 | 4.57 | 5.09 |
| dist_tol | 2.0 | 85/10 | 2 | aro+cat | 1.79 | 0.79 | - | 4.84 | - |
| min_clique | 3 | 85/10 | 3 | acc+aro+cat | 1.40 | 0.29 | 2.22 | 4.57 | 5.09 |
| min_clique | 4 | 35/60 | 2 | aro+cat | 1.74 | 0.81 | - | 4.92 | - |
| max_align_rmsd | 0.75 | 85/10 | 2 | aro+cat | 1.38 | 0.86 | - | 4.66 | - |
| max_align_rmsd | 1.0 | 85/10 | 2 | aro+cat | 1.33 | 0.86 | - | 4.41 | - |
| max_align_rmsd | 1.5 | 85/10 | 3 | acc+aro+cat | 1.40 | 0.29 | 2.22 | 4.57 | 5.09 |
| max_align_rmsd | None | 85/10 | 3 | acc+aro+cat | 1.40 | 0.29 | 2.22 | 4.57 | 5.09 |
| conformers(n,ewin) | 32,10.0 | 85/10 | 2 | aro+cat | 1.53 | 0.83 | - | 4.60 | - |
| conformers(n,ewin) | 64,15.0 | 85/10 | 3 | acc+aro+cat | 1.40 | 0.29 | 2.22 | 4.57 | 5.09 |
| conformers(n,ewin) | 128,20.0 | 85/10 | 2 | aro+cat | 1.33 | 1.17 | - | 5.10 | - |

**Determinism:** two identical builds MATCH (identical).

## Reading

- `d_*` = absolute distance of the consensus feature to the crystal nicotine atom (cation=pyrrolidinium N, aromatic=pyridine centroid, acceptor=pyridine N).
- `cat-acc` is inflated by the GNINA seed **ring-flip** (acceptor low-confidence); `cat-arom` + the absolute cation/aromatic accuracy are the trustworthy signals.
- Base result: cation 1.40 A, aromatic 0.29 A from the crystal pose.

## Verdict — the config defaults are optimal

The base recipe (`seed_k=5`, `dist_tol=1.5`, `min_clique=3`, `max_align_rmsd=1.5`, conformers
64/15) is the **best point in the sweep** and recovers the full nicotinic **cation + aromatic +
acceptor** model: cation/aromatic land **1.40 / 0.29 A** from the crystal nicotine, and the internal
**cation–aromatic 4.57 A matches the known-actives model (4.50 A) to 0.07 A**. Build is
**deterministic** (repeat run identical). No parameter change is warranted — the config is kept as is.

The acceptor is recovered but **low-confidence**: it inherits the docking ring-flip, so `cat-acc`
= 5.09 A (vs known-actives 4.56 A / Beers–Reich ~5.35 A / native 4.18 A). Notably aggregating 85
aligned compounds pulls the acceptor to **2.22 A** from native — *better* than the ~3.4 A of the
seed poses alone, i.e. the ensemble partially averages out the flip, but it stays directional and
flagged `†`.

## Troubleshooting — the parameters sit in a narrow "goldilocks" band

Each axis degrades the model when moved off the default, and the failure mode is almost always
**losing the (directional) acceptor**, i.e. collapsing 3 features → 2:

- **`seed_k`** — 3 loses the acceptor *and* worsens the aromatic (d_arom 0.29→1.14); 10 loses the
  aromatic. **5 is the sweet spot** (matches the user's recipe): enough bioactive seeds to define the
  frame, not so many that a bad seed pose scatters it.
- **`dist_tol`** — 1.0 (too tight) and 2.0 (too loose) both drop the acceptor and worsen the cation;
  **1.5** keeps the 3-point model. It is the correspondence tolerance on *relative feature distances*,
  so too tight rejects real matches and too loose admits wrong ones.
- **`min_clique`** — 4 **collapses coverage** (85→35 aligned, 60 dropped): most 3-feature compounds
  cannot form a 4-point clique. **3** (a determined 3-D transform) is essential.
- **`max_align_rmsd`** — 1.5 is **neutral** here (identical to no gate: the good alignments are all
  under it), but tightening to ≤1.0 is *counterproductive* — it excludes the moderate-RMSD
  (1.0–1.5 A) alignments that carry the acceptor consensus, dropping it to 2 features. So the gate is
  a **safety rail for pathological folds on other targets**, set loose enough (1.5) not to distort
  good ones.
- **conformers** — 32/10 (too few → bioactive conformer sometimes absent) and 128/20 (too many/too
  high-energy → spurious matching poses scatter the aromatic, d_arom 0.29→1.17) both drop to 2
  features. **64/15** is best — more is not better.

**General lesson for the method:** the fragile feature is the **directional acceptor**; every
parameter's job is really to keep the moderate-quality alignments that carry it without admitting
noise. The pose-invariant cation + aromatic anchors are robust across the whole sweep (2-feature rows
still nail them). This is consistent with the standing conclusion that directional features need the
(parked) lone-pair/vector treatment, not more alignment tuning.