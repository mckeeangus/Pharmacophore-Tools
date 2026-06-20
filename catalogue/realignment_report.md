# Realignment — robust binding-site superposition (2026-06-20)

## Problem

Surrogate poses (AChBP for nAChR, dDAT for NET) overlaid poorly at the binding
site, which corrupts pose comparison for pharmacophore construction. The
`pocket_rmsd` reported in `site_filter.csv` looked fine (all < 2 Å) because it
averages Calpha over the whole 10 Å pocket shell — that average hides drift of the
residues that actually line the pocket.

A focused diagnostic (`scripts/diag_alignment.py`) measures the **inner-site Calpha
RMSD**: reference pocket residues within 8 Å of the anchor, after the alignment
transform. That is the quantity the pharmacophore depends on. It exposed the issue:

| target (group) | inner-site RMSD, OLD | inner-site RMSD, NEW |
|---|---|---|
| nachr_a4b2 **surrogate** (AChBP) | median 1.18, max 2.20, p90 1.92 | **median 0.71, max 1.14, p90 1.00** |
| net_slc6a2 **surrogate** (dDAT) | median 1.00, max 1.27, p90 1.18 | **median 0.92, max 1.26, p90 1.17** |
| nachr_a4b2 native | 0.16 | 0.16 |
| net_slc6a2 native | 0.58 | 0.53 |
| esr1 native | 0.50 | 0.42 |
| adora2a native | 0.25 | 0.20 |
| ache native | 0.25 | 0.23 |

AChBP — the worst case — improved ~40 % on every statistic; natives held or
improved slightly (no regression). Kept-pose counts are essentially unchanged, so
this is a quality fix, not a change of which poses qualify.

## Why the old fit drifted

The old strategy did a sequence-aware global fit then **one** proximity-paired
Calpha refinement over the *whole* pocket shell, weighted uniformly. For a
low-identity surrogate (AChBP ≈ 20–24 % identity to human α4/β2) the single fit is
a compromise over a divergent subunit, and a uniform shell average lets the
immediate site slide while distant shell residues pull the rotation.

## New strategy (`src/pharmpipe/sites/align.py`)

The global sequence fit is now only an **initialiser**. It is followed by an
**iterative closest-point (ICP) refinement focused on the binding site**:

1. Restrict the working set to candidate residues near the pocket (so distant
   chains cannot mis-pair).
2. Each iteration: re-pair every reference pocket residue to its nearest candidate
   residue (capture radius `refine_pair_radius`), then re-superpose on the paired
   **backbone atoms** (N, CA, C, O — 4× the orientational constraint of Calpha
   alone), **weighting** each residue by a Gaussian on its Calpha–anchor distance
   (`anchor_weight_sigma`) so the immediate site dominates.
3. Iterate to convergence (`refine_iterations`).

Re-pairing each iteration is what lets the fit recover from a rough surrogate
initialiser; the anchor weighting is what holds the *nearby* residues constant.
All knobs live in `config/sites.yaml` (`defaults:`), not in code. A σ sweep set the
defaults: weighting beats unweighted (AChBP 0.81→0.76, dDAT 0.98→0.92 at σ=6);
σ=6 Å balances surrogate accuracy against worst-case stability (σ=4 lowered dDAT
slightly but inflated AChBP's max to 1.67).

## Where it can't go further — and why that's correct

dDAT improved only modestly (1.00→0.92 Å). A rigid-body superposition's RMSD is
**lower-bounded by the genuine structural divergence** between the surrogate and the
human pocket: *Drosophila* dDAT and human NET have real backbone differences in the
S1 site that no rotation/translation can remove. The improvement on AChBP
(1.18→0.71) was the *avoidable* fit-suboptimality; dDAT's residual is mostly
*physical* difference, not a fixable algorithm fault. The valid response is to keep
surrogate poses labelled (already done — `pose_source: surrogate` in the curation)
and treat surrogate-built hypotheses with the documented care, rather than to
distort geometry to force a lower number.

Reproduce the metric: `pixi run python scripts/diag_alignment.py [--targets …]`.
