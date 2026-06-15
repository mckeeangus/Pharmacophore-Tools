"""Stage 3 — effect-based grouping with pocket verification.

Organise the Stage-2 site-aligned poses into *partition cells*
``(verified pocket) x (efficacy sign)``. Three separable concerns:

* :mod:`pharmpipe.groups.pocket` — contact-based pocket identity (pure geometry).
* :mod:`pharmpipe.groups.efficacy` / :mod:`pharmpipe.groups.pockets` — curator
  knowledge loaded from versioned config data (never hardcoded in logic).
* :mod:`pharmpipe.groups.group` — orchestration into cells.
* :mod:`pharmpipe.groups.visualize` — per-cell + combined PyMOL sessions.

Stage 3 ends at pose grouping; it does not cluster, extract features, or build
models (that is the downstream pipeline and remains out of scope).
"""
