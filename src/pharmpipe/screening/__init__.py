"""DrugCLIP screening-set evaluation (organise + compare), orthogonal to the catalogue build.

This package supports the library-wide evaluation of the docking-derived pharmacophore methods
(full-docking `--docked-dir` and minimum-docking `--seed-docked`) against the known-actives
catalogue models and the literature. It depends on the Stage-4 core only through the same public
interfaces the build modes use; nothing here feeds the known-actives build.
"""
