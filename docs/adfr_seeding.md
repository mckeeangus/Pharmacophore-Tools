# Producing seed poses for `--seed-docked` (AutoDockFR / any docking engine)

The minimum-docking pharmacophore build (`pixi run build-pharmacophores --seed-docked`) needs a
small **bioactive frame**: the top-`seed_k` (default 5) DrugCLIP-ranked ligands docked into the
pocket. The build is **engine-agnostic** — it consumes docked poses as SDF and never runs a docking
engine itself (per the project scope). GNINA poses from the screening deposit are the current
stand-in; this note describes producing the seeds with **AutoDockFR (ADFRsuite)**, which is not
installable in the local pixi environment (Linux/macOS toolchain, clean receptors + boxes live on
Gadi), so run it on a login/data-mover node and drop the results in.

## Seed-pose input contract

`--seed-docked DIR` expects, inside `DIR`:

- **`index_<key>.csv`** — the DrugCLIP rank index, pipeline format
  (`entity_id,mol_id,library_name,smiles,drugclip_score,vina_docking_score`, header, ranked rows).
  All 100 compounds live here; ranks + SMILES for the 95 non-seed compounds come from it.
- **`<mol_id>_docked.sdf`** for at least the top-`seed_k` ranked `mol_id`s — the docked seed poses.
  One compound per file; if a file holds several poses, the loader takes pose 1 unless a recognised
  GNINA score tag (`CNNaffinity` etc.) is present to rank them. **Only the seeds need SDFs** — the
  remaining ranked compounds are embedded from their index SMILES, so you dock 5, not 100.

The 3D frame of these SDFs *is* the bioactive frame the whole model is built in, so dock into the
same receptor/box you want the pharmacophore expressed in (e.g. the crystal pocket).

## AutoDockFR procedure (Gadi login node)

Prerequisites: ADFRsuite on `PATH` (`prepare_receptor`, `agfr`, `prepare_ligand`, `adfr`); the
**clean receptor PDB** (protein only, no ligand/waters unless intended) and a **reference ligand
SDF** marking the pocket (both already on Gadi under `/g/data/<proj>/…/PDB_CLEAN/` and `…/HET/`).

```bash
# 1. Receptor -> PDBQT (once per target)
prepare_receptor -r 5KXI_clean.pdb -o 5KXI.pdbqt

# 2. Pocket target file (.trg): autobox around the reference ligand (+4 A padding)
agfr -r 5KXI.pdbqt -l 5KXI_reference.pdb -o 5KXI            # -> 5KXI.trg
#    (or -b user cx cy cz sx sy sz for an explicit box; add -f <resids> for flexible sidechains)

# 3. Per seed ligand (top-5 by DrugCLIP): protonated SMILES -> 3D PDBQT -> dock
for mid in $(head -6 index_key.csv | tail -5 | cut -d, -f2); do          # top-5 mol_ids
    smi=$(grep ",$mid," index_key.csv | cut -d, -f4)
    obabel -:"$smi" -O ${mid}.sdf --gen3d -p 7.4                          # 3D, pH 7.4
    prepare_ligand -l ${mid}.sdf -o ${mid}.pdbqt
    adfr -t 5KXI.trg -l ${mid}.pdbqt --jobName ${mid} -O                  # -> ${mid}_adfr_out/
    # 4. Convert the best ADFR pose to the expected filename
    obabel ${mid}_adfr_out/${mid}_ranked_1.pdbqt -O ${mid}_docked.sdf
done
```

Place the resulting `<mol_id>_docked.sdf` files and `index_<key>.csv` in one directory and run:

```bash
pixi run build-pharmacophores --seed-docked DIR --out MODELDIR --top-hits 100 --seed-k 5
```

## Notes

- **ADFR poses carry no GNINA score tags**; the loader falls back to pose 1 of each SDF, which is
  ADFR's top-ranked pose — the intended behaviour. If you export multiple ranked poses per file,
  keep ADFR's rank order.
- **Flexible-receptor (the "FR")**: pass `-f <resid,resid,…>` to `agfr` to let named sidechains move
  during docking; useful where induced fit or a conserved water matters (e.g. the nicotinic cation
  cage). The pharmacophore build is unaffected — only the seed geometry changes.
- **Determinism**: ADFR is a genetic-algorithm docker; fix its seed (`--seed`) for reproducible
  seeds. The alignment build itself is deterministic given fixed seed poses.
