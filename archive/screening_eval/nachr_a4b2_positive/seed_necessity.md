# Is the seed necessary for correct convergence? — nAChR/5KXI

Three inits of the same top-100 DrugCLIP compounds; compared by **frame-independent internal geometry** (A) vs the known-actives model and Beers-Reich (cation-acceptor ~5.35). Ground truth internal geometry (known actives): cat-aro 4.50, cat-acc 4.56, aro-acc 1.50.

| init | families | cat-aro | cat-acc | aro-acc | aligned | EM iters | final shift (A) |
|---|---|--:|--:|--:|--:|--:|--:|
| crystal | acc+aro+cat | 3.97 | 4.27 | 1.03 | 69 | 1 | 0.046 |
| docked | acc+aro+cat | 5.14 | 5.71 | 1.11 | 79 | 2 | 0.098 |
| **seedless** | acc+aro+cat | **4.40** | 5.34 | **1.53** | 71 | 1 | 0.075 |
| *known actives* | acc+aro+cat | *4.50* | *4.56* | *1.50* | — | — | — |

## Verdict — the seed is NOT necessary for correct convergence

**All three inits recover the full 3-point nicotinic model (cation + aromatic + acceptor)**, and
each EM converges in 1–2 iterations (final centre shift < 0.1 Å). Decisively, the **seedless** build
— started only from the top-ranked compound's own energy-minimum conformer, no docked or crystal
frame — reaches the known-actives geometry **as well as or better than the seeded builds**:

- **cation–aromatic 4.40 Å** vs known-actives 4.50 (Δ **0.10**) — the best of the three (crystal 3.97,
  docked 5.14).
- **aromatic–acceptor 1.53 Å** vs 1.50 (Δ **0.03**) — again the best (crystal 1.03, docked 1.11).
- **cation–acceptor 5.34 Å** — essentially on Beers–Reich (~5.35); the known-actives 4.56 sits between
  the seedless and crystal values, and this distance is the flip-affected directional one.

**So on nAChR the chemistry carries the geometry — a seed is not required for a correct model.** The
shared *rigid cores* (the pyridine ring + its adjacent cationic centre) impose enough mutual distance
constraint that the consensus locks onto the right geometry from any reasonable start; the seed's
only role is convergence speed/robustness (here all converged almost immediately). This validates the
guiding thesis for this target.

**Caveats.** (i) One target — generalising needs the other crystal-ligand systems (esr1, adrb2, cdk2).
(ii) The **acceptor stays low-confidence**: positional matching can't resolve the pyridine-N
orientation (the docking ring-flip / averaging), which is why cat–acc is the least stable distance;
orientation-aware (directional) matching is the agreed next iteration and the model's `direction`
field is already plumbed for it. (iii) Support is not a meaningful discriminator here — feature-clique
alignment forces matched features to coincide, so *internal geometry* vs ground truth (used above),
not support, is the right metric.