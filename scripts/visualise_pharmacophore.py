#!/usr/bin/env python
"""Tool 3 — pharmacophore visualisation. See README.md.

    pixi run visualise-pharmacophore --pharmacophore pharmacophore.csv --out DIR \\
        [--compounds aligned_compounds.sdf] [--features features.csv]
"""

from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from pharmpipe.pharmacophore.io import read_model_csv, write_json  # noqa: E402

REPO = Path(__file__).resolve().parents[1]


def _auto_compounds(pharmacophore_csv: Path) -> Path | None:
    """The aligned molecules this model was built from (SDF or mol2 dir), from the sibling
    ``pharmacophore_model.json``'s ``metadata.source`` — or ``None`` if not found."""
    json_path = pharmacophore_csv.with_name("pharmacophore_model.json")
    if not json_path.exists():
        return None
    try:
        source = json.loads(json_path.read_text(encoding="utf-8")).get("metadata", {}).get(
            "source", {})
    except (OSError, ValueError):
        return None
    for key in ("input", "input_dir"):
        p = source.get(key)
        if p and Path(p).exists():
            return Path(p)
    return None


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--pharmacophore", type=Path, required=True,
                    help="a pharmacophore CSV (from build-pharmacophore)")
    ap.add_argument("--out", type=Path, required=True, help="output directory")
    ap.add_argument("--compounds", type=Path, default=None,
                    help="aligned molecules to overlay (default: auto-detected from the model)")
    ap.add_argument("--features", type=Path, default=None,
                    help="optional features.csv (raw points) — enables the support sweep")
    args = ap.parse_args(argv)

    out = args.out.resolve()
    out.mkdir(parents=True, exist_ok=True)
    pharmacophore_csv = args.pharmacophore.resolve()
    compounds = args.compounds.resolve() if args.compounds else _auto_compounds(pharmacophore_csv)
    # The PyMOL renderer reads the canonical JSON; materialise it from the CSV.
    model = read_model_csv(pharmacophore_csv)
    tmp_json = out / "_model.json"
    write_json(model, tmp_json)

    pixi = shutil.which("pixi")
    if pixi is None:
        print("ERROR: pixi not found on PATH (needed to reach the viz env for PyMOL).",
              file=sys.stderr)
        return 1
    script = REPO / "scripts" / "pymol_pharmacophore.py"
    cmd = [pixi, "run", "-e", "viz", "pymol", "-cq", str(script), "--",
           "--pharmacophore", str(tmp_json),
           "--out", str(out / "pharmacophore.pse"),
           "--image", str(out / "pharmacophore.png"),
           "--sweep-out", str(out / "pharmacophore_sweep.pse"),
           "--sweep-image", str(out / "pharmacophore_sweep.png")]
    if args.features:
        cmd += ["--features", str(args.features.resolve())]
    if compounds:
        cmd += ["--compounds", str(compounds)]
    os.environ.setdefault("PYTHONIOENCODING", "utf-8")
    result = subprocess.run(cmd, cwd=REPO, check=False)
    tmp_json.unlink(missing_ok=True)
    if result.returncode != 0:
        print(f"visualise-pharmacophore: PyMOL render failed (exit {result.returncode})",
              file=sys.stderr)
        return result.returncode
    print(f"visualised -> {out} (pharmacophore.pse/.png, pharmacophore_sweep.pse)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
