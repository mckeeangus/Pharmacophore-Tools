# Example — nicotinic acetylcholine receptor (nAChR)

A small, self-contained input so you can run the three tools immediately.

- **`nachr_hits.csv`** — 25 top-ranked nAChR hits in DrugCLIP output form
  (`mol_id,smiles,drugclip_score`). Input for `align-molecules`.
- **`nachr_seed.sdf`** — a co-crystal-style nicotine ligand (one 3-D conformer), to demonstrate
  the optional `--seed` (bootstrap) mode.

## Run the full chain

```bash
pixi run align-molecules       --input examples/nachr_hits.csv --out out/align
pixi run build-pharmacophore   --input out/align/aligned_compounds.sdf --out out/model
pixi run visualise-pharmacophore --pharmacophore out/model/pharmacophore.csv --out out/viz \
    --compounds out/align/aligned_compounds.sdf --features out/model/features.csv
```

You should get the classic nicotinic 3-point model — a **positive-ionisable** (cationic amine),
an **aromatic**, and an H-bond **acceptor** — in `out/model/pharmacophore.csv`.

## With a holo seed

```bash
pixi run align-molecules --input examples/nachr_hits.csv --seed examples/nachr_seed.sdf --out out/align_seeded
```

The seed anchors the alignment frame (and, if it were in a protein's coordinates, would place the
pharmacophore in that binding site), then is dropped before the EM refinement.

> **Note:** this is a *deliberately small* illustrative set (25 molecules, and the top DrugCLIP
> hits for nAChR are chemically diverse), so only a handful pass the alignment quality gate and you
> will see a "consensus is weak / provisional" warning — expected here. Real runs use larger hit
> lists (the `--top-n` default is 50), where many more compounds align.
