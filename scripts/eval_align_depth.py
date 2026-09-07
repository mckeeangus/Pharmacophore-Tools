#!/usr/bin/env python
"""Find the most effective seed-alignment depth against the known-actives models.

Builds the seed-alignment model at several `top_hits` depths for a few targets that have a
built known-actives pharmacophore, scores each by feature-family recall + internal-geometry
agreement with that known-actives model, and prints a table + the recommended depth. Writes
models to a scratch dir (not the catalogue). Run: pixi run python scripts/eval_align_depth.py.
"""

from __future__ import annotations

import json
import os
import sys
import tempfile
from pathlib import Path

os.environ.setdefault("OMP_NUM_THREADS", "1")
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from rdkit import RDLogger  # noqa: E402

RDLogger.DisableLog("rdApp.*")

from pharmpipe.pharmacophore.config import load_pharmacophore_config  # noqa: E402
from pharmpipe.pharmacophore.run import build_from_seed_alignment  # noqa: E402
from pharmpipe.screening.compare import compare_models, summarise  # noqa: E402
from pharmpipe.screening.crosswalk import SCREENING_DIR, load_crosswalk  # noqa: E402
from pharmpipe.util.paths import CATALOGUE_DIR  # noqa: E402

DEPTHS = [int(x) for x in os.environ.get("DEPTHS", "30,50,100,200").split(",")]
# targets with a built known-actives model, spanning chemotypes (cation, steroid, ATP-site)
EVAL_KEYS = os.environ.get("EVAL_KEYS",
                           "nachr_a4b2_positive,esr1,cdk2,adrb2,hmgcr").split(",")


def _ka_features(slug: str, cell: str) -> list[dict] | None:
    p = CATALOGUE_DIR / slug / "pharmacophores" / cell / "pharmacophore.json"
    return json.loads(p.read_text())["features"] if p.exists() else None


def main() -> int:
    cfg = load_pharmacophore_config()
    _, targets = load_crosswalk()
    by_key = {t.key: t for t in targets}
    print(f"{'target':<22} {'depth':>5} {'align':>6} {'recall':>6} {'geomD':>6} {'verdict':>8}")
    print("-" * 60)
    scores: dict[int, list[float]] = {d: [] for d in DEPTHS}
    with tempfile.TemporaryDirectory() as tmp:
        for key in EVAL_KEYS:
            t = by_key.get(key)
            if t is None or not t.cell:
                continue
            ka = _ka_features(t.slug, t.cell)
            if ka is None:
                continue
            ka_sum = summarise(ka)
            for d in DEPTHS:
                out = Path(tmp) / f"{key}_{d}"
                res = build_from_seed_alignment(
                    SCREENING_DIR / key, SCREENING_DIR / key / f"index_{key}.csv", out, cfg,
                    top_n_hits=d, seed_k=cfg.alignment.seed_k, name=f"{key}_{d}")
                if res is None:
                    print(f"{key:<22} {d:>5}  (skipped)")
                    continue
                a = summarise([f for f in
                               json.loads((out / 'pharmacophore.json').read_text())['features']])
                cmp = compare_models(a, ka_sum)
                n_lig = res.pharmacophore.metadata["source"]["n_ligands"]
                gd = f"{cmp.mean_geom_delta:.2f}" if cmp.mean_geom_delta is not None else "-"
                print(f"{key:<22} {d:>5} {n_lig:>6} {cmp.family_recall:>6.2f} {gd:>6} "
                      f"{cmp.verdict:>8}")
                # score = family recall minus a geometry penalty (0.1/A over shared pairs)
                pen = (cmp.mean_geom_delta or 0.0) * 0.1
                scores[d].append(cmp.family_recall - pen)
    print("\nMean score by depth (family recall - 0.1 * geomD):")
    ranked = sorted(((sum(v) / len(v) if v else 0.0, d) for d, v in scores.items()), reverse=True)
    for s, d in ranked:
        print(f"  depth {d:>4}: {s:.3f}")
    print(f"\nRecommended alignment_depth = {ranked[0][1]} "
          f"(set config/screening.yaml alignment_depth)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
