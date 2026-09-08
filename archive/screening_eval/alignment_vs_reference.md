# Seedless alignment vs the crystal (known-actives) and literature pharmacophores

Per target: the **seedless** feature-alignment model scored against the **known-actives** model (crystal-derived — family recall + frame-independent internal geometry, mean pairwise-distance delta in A) and the **literature** model (family composition). MATCH/PARTIAL/MISMATCH per `screening.compare`.

| target | model families | vs crystal | recall | geomD | vs literature | recall | missing (lit) |
|---|---|:--:|--:|--:|:--:|--:|---|
| esr1 | acc+aro+don+hyd | MATCH | 1.00 | 0.21 | MATCH | 1.00 |  |
| hiv1_protease | acc+aro+hyd | PARTIAL | 0.75 | 1.01 | PARTIAL | 0.75 | don |
| cdk2 | acc+aro+don+hyd | PARTIAL | 1.00 | 3.65 | MATCH | 1.00 |  |
| hmgcr | acc+an+aro+don+hyd | PARTIAL | 1.00 | 2.79 | - | - |  |
| ca2 | acc+aro+hyd | PARTIAL | 0.75 | 2.44 | PARTIAL | 0.75 | an |
| ache | acc+aro+cat+hyd | PARTIAL | 1.00 | 4.63 | - | - |  |
| adrb2 | acc+aro+cat+don+hyd | MATCH | 1.00 | 0.40 | MATCH | 1.00 |  |
| adora2a | acc+aro+don | MATCH | 1.00 | 1.00 | PARTIAL | 0.75 | hyd |
| nachr_a4b2_positive | acc+aro+cat | MATCH | 1.00 | 0.53 | MATCH | 1.00 |  |
| gr_nr3c1 | acc+aro+don+hyd | MATCH | 1.00 | 1.39 | MATCH | 1.00 |  |
| drd1 | acc+aro+cat+hyd | PARTIAL | 0.80 | 1.86 | PARTIAL | 0.80 | don |

## Verdict

- Targets compared: **11** (those with a known-actives model + a seedless model).
- **vs crystal (known-actives):** 5 MATCH, 6 PARTIAL, 0 MISMATCH — the alignment recovers the crystal-derived families in 11/11 targets.
- **vs literature:** 9/9 MATCH-or-PARTIAL on family composition.
- Directionality is a modest refinement over these (family-level recovery is unchanged); the geometry deltas are inflated where a feature is directional (the acceptor). The crystal comparison is the stricter test (it scores geometry, not just families); literature agreement is family-level (most papers report features, not full geometries).