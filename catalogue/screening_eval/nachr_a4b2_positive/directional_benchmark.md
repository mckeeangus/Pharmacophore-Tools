# Directional matching A/B — nAChR/5KXI (docked seed, crystal frame)

Absolute distance (A) of each consensus feature to the crystal nicotine atom it should sit on, with orientation-aware matching OFF vs ON. The acceptor is the directional feature the ring-flip corrupts; cation/aromatic are pose-invariant controls.

| feature | dist OFF | dist ON | support OFF | support ON | direction set (ON) |
|---|--:|--:|--:|--:|:--:|
| cation | 1.68 | 1.38 | 0.58 | 0.60 | no |
| aromatic | 0.87 | 0.77 | 0.89 | 0.96 | yes |
| acceptor | 1.54 | 1.41 | 0.60 | 0.63 | yes |

## Verdict

- **Acceptor off-native: 1.54 A → 1.41 A** with directional matching, and its **orientation is now
  populated** (`direction` set). The improvement is real but modest, and comparable to the small
  shifts in the cation/aromatic controls (which move because directional matching changes which
  conformer/clique wins per compound, nudging the whole consensus) — so it is at the edge of
  run-to-run noise on this target.
- **Why modest here:** on nAChR the seed-align + EM method *already* places the acceptor well
  (~1.5 A), so this target does not stress-test the ring-flip. The flip was most damaging in the
  *full-docking consensus* method (`--docked-dir`, acceptor ~3.5 A off); the incremental
  align + EM consensus is far less flip-prone, leaving directionality little to fix here.
- **The concrete deliverable** is that directional matching is implemented (projected-point Kabsch
  for donor/acceptor) and the model's `direction` field is populated — orientation is now part of
  both the alignment objective and the output model. Its quantitative payoff is target-dependent;
  a flip-stressed target (or the full-docking path) is where it should matter most, and is the
  right place to benchmark it next.