"""Build one pharmacophore model from a directory of aligned compounds (Stage 4).

This is the orchestration edge: it wires the pure pieces (load -> featurize ->
cluster -> assemble) and writes the model artifacts. The general entry point is
``build_from_directory``; ``build_for_cell`` adds the catalogue convention
(SMILES sourced from the target's unique_ligands.csv).
"""

from __future__ import annotations

import logging
from dataclasses import asdict, dataclass, field
from datetime import date
from pathlib import Path

import numpy as np

from ..features.extract import FeatureResolution, build_table, feature_factory
from ..features.load import (
    LoadReport,
    load_directory,
    read_protonation_map,
    read_smiles_map,
)
from ..io.structures import read_protein_atom_coords
from ..util.paths import ensure_dir
from .build import best_representative
from .config import PharmacophoreConfig
from .consensus import build_consensus
from .io import write_features_csv, write_json, write_pml, write_representative_sdf
from .model import Pharmacophore
from .viz import plot_raw_features

log = logging.getLogger("pharmpipe.pharmacophore.run")


@dataclass
class ModelOutputs:
    name: str
    model_dir: Path
    pharmacophore: Pharmacophore
    report: LoadReport
    files: list[Path] = field(default_factory=list)


def _aggregate_resolutions(resolutions: list[FeatureResolution]) -> dict:
    """Group co-atom hierarchy decisions by ``kept<-dropped`` for provenance/report.

    Returns ``{"PosIonizable<-Donor": {"events": n, "ligands": [ids...]}, ...}`` so the
    ligands that carried a dual classification are recorded (sorted, de-duplicated).
    """
    by_pair: dict[str, dict] = {}
    for r in resolutions:
        key = f"{r.kept_family}<-{r.dropped_family}"
        entry = by_pair.setdefault(key, {"events": 0, "ligands": set()})
        entry["events"] += 1
        entry["ligands"].add(r.ligand_id)
    return {k: {"events": v["events"], "ligands": sorted(v["ligands"])}
            for k, v in sorted(by_pair.items())}


def _feature_ordinal(feat) -> int:
    """The per-family index in a feature's label (``Donor 2`` -> 2); 0 if unlabelled."""
    try:
        return int(feat.label.rsplit(" ", 1)[1])
    except (ValueError, IndexError):
        return 0


def _unselected_features(result, n_ligands: int) -> list[tuple[str, int, int, float]]:
    """Clusters/peaks that were formed but did NOT enter the model, as
    ``(family, n_points, n_ligands, support)`` sorted by support then size.

    A cluster is "not selected" when its label is absent from the family's
    ``kept_labels`` — it fell below the support/size floor (§5/§11.4) or was displaced by
    the cross-family overlap merge. Support is recomputed here from the raw assignment.
    """
    rows: list[tuple[str, int, int, float]] = []
    for a in result.assignments:
        for lbl in sorted(set(a.labels.tolist())):
            if lbl in a.kept_labels:
                continue
            mask = a.labels == lbl
            n_points = int(mask.sum())
            n_lig = len({lig for lig, m in zip(a.ligand_ids, mask, strict=True) if m})
            support = n_lig / n_ligands if n_ligands else 0.0
            rows.append((a.family, n_points, n_lig, support))
    rows.sort(key=lambda r: (r[3], r[1]), reverse=True)
    return rows


