# Screening-derived pharmacophores vs known-actives + literature — analysis

Companion narrative to the auto-generated `comparison_report.md` (per-target verdict matrix)
and `results.json` (full data). Covers all **18** DrugCLIP→GNINA screening sets, each built two
ways — **docked** (density consensus over all ~1000 docked poses) and **seed_align**
(minimum-docking: seed from 3 docked poses, align the top-50 DrugCLIP hits by features, depth
chosen in `config/screening.yaml`). Comparison is frame-independent (feature-family recall +
internal geometry), since each docked model sits in its own PDB crystal frame while the
known-actives models are in the Stage-2 aligned frame.

## Two headline findings

**1. Consensus over the *whole* docked library fails — dilution.** Full-docking over all 1000
poses collapses to **0 features for 8/18 targets** and ≤2 for 14/18 (median 1); only **esr1**
reaches MATCH. The deep hits DrugCLIP returns are chemically heterogeneous, so their features
scatter and nothing clears the 0.5 support floor. "Use all the docked poses" is therefore the
*wrong* way to consume a screen. The two exceptions (esr1 4-feat; nav1_7_vsd4 5-feat) are
exactly the **chemically homogeneous** hit sets (phenols; aryl-sulfonamides), which confirms the
mechanism.

**2. Minimum-docking seed-alignment is the robust method.** It recovers a real pharmacophore for
**16/18** targets (median ~5 features) and agrees with the known-actives model far better —
**2 MATCH / 7 PARTIAL / 2 MISMATCH** (vs full-docking's 1/2/8). It is also ~30× cheaper (3
docked seeds, not 1000). **Recommendation: seed-alignment is the default for screening-derived
construction; full-docking should be run on a top slice (~30–50), not the whole library.**

| Metric | Full-docking | Seed-align (depth 50) |
|---|---|---|
| vs known-actives (MATCH/PARTIAL/MISMATCH) | 1 / 2 / 8 | **2 / 7 / 2** |
| vs literature | 1 / 1 / 12 | **2 / 8 / 4** |
| features per model (median) | 1 | ~5 |
| zero-feature failures | **8 / 18** | 1 / 18 |

## Per-target diagnosis (seed-align, unless noted)

**Full agreement (MATCH):**
- **esr1** — both methods MATCH known-actives *and* literature (Anstead: aromatic + phenol
  donor/acceptor + hydrophobe). Homogeneous phenolic hits; the ideal case.
- **nachr_a4b2_positive** — seed MATCH (cation + aromatic + acceptor; the classic nicotinic
  3-point). Full-docking diluted to 1. (The acceptor is present but, per the earlier deep-dive,
  sits at the ring-flipped orientation — a known docking artefact, not a family miss.)

**Close (PARTIAL) — right families, geometry or one feature off:**
- **adrb2** — aromatic(1.0)+hydrophobe(1.0)+catechol donor/acceptor recovered, but the defining
  **protonated amine (PosIonizable) is missing** → likely a *protonation/perception* gap (the
  β-amine read as Donor, not cation). *Fix: verify the pH-7.4 microstate carries the amine
  charge; anchor the seed on the cation.*
- **drd1, adora2a, ache** — aminergic/aromatic cores recovered; PARTIAL because an accessory
  H-bond or the exact geometry differs from the diverse experimental actives (compound-set
  difference, not method failure).
- **hiv1_protease** — acceptor+aromatic+hydrophobe recovered; misses the **bridging-water**
  H-bond network the crystal actives exploit (the pipeline models no waters).
- **hmgcr** — richest seed model (8 features incl. anion + acceptors); PARTIAL because the
  statin di-hydroxy-acid H-bonds are only partly consolidated.
- **gr_nr3c1** — aromatic+hydrophobe steroid body recovered; misses the steroid **H-bond
  acceptors** (3-keto / 11β,17-OH). Rigid steroids, few conformers — *fix: steroid-aware seed*.
- **nav1_7 (pore, vsd4)** — aryl-sulfonamide features recovered; PARTIAL vs the Wang model
  (acidic sulfonamide as NegIonizable not always perceived).

**Mismatch — a genuine method gap:**
- **cdk2** — recovered only aromatic+hydrophobe; **missing the hinge Donor+Acceptor pair** that
  *defines* the ATP site. The hinge H-bond is directional and presented differently across
  diverse inhibitors, so feature alignment on the flat aromatic core doesn't pin it. *Fix:
  directional H-bond features (the parked directionality work) and/or hinge-anchored seeding.*
- **ca2** — only an acceptor, and only **37/50 compounds aligned** (low clique coverage). The
  defining feature is the **Zn²⁺-coordinating sulfonamide**, which the pipeline has *no feature
  family for*. *Fix: add a metal-binding feature.*
- **gaba_a_bzd** — **0 features from both methods** despite 50 aligned ligands: the
  benzodiazepine-site hits do not consolidate to any consensus (interface pocket, heterogeneous
  binding modes, inconsistent seed poses). *Fix: larger seed_k + per-site conformer/clique
  tuning; this site needs manual review.*

## Prioritised method improvements

1. **Never consensus the whole docked library** (biggest, most general): the density-consensus
   method must run on a **top slice (~30–50 by DrugCLIP)**, matching seed-align's depth. Trivial
   change (cap `--top-hits`); turns 8 zero-feature failures into usable models.
2. **Make seed-alignment the default** screening builder — it is both more accurate and far
   cheaper.
3. **Directional H-bond features** (the parked lone-pair/vector work): would fix cdk2's hinge and
   nachr's acceptor flip — the two clearest directional failures.
4. **A metal-binding feature family**: required for ca2 and any metalloenzyme; currently
   un-modellable.
5. **Verify ligand protonation** end-to-end: adrb2's missing cation points at a microstate/
   perception gap that likely affects other basic-amine targets.
6. **Coverage for hard sets**: raise `seed_k` / relax `min_clique` / enlarge conformer ensembles
   for low-alignment targets (ca2 37/50; gaba_bzd 0-consensus).
7. **Homogeneity gate**: full-docking *does* work on homogeneous hit sets (esr1, nav1_7_vsd4); a
   scaffold-clustering pre-filter could recover it where wanted, or flag heterogeneous screens.

## Caveats

- **Literature comparison is family-level** (most cited models give features + a few distances,
  not full geometries); treat `vsLit` as composition agreement, not a geometric fit.
- **Seed-alignment has mild run-to-run variance** (conformer embedding / clique tie-breaks): a
  re-run shifted nachr aligned-ligand count 43↔80 and feature count 2↔3. Worth making fully
  deterministic before publication.
- **Known-actives models exist for only 11 targets**; cox2/chrm2/gaba/nav1_7/nachr-negative are
  literature-only. `net_slc6a2` had no docked poses deposited (excluded).
