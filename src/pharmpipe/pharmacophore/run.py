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

from ..clustering.registry import get_clusterer
from ..features.extract import build_table, feature_factory
from ..features.load import LoadReport, load_directory, read_smiles_map
from ..util.paths import ensure_dir
from .build import best_representative, build_pharmacophore
from .config import PharmacophoreConfig
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


def _write_summary(ph: Pharmacophore, report: LoadReport, n_ligands: int,
                   path: Path) -> Path:
    by_family: dict[str, int] = {}
    for f in ph.features:
        by_family[f.family] = by_family.get(f.family, 0) + 1
    lines = [
        f"# Pharmacophore — {ph.name}", "",
        f"- Ligands loaded: **{n_ligands}** "
        f"({', '.join(f'{k}={v}' for k, v in sorted(report.by_method.items())) or 'none'})",
        f"- Skipped poses: {len(report.skipped)}"
        + (f" ({', '.join(f'{lid}:{why}' for lid, why in report.skipped)})"
           if report.skipped else ""),
        f"- Clustering: `{ph.metadata.get('clustering', {}).get('method', '?')}`",
        f"- Representative ligand (viz): `{ph.metadata.get('representative_ligand') or 'none'}`",
        f"- Features kept: **{len(ph.features)}**", "",
        "| Family | Features | Mean support |", "|---|---:|---:|",
    ]
    for fam in sorted(by_family):
        feats = [f for f in ph.features if f.family == fam]
        mean_support = sum(f.support for f in feats) / len(feats)
        lines.append(f"| {fam} | {len(feats)} | {mean_support:.2f} |")
    lines += ["", "See `pharmacophore.json` (model), `features.csv` (raw points + "
              "cluster ids), and `raw_features_*.png` (per-family point distributions)."]
    path.write_text("\n".join(lines), encoding="utf-8")
    return path


def build_from_directory(input_dir: Path, out_dir: Path, cfg: PharmacophoreConfig,
                         smiles_map: dict[str, str] | None = None,
                         name: str | None = None) -> ModelOutputs | None:
    """Build a pharmacophore from any directory of aligned ``*.mol2`` compounds.

    Returns ``None`` (and writes nothing) when the set has fewer than
    ``selection.min_ligands`` loadable ligands — too few to define a hypothesis.
    """
    name = name or input_dir.name
    molecules, report = load_directory(input_dir, smiles_map)

    if len(molecules) < cfg.selection.min_ligands:
        log.info("[%s] only %d ligand(s) < min_ligands=%d — skipped",
                 name, len(molecules), cfg.selection.min_ligands)
        return None

    factory = feature_factory(cfg.features.fdef)
    table = build_table(molecules, factory, cfg.features.families)
    clusterer = get_clusterer(cfg.clustering.method, cfg.clustering.params)
    metadata = {
        "source": {"input_dir": str(input_dir), "n_ligands": len(molecules),
                   "load": report.by_method, "skipped": report.skipped},
        "selection": asdict(cfg.selection),
        "tolerance": asdict(cfg.tolerance),
        "created": date.today().isoformat(),
    }
    result = build_pharmacophore(table, clusterer, cfg.selection, cfg.tolerance,
                                 name, metadata)

    rep_id = best_representative(table, result.pharmacophore)
    rep_mol = dict(molecules).get(rep_id) if rep_id else None
    result.pharmacophore.metadata["representative_ligand"] = rep_id

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
        _write_summary(result.pharmacophore, report, len(molecules),
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
                   ) -> ModelOutputs | None:
    """Catalogue convention: take SMILES from the target's unique_ligands.csv."""
    smiles_map = read_smiles_map(unique_ligands_csv)
    return build_from_directory(cell_dir, out_dir, cfg, smiles_map=smiles_map, name=name)