def _write_summary(result, report: LoadReport, n_ligands: int,
                   path: Path) -> Path:
    ph: Pharmacophore = result.pharmacophore
    # Excluded-volume spheres are receptor steric markers, not ligand-derived
    # peaks: they carry no label and no support, so they are counted separately
    # and kept out of the per-feature support table (which is one row per peak).
    ligand_feats = [f for f in ph.features if f.family != "ExcludedVolume"]
    n_ev = len(ph.features) - len(ligand_feats)
    lines = [
        f"# Pharmacophore — {ph.name}", "",
        f"- Ligands loaded: **{n_ligands}** "
        f"({', '.join(f'{k}={v}' for k, v in sorted(report.by_method.items())) or 'none'})",
        f"- Skipped poses: {len(report.skipped)}"
        + (f" ({', '.join(f'{lid}:{why}' for lid, why in report.skipped)})"
           if report.skipped else ""),
        f"- Consensus method: `{ph.metadata.get('consensus_method', '?')}`",
        f"- Representative ligand (viz): `{ph.metadata.get('representative_ligand') or 'none'}`",
        f"- Features kept: **{len(ligand_feats)}**",
    ]
    if n_ev:
        lines.append(f"- Excluded-volume spheres (receptor markers): **{n_ev}**")
    lines += [
        "",
        "Support is the fraction of the cell's ligands that contribute to a feature "
        "(one row per feature / peak; all features are kept only above the support floor).",
        "",
        "| Feature | Points | Ligands | Support |", "|---|---:|---:|---:|",
    ]
    for f in sorted(ligand_feats, key=lambda f: (f.family, _feature_ordinal(f))):
        lines.append(
            f"| {f.label or f.family} | {f.n_points} | {f.n_ligands} | {f.support:.2f} |")
    resolution = ph.metadata.get("feature_resolution") or {}
    if resolution:
        lines += [
            "", "## Feature resolution",
            "", "Co-incident dual classifications collapsed by the feature hierarchy "
            "(higher-priority family kept on the shared atom); the listed ligands each "
            "carried both types on one atom.",
            "", "| Kept ← dropped | Events | Ligands |", "|---|---:|---|",
        ]
        for pair, info in resolution.items():
            kept, dropped = pair.split("<-", 1)
            ligs = ", ".join(info["ligands"])
            lines.append(f"| {kept} ← {dropped} | {info['events']} | {ligs} |")
    unselected = _unselected_features(result, n_ligands)
    if unselected:
        lines += [
            "", "## Not selected",
            "", "Clusters/peaks that formed but did not enter the model — below the "
            "support or size floor, or displaced by the cross-family overlap merge — with "
            "their mean support (fraction of the cell's ligands contributing).",
            "", "| Feature | Points | Ligands | Mean support |", "|---|---:|---:|---:|",
        ]
        for fam, npts, nlig, sup in unselected:
            lines.append(f"| {fam} | {npts} | {nlig} | {sup:.2f} |")
    lines += ["", "See `pharmacophore.json` (model), `features.csv` (raw points + "
              "cluster ids), and `raw_features_*.png` (per-family point distributions, "
              "each kept peak annotated with its label and support)."]
    path.write_text("\n".join(lines), encoding="utf-8")
    return path


def _ligand_atom_coords(molecules: list[tuple[str, object]]) -> np.ndarray:
    """All heavy-atom coordinates of the loaded poses (the ligand envelope)."""
    blocks = [m.GetConformer().GetPositions()
              for _, m in molecules if m is not None and m.GetNumConformers()]
    return np.vstack(blocks) if blocks else np.empty((0, 3), dtype=float)


def _scaffold_frequencies(molecules: list[tuple[str, object]]) -> dict[str, int]:
    """Map each ligand_id to how many loaded ligands share its Murcko scaffold."""
    from rdkit.Chem import MolToSmiles
    from rdkit.Chem.Scaffolds import MurckoScaffold

    scaffold_of: dict[str, str] = {}
    for lig, mol in molecules:
        if mol is None:
            continue
        try:
            scaffold_of[lig] = MolToSmiles(MurckoScaffold.GetScaffoldForMol(mol))
        except Exception:                            # pragma: no cover — perception edge
            scaffold_of[lig] = lig
    counts: dict[str, int] = {}
    for scaf in scaffold_of.values():
        counts[scaf] = counts.get(scaf, 0) + 1
    return {lig: counts[scaf] for lig, scaf in scaffold_of.items()}


