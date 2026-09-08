#!/usr/bin/env python
"""How does the seedless alignment method compare to the crystal + literature pharmacophores?

For each target with a known-actives (crystal-derived) model, score the **seedless** feature-
alignment model against two references: (a) the known-actives model — feature-family recall +
frame-independent internal geometry (`compare_models`); (b) the literature model — family
composition (`compare_to_literature`). Reuses the seedless models built for the seed-necessity
generalisation (light conformer budget; directional matching is a modest refinement that does not
change family-level recovery, so the comparison holds). Read-only + fast — no rebuilds.

Run: pixi run python scripts/alignment_vs_reference.py.
Writes catalogue/screening_eval/alignment_vs_reference.md.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))

from pharmpipe.screening.compare import (  # noqa: E402
    compare_models,
    compare_to_literature,
    summarise,
)
from pharmpipe.screening.crosswalk import load_crosswalk  # noqa: E402
from pharmpipe.screening.literature import load_literature  # noqa: E402
from pharmpipe.util.paths import CATALOGUE_DIR, REPO_ROOT  # noqa: E402

SEEDLESS = REPO_ROOT / "data" / "_geom_probe" / "seednec"
EVAL = CATALOGUE_DIR / "screening_eval"
SHORT = {"PosIonizable": "cat", "NegIonizable": "an", "Aromatic": "aro", "Acceptor": "acc",
         "Donor": "don", "LumpedHydrophobe": "hyd"}


def _fams(summary) -> str:
    return "+".join(sorted(SHORT.get(f, f) for f in summary.dominant))


def main() -> int:
    _, targets = load_crosswalk()
    lit = load_literature()
    lines = ["# Seedless alignment vs the crystal (known-actives) and literature pharmacophores",
             "",
             "Per target: the **seedless** feature-alignment model scored against the "
             "**known-actives** model (crystal-derived — family recall + frame-independent "
             "internal geometry, mean pairwise-distance delta in A) and the **literature** model "
             "(family composition). MATCH/PARTIAL/MISMATCH per `screening.compare`.", "",
             "| target | model families | vs crystal | recall | geomD | vs literature | recall | "
             "missing (lit) |", "|---|---|:--:|--:|--:|:--:|--:|---|"]
    rows = []
    for t in targets:
        model = SEEDLESS / t.key / "seedless" / "pharmacophore.json"
        cell_json = (CATALOGUE_DIR / t.slug / "pharmacophores" / (t.cell or "") /
                     "pharmacophore.json")
        if not model.exists() or t.cell is None or not cell_json.exists():
            continue
        a = summarise(json.loads(model.read_text())["features"])
        ka = compare_models(a, summarise(json.loads(cell_json.read_text())["features"]))
        lit_cell = "-"
        lrecall = "-"
        lmissing = ""
        if t.literature and t.literature in lit:
            lc = compare_to_literature(a, lit[t.literature].families)
            lit_cell, lrecall = lc.verdict, f"{lc.recall:.2f}"
            lmissing = ", ".join(SHORT.get(m, m) for m in lc.missing)
        gd = f"{ka.mean_geom_delta:.2f}" if ka.mean_geom_delta is not None else "-"
        lines.append(f"| {t.key} | {_fams(a)} | {ka.verdict} | {ka.family_recall:.2f} | {gd} | "
                     f"{lit_cell} | {lrecall} | {lmissing} |")
        rows.append((t.key, ka, lit_cell))

    n = len(rows)
    ka_match = sum(1 for _, k, _ in rows if k.verdict in ("MATCH", "PARTIAL"))
    ka_full = sum(1 for _, k, _ in rows if k.verdict == "MATCH")
    lit_ok = sum(1 for _, _, lv in rows if lv in ("MATCH", "PARTIAL"))
    lit_scored = sum(1 for _, _, lv in rows if lv != "-")
    lines += ["", "## Verdict", "",
              f"- Targets compared: **{n}** (those with a known-actives model + a seedless model).",
              f"- **vs crystal (known-actives):** {ka_full} MATCH, {ka_match - ka_full} PARTIAL, "
              f"{n - ka_match} MISMATCH — the alignment recovers the crystal-derived families in "
              f"{ka_match}/{n} targets.",
              f"- **vs literature:** {lit_ok}/{lit_scored} MATCH-or-PARTIAL on family composition.",
              "- Directionality is a modest refinement over these (family-level recovery is "
              "unchanged); the geometry deltas are inflated where a feature is directional (the "
              "acceptor). The crystal comparison is the stricter test (it scores geometry, not "
              "just families); literature agreement is family-level (most papers report features, "
              "not full geometries)."]
    (EVAL / "alignment_vs_reference.md").write_text("\n".join(lines), encoding="utf-8")
    print("\n".join(lines))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
