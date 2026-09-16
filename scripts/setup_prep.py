#!/usr/bin/env python
"""Provision the isolated ``prep`` env (pkasolver) so ``--pkasolver`` works out of the box.

Clones the vendored pkasolver checkout (``external/pkasolver``, gitignored — see its bundled
model weights) if missing, then installs the ``prep`` pixi environment.

    pixi run setup-prep
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
PKASOLVER = REPO / "external" / "pkasolver"
PKASOLVER_URL = "https://github.com/mayrf/pkasolver"


def main() -> int:
    if not PKASOLVER.exists():
        print(f"cloning {PKASOLVER_URL} -> {PKASOLVER}")
        subprocess.run(["git", "clone", "--depth", "1", PKASOLVER_URL, str(PKASOLVER)],
                       cwd=REPO, check=True)
    else:
        print(f"{PKASOLVER} already present")
    subprocess.run(["pixi", "install", "-e", "prep"], cwd=REPO, check=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