def build_from_directory(input_dir: Path, out_dir: Path, cfg: PharmacophoreConfig,
                         smiles_map: dict[str, str] | None = None,
                         name: str | None = None,
                         reference_pdb: Path | None = None) -> ModelOutputs | None:
    """Build a pharmacophore from any directory of aligned ``*.mol2`` compounds.

    Returns ``None`` (and writes nothing) when the set has fewer than
    ``selection.min_ligands`` loadable ligands — too few to define a hypothesis.
    ``reference_pdb`` (aligned receptor) enables excluded-volume spheres for the
    density consensus strategy; it is ignored by the k-means path.
    """
    name = name or input_dir.name
    molecules, report = load_directory(input_dir, smiles_map)

    if len(molecules) < cfg.selection.min_ligands:
        log.info("[%s] only %d ligand(s) < min_ligands=%d — skipped",
                 name, len(molecules), cfg.selection.min_ligands)
        return None

    factory = feature_factory(cfg.features.fdef)
    table = build_table(molecules, factory, cfg.features.families,
                        cfg.features.feature_hierarchy)
    metadata = {
        "source": {"input_dir": str(input_dir), "n_ligands": len(molecules),
                   "load": report.by_method, "skipped": report.skipped},
        "selection": asdict(cfg.selection),
        "tolerance": asdict(cfg.tolerance),
        "created": date.today().isoformat(),
    }
    ligand_atoms = protein_atoms = scaffold_freq = None
    if cfg.consensus_method == "density":
        if cfg.density.scaffold_weighting:
            scaffold_freq = _scaffold_frequencies(molecules)
        if cfg.density.excluded_volume and reference_pdb and reference_pdb.exists():
            ligand_atoms = _ligand_atom_coords(molecules)
            protein_atoms = read_protein_atom_coords(reference_pdb)
    result = build_consensus(table, cfg, name, metadata, ligand_atoms=ligand_atoms,
                             protein_atoms=protein_atoms, scaffold_freq=scaffold_freq)

    rep_id = best_representative(table, result.pharmacophore)
    rep_mol = dict(molecules).get(rep_id) if rep_id else None
    result.pharmacophore.metadata["representative_ligand"] = rep_id
    result.pharmacophore.metadata["feature_resolution"] = _aggregate_resolutions(
        table.resolutions)

    ensure_dir(out_dir)
    # Drop per-family plots from a previous run (e.g. an old `Hydrophobe` family)
    # so the dir never carries stale artifacts after a config change.
    for stale in out_dir.glob("raw_features_*.png"):
        stale.unlink()
    ligand_file: Path | None = None
    if rep_mol is not None:
        ligand_file = write_representative_sdf(
            rep_mol, rep_id, out_dir / "representative_ligand.sdf")
    files = [
        write_json(result.pharmacophore, out_dir / "pharmacophore.json"),
        write_features_csv(result, out_dir / "features.csv"),
        write_pml(result.pharmacophore, out_dir / "pharmacophore.pml",
                  cfg.features.colors, ligand_file=ligand_file),
        _write_summary(result, report, len(molecules),
                       out_dir / "model_summary.md"),
    ]
    if ligand_file is not None:
        files.append(ligand_file)
    files.extend(plot_raw_features(result, out_dir))
    log.info("[%s] %d features from %d ligands -> %s",
             name, len(result.pharmacophore.features), len(molecules), out_dir)
    return ModelOutputs(name=name, model_dir=out_dir,
                        pharmacophore=result.pharmacophore, report=report, files=files)


def build_for_cell(cell_dir: Path, out_dir: Path, cfg: PharmacophoreConfig,
                   unique_ligands_csv: Path, name: str | None = None,
                   reference_pdb: Path | None = None) -> ModelOutputs | None:
    """Catalogue convention: SMILES from the target's unique_ligands.csv.

    Prefers the pH-7.4 ``protonated_ligands.csv`` (written by
    ``scripts/protonate_ligands.py``) when present, overlaying it onto the neutral map
    so HETs without a protonation entry keep their original SMILES.
    """
    smiles_map = read_smiles_map(unique_ligands_csv)
    protonated = read_protonation_map(unique_ligands_csv.parent / "protonated_ligands.csv")
    if protonated:
        smiles_map = {**smiles_map, **protonated}
    return build_from_directory(cell_dir, out_dir, cfg, smiles_map=smiles_map,
                                name=name, reference_pdb=reference_pdb)
