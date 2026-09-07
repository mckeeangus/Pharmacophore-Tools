# Chemistry vs docking-geometry — is the pattern library-wide?

Seed-5 / depth-100 seed-alignment per target. **chem** = fraction of the top-100 carrying the group (hard ceiling); **geom** = of those carriers, fraction placing it at the model consensus (within 1.5 A). Low geom with high chem => the docking/alignment **geometry** limits, not the chemistry.

> Probe models were built with a light conformer budget (8 embeds) so all 18 targets were tractable; the geometry-realization metric is robust to this (full-recipe nAChR gives acceptor 63% vs the probe's 62%, esr1 57% vs 54%). The full-recipe recovery models for nAChR/esr1 live under each target's `seed_align/`.

## Verdict — the geometry is the limiting factor, library-wide

Across **18 targets / 47 feature-rows**: **mean chemistry ceiling 98% vs mean geometry realization 67%**; **0** rows are chemistry-deficient, **30 (64%)** are geometry-limited (chemistry present, realization < 70%). DrugCLIP retrieves compounds that carry the right functional groups almost universally; the pipeline's weakness is placing those groups consistently in 3D. The failure tracks feature type exactly:

| feature | mean geom realization | placed… |
|---|--:|---|
| aromatic | 72% (n=15) | **best** — rigid ring anchor |
| hydrophobe | 71% (n=12) | best — bulky, tolerant |
| anion | 72% (n=2) | good — usually a rigid aromatic acid |
| cation | 63% (n=3) | poor — **flexible** amine on varied linkers |
| donor | 62% (n=3) | poor — directional |
| acceptor | **58% (n=12)** | **worst** — directional; inherits the docking ring-flip |

So the geometry problem is specifically about **flexible groups (the cation) and directional groups (acceptor/donor)**: a single rigid whole-molecule superposition places the rigid aromatic core well but lets a peripheral flexible cation or a directional acceptor land off-consensus. This is the nAChR finding, generalised.

## Alternatives to fix the geometry

Ordered by expected payoff against the failure modes above:

1. **Directional (lone-pair / ring-normal) features** *(fixes the worst feature)*. Model acceptor/donor as a point **plus an orientation vector** (and aromatics as centroid + ring normal), and score orientation agreement, not just position. The acceptor's 58% is dominated by the pyridine-N/carbonyl pointing the wrong way (the docking ring-flip); an orientation term rejects the flipped placement instead of averaging it. This is the parked directionality work and is the highest-value single change.

2. **Post-alignment flexible/local refinement** *(fixes the flexible cation)*. After the rigid clique→Kabsch transform, run a short local optimisation that lets peripheral torsions relax to minimise feature-RMSD to the consensus (a pharmacophore-constrained fit, or RDKit `MMFF`+constraints / `O3A` polish). The core stays put; the flexible cation snaps onto the consensus instead of riding the rigid body fit.

3. **Iterative consensus re-alignment (EM-style)** *(reduces seed/order dependence)*. Currently each compound aligns to the model *as it grows*, so early compounds and the seed frame dominate. Add an outer loop: build the model, then re-align **every** compound to the converged consensus and rebuild, to a fixed point. This tightens all features and removes the order artefact, at a few× the cost.

4. **Better / independent seed docking** *(fixes the flip at its source)*. The directional error originates in the 5 seed poses (GNINA ring-flip, unmodelled bridging water). Your **AutoDockFR** seeds — especially flexible-receptor with the conserved water present — would give a correct bioactive frame that the acceptor consensus then inherits. Cheapest to try since it needs no new algorithm (just better seed SDFs).

5. **Quality-weighted contributions** *(dampens noise)*. Weight each compound's feature points by its alignment RMSD (already gated at 1.5 A) so marginal fits contribute less to the consensus centroid — a small, safe refinement that sharpens every feature.

6. **Scalability guard (already added)**: feature-rich ligands (HIV/CDK2, 12–17 features) blow up the exact clique search; a bounded greedy fallback above `alignment.max_clique_nodes` keeps them tractable. Necessary for the flexible-refinement/EM options to run library-wide.

**Recommendation:** (1) directional features + (4) better seeds attack the acceptor (the worst feature) from both ends; (2) local refinement attacks the flexible cation. Together they target the exact features this analysis shows are limiting.

| target | feature | chem | geom | n_carry/n_sup | limited by |
|---|---|--:|--:|---|---|
| esr1 | arom | 100% | 64% | 50/32 | geometry |
|  | acc | 100% | 54% | 50/27 | geometry |
|  | don | 98% | 76% | 49/37 | chemistry |
|  | hydph | 100% | 74% | 50/37 | chemistry |
| hiv1_protease | arom | 100% | 64% | 50/32 | geometry |
|  | hydph | 100% | 56% | 50/28 | geometry |
| cdk2 | arom | 100% | 56% | 50/28 | geometry |
| hmgcr | arom | 100% | 88% | 50/44 | chemistry |
|  | acc | 100% | 64% | 50/32 | geometry |
|  | don | 100% | 58% | 50/29 | geometry |
|  | anion | 96% | 77% | 48/37 | chemistry |
| nachr_a4b2_negative | arom | 100% | 54% | 50/27 | geometry |
|  | acc | 100% | 58% | 50/29 | geometry |
|  | hydph | 100% | 50% | 50/25 | geometry |
| ca2 | acc | 100% | 40% | 50/20 | geometry |
| ache | arom | 100% | 84% | 50/42 | chemistry |
|  | acc | 100% | 56% | 50/28 | geometry |
|  | hydph | 98% | 84% | 49/41 | chemistry |
| adrb2 | cation | 100% | 78% | 50/39 | chemistry |
|  | arom | 100% | 100% | 50/50 | chemistry |
|  | acc | 100% | 58% | 50/29 | geometry |
|  | don | 98% | 53% | 49/26 | geometry |
|  | hydph | 100% | 98% | 50/49 | chemistry |
| cox2 | arom | 100% | 80% | 50/40 | chemistry |
|  | acc | 90% | 69% | 45/31 | geometry |
|  | hydph | 100% | 72% | 50/36 | chemistry |
|  | anion | 96% | 67% | 48/32 | geometry |
| adora2a | arom | 100% | 80% | 50/40 | chemistry |
|  | acc | 100% | 54% | 50/27 | geometry |
|  | hydph | 88% | 73% | 44/32 | chemistry |
| nachr_a4b2_positive | cation | 94% | 57% | 47/27 | geometry |
|  | arom | 100% | 82% | 50/41 | chemistry |
|  | acc | 80% | 62% | 40/25 | geometry |
| chrm2 | arom | 100% | 54% | 50/27 | geometry |
|  | hydph | 98% | 55% | 49/27 | geometry |
| gaba_a_gaba | cation | 94% | 53% | 47/25 | geometry |
| gr_nr3c1 | arom | 100% | 86% | 50/43 | chemistry |
|  | hydph | 100% | 78% | 50/39 | chemistry |
| nav1_7_pore | arom | 100% | 58% | 50/29 | geometry |
|  | acc | 100% | 50% | 50/25 | geometry |
|  | hydph | 100% | 82% | 50/41 | chemistry |
| nav1_7_vsd4 | arom | 100% | 58% | 50/29 | geometry |
|  | acc | 100% | 58% | 50/29 | geometry |
|  | hydph | 100% | 60% | 50/30 | geometry |
| drd1 | arom | 100% | 66% | 50/33 | geometry |
|  | acc | 98% | 69% | 49/34 | geometry |
|  | hydph | 90% | 69% | 45/31 | geometry |

## Pattern

- Feature/target rows scored: **47** (chemistry-limited 17, geometry-limited 30, both 0).
- Of the **47** rows where the chemistry is present (ceiling >= 60%), **30** (64%) are geometry-limited (realization < 70%) — the chemistry is there but the alignment places it inconsistently.
- Mean chemistry ceiling 98% vs mean geometry realization 67%.