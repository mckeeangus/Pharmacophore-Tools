"""Build one pharmacophore model from a directory of aligned compounds (Stage 4).

This is the orchestration edge: it wires the pure pieces (load -> featurize ->
cluster -> assemble) and writes the model artifacts. The general entry point is
``build_from_directory``; ``build_for_cell`` adds the catalogue convention
(SMILES sourced from the target's unique_ligands.csv).
"""

from __future__ import annotations

import logging
from dataclasses import asdict, dataclass, field, replace
from datetime import date
from pathlib import Path

import numpy as np

from ..features.conformers import generate_conformers
from ..features.dock_load import (
    load_docked_set,
    read_protonated_smiles,
    read_rank_index,
    write_manifest,
)
from ..features.extract import (
    FeaturePoint,
    FeatureResolution,
    FeatureTable,
    build_table,
    conformer_features,
    feature_factory,
)
from ..features.load import (
    LoadReport,
    load_directory,
    read_protonation_map,
    read_smiles_map,
)
from ..util.paths import ensure_dir
from .align import seed_align, write_alignment_manifest
from .build import best_representative
from .config import PharmacophoreConfig
from .density import build_density
from .io import (
    write_aligned_points_csv,
    write_aligned_sdf,
    write_features_csv,
    write_json,
    write_model_csv,
    write_pml,
    write_representative_sdf,
)
from .model import Pharmacophore
from .viz import plot_raw_features

log = logging.getLogger("pharmpipe.pharmacophore.run")


@dataclass
class ModelOutputs:
    name: str
    model_dir: Path
    pharmacophore: Pharmacophore | None  # None for an align-only run (no KDE model built)
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


def _occupancy(n_points: int, n_ligands: int) -> float:
    """Points per contributing ligand (``n_points / n_ligands``), uncapped.

    One ligand can drop several same-family points into one cluster, so this is ≥ 1.0
    whenever a cluster is denser than one point per ligand. Unlike ``support`` (a
    fraction of ligands, ≤ 1.0) it is reported honestly, never clamped."""
    return n_points / n_ligands if n_ligands else 0.0


def _below_floor_features(
    result, n_ligands: int, exclude: set[tuple[str, int]], membership_radius: float,
) -> list[tuple[str, int, int, float]]:
    """Peaks that formed but never became candidates — below the support/size floor —
    as ``(family, n_points, n_ligands, support)`` sorted by support then size.

    A peak is here when its label is absent from the family's ``kept_labels`` *and* it was
    not displaced by the overlap merge (``exclude`` = the merged-away keys, reported
    separately). Support uses the SAME membership radius as the model (distinct ligands
    with a point within ``membership_radius`` of the peak centre), so the reported support
    matches the reason the peak was dropped — not the basin count.
    """
    rows: list[tuple[str, int, int, float]] = []
    for a in result.assignments:
        for lbl in sorted(set(a.labels.tolist())):
            centre = a.centers.get(int(lbl))
            if lbl in a.kept_labels or (a.family, int(lbl)) in exclude or centre is None:
                continue
            within = np.linalg.norm(a.coords - np.asarray(centre), axis=1) <= membership_radius
            n_points = int(within.sum())
            n_lig = len({lig for lig, m in zip(a.ligand_ids, within, strict=True) if m})
            support = n_lig / n_ligands if n_ligands else 0.0
            rows.append((a.family, n_points, n_lig, support))
    rows.sort(key=lambda r: (r[3], r[1]), reverse=True)
    return rows


_DIRECTIONAL_FAMILIES = frozenset({"Acceptor", "Donor"})


def _write_summary(result, report: LoadReport, n_ligands: int,
                   membership_radius: float, path: Path,
                   directional_caveat: bool = False) -> Path:
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
    if directional_caveat:
        lines += [
            "",
            "> **Directional features (Acceptor, Donor) are low-confidence in this build "
            "(marked †).** Reconstructed from aligned poses, they inherit the docking "
            "pose/flip ambiguity — a correctly placed ring can present its H-bond atom in the "
            "wrong orientation. The cation/aromatic anchors are pose-invariant and trustworthy.",
        ]
    lines += [
        "",
        "**Support** = fraction of the cell's ligands that contribute to a feature (≤ 1.0; "
        "features are kept only above the 0.5 support floor). **Occupancy** = points ÷ "
        "contributing ligands (points-per-ligand, uncapped: > 1.0 when a cluster is denser "
        "than one point per ligand). One row per feature / peak.",
        "",
        "| Feature | Points | Ligands | Support | Occupancy |", "|---|---:|---:|---:|---:|",
    ]
    for f in sorted(ligand_feats, key=lambda f: (f.family, _feature_ordinal(f))):
        mark = " †" if directional_caveat and f.family in _DIRECTIONAL_FAMILIES else ""
        lines.append(
            f"| {(f.label or f.family)}{mark} | {f.n_points} | {f.n_ligands} | {f.support:.2f} "
            f"| {_occupancy(f.n_points, f.n_ligands):.2f} |")
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
    merged_away = getattr(result, "merged_away", [])
    if merged_away:
        lines += [
            "", "## Merged away",
            "", "Clusters that passed the support/size floor but were displaced by the "
            "1 Å cross-family overlap merge — one feature per region, keeping the denser "
            "one. Each row states in favour of which kept feature it was removed.",
            "", "| Feature | Points | Ligands | Support | Occupancy | In favour of |",
            "|---|---:|---:|---:|---:|---|",
        ]
        for r in sorted(merged_away,
                        key=lambda r: (r.dropped_support, r.dropped_points), reverse=True):
            occ = _occupancy(r.dropped_points, r.dropped_ligands)
            lines.append(
                f"| {r.dropped_family} | {r.dropped_points} | {r.dropped_ligands} "
                f"| {r.dropped_support:.2f} | {occ:.2f} | {r.winner_label} |")
    exclude = {(r.dropped_family, r.dropped_cluster_label) for r in merged_away}
    below = _below_floor_features(result, n_ligands, exclude, membership_radius)
    if below:
        lines += [
            "", "## Below the support/size floor",
            "", "Clusters that formed but never became candidates — below the 0.5 support "
            "floor or the minimum cluster size.",
            "", "| Feature | Points | Ligands | Support | Occupancy |",
            "|---|---:|---:|---:|---:|",
        ]
        for fam, npts, nlig, sup in below:
            lines.append(
                f"| {fam} | {npts} | {nlig} | {sup:.2f} | {_occupancy(npts, nlig):.2f} |")
    lines += ["", "See `pharmacophore_model.json` (model), `features.csv` (raw points + "
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


def build_from_molecules(molecules: list[tuple[str, object]], report: LoadReport,
                         out_dir: Path, cfg: PharmacophoreConfig, *,
                         source: dict, name: str,
                         reference_pdb: Path | None = None,
                         extra_files: list[Path] | None = None) -> ModelOutputs | None:
    """Build + write one model from already-loaded aligned poses (the shared core).

    ``source`` is copied into the model metadata verbatim, so each entry point records
    its own provenance (mol2 directory vs docked screening set). ``extra_files`` are
    appended to the artifact list (e.g. a docking manifest). Returns ``None`` (writing
    nothing) when fewer than ``selection.min_ligands`` poses loaded. ``reference_pdb``
    (aligned receptor) enables density excluded-volume spheres.
    """
    if not molecules:
        log.warning("[%s] no ligands loaded — nothing to build", name)
        return None
    if len(molecules) < cfg.selection.min_ligands:
        log.warning("[%s] only %d ligand(s) < min_ligands=%d — building anyway; with so few "
                    "molecules the consensus is weak (a 0.5-support feature may rest on one or "
                    "two ligands), so treat the model as provisional",
                    name, len(molecules), cfg.selection.min_ligands)

    factory = feature_factory(cfg.features.fdef)
    table = build_table(molecules, factory, cfg.features.families,
                        cfg.features.feature_hierarchy)
    metadata = {
        "source": source,
        "selection": asdict(cfg.selection),
        "tolerance": asdict(cfg.tolerance),
        "created": date.today().isoformat(),
        "consensus_method": "density",
    }
    scaffold_freq = _scaffold_frequencies(molecules) if cfg.density.scaffold_weighting else None
    result = build_density(table, cfg.density, cfg.tolerance, name, metadata,
                           min_support=cfg.selection.min_support_fraction,
                           scaffold_freq=scaffold_freq)

    rep_id = best_representative(table, result.pharmacophore)
    rep_mol = dict(molecules).get(rep_id) if rep_id else None
    return _write_model_artifacts(
        result, report, out_dir, cfg, name=name, rep_id=rep_id, rep_mol=rep_mol,
        resolutions=table.resolutions, n_ligands=len(molecules), extra_files=extra_files)


def _write_model_artifacts(result, report: LoadReport, out_dir: Path,
                           cfg: PharmacophoreConfig, *, name: str, rep_id: str | None,
                           rep_mol, resolutions: list, n_ligands: int,
                           extra_files: list[Path] | None = None,
                           directional_caveat: bool = False) -> ModelOutputs:
    """Write the model artifacts (json/csv/pml/summary/plots + representative) for a built
    ``BuildResult`` — the shared tail every build path (mol2, docked, seed-alignment) reuses.

    ``directional_caveat`` marks Acceptor/Donor features low-confidence in the summary (the
    alignment build, where directional features inherit the docking flip).
    """
    result.pharmacophore.metadata["representative_ligand"] = rep_id
    result.pharmacophore.metadata["feature_resolution"] = _aggregate_resolutions(resolutions)

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
        write_model_csv(result.pharmacophore, out_dir / "pharmacophore.csv"),
        write_json(result.pharmacophore, out_dir / "pharmacophore_model.json"),
        write_features_csv(result, out_dir / "features.csv"),
        write_pml(result.pharmacophore, out_dir / "pharmacophore_pymol.pml",
                  cfg.features.colors, ligand_file=ligand_file),
        _write_summary(result, report, n_ligands, cfg.density.membership_radius,
                       out_dir / "model_summary.md", directional_caveat=directional_caveat),
    ]
    if ligand_file is not None:
        files.append(ligand_file)
    files.extend(extra_files or [])
    files.extend(plot_raw_features(result, out_dir))
    log.info("[%s] %d features from %d ligands -> %s",
             name, len(result.pharmacophore.features), n_ligands, out_dir)
    return ModelOutputs(name=name, model_dir=out_dir,
                        pharmacophore=result.pharmacophore, report=report, files=files)


def build_from_directory(input_dir: Path, out_dir: Path, cfg: PharmacophoreConfig,
                         smiles_map: dict[str, str] | None = None,
                         name: str | None = None,
                         reference_pdb: Path | None = None) -> ModelOutputs | None:
    """Build a pharmacophore from any directory of aligned ``*.mol2`` compounds.

    Returns ``None`` (and writes nothing) when the set has fewer than
    ``selection.min_ligands`` loadable ligands — too few to define a hypothesis.
    ``reference_pdb`` (aligned receptor) enables excluded-volume spheres.
    """
    name = name or input_dir.name
    molecules, report = load_directory(input_dir, smiles_map)
    source = {"input_dir": str(input_dir), "n_ligands": len(molecules),
              "load": report.by_method, "skipped": report.skipped}
    return build_from_molecules(molecules, report, out_dir, cfg, source=source,
                                name=name, reference_pdb=reference_pdb)


def build_from_docked_set(docked_dir: Path, index_csv: Path, out_dir: Path,
                          cfg: PharmacophoreConfig, *, top_n_hits: int,
                          top_n_poses: int = 1, name: str | None = None,
                          reference_pdb: Path | None = None,
                          score_column: str = "drugclip_score",
                          pose_score: str = "cnnaffinity",
                          max_vina: float | None = None) -> ModelOutputs | None:
    """Build a pharmacophore from a DrugCLIP -> GNINA docked screening directory.

    Treats the top-``top_n_hits`` ranked compounds (best ``top_n_poses`` poses each,
    default 1) as one aligned active set and emits a single hypothesis, alongside a
    ``docked_manifest.csv`` recording the rank/pose provenance of every loaded pose. Poses
    are chosen by ``pose_score`` binding quality (``max_vina`` optional clash filter), not
    raw SDF order. Returns ``None`` when fewer than ``selection.min_ligands`` poses loaded.
    """
    name = name or docked_dir.name
    molecules, report, manifest = load_docked_set(
        docked_dir, index_csv, top_n_hits, top_n_poses, score_column, pose_score, max_vina)
    source = {"docked_dir": str(docked_dir), "index": str(index_csv),
              "score_column": score_column, "top_n_hits": top_n_hits,
              "top_n_poses": top_n_poses, "pose_score": pose_score, "max_vina": max_vina,
              "n_hits": len({r.mol_id for r in manifest}),
              "n_ligands": len(molecules),
              "load": report.by_method, "skipped": report.skipped}
    ensure_dir(out_dir)
    manifest_file = write_manifest(manifest, out_dir / "docked_manifest.csv")
    return build_from_molecules(molecules, report, out_dir, cfg, source=source,
                                name=name, reference_pdb=reference_pdb,
                                extra_files=[manifest_file])


def _aligned_ligand_atoms(seed_mols, transforms, conf_mols) -> np.ndarray:
    """Heavy(+H)-atom coords of the aligned ligand envelope, for excluded volume.

    Seed poses are already in frame; each aligned compound's chosen conformer is transformed
    by its clique rotation/translation. Best-effort — a mol that fails to transform is skipped.
    """
    blocks = [m.GetConformer().GetPositions() for _, m in seed_mols if m.GetNumConformers()]
    for lig, (rot, trans, ci) in transforms.items():
        mol, cids = conf_mols.get(lig, (None, None))
        if mol is None or ci >= len(cids):
            continue
        try:
            pos = mol.GetConformer(cids[ci]).GetPositions()
            blocks.append(pos @ rot.T + trans)
        except Exception:                                # pragma: no cover — conformer edge
            continue
    return np.vstack(blocks) if blocks else np.empty((0, 3), dtype=float)


def _read_seed_sdf(path: Path) -> list[tuple[str, object]]:
    """Read an arbitrary 3D-coordinate seed (crystal ligand or docked poses) -> [(id, mol)].

    Accepts ``.sdf`` (multi-record) or ``.mol2`` (single molecule). The seed's coordinates are
    kept verbatim, so a ligand given in a protein's coordinate frame yields a pharmacophore
    positioned in that binding site. A ``.mol2`` is read directly (sanitized); a heavy-atom-only
    mol2 with no bond orders may perceive features poorly — prefer an SDF (or a bond-order-correct
    mol2) for the seed.
    """
    from rdkit import Chem

    if path.suffix.lower() == ".mol2":
        mol = Chem.MolFromMol2File(str(path), removeHs=True, sanitize=True)
        return [(mol.GetProp("_Name") if mol.HasProp("_Name") and mol.GetProp("_Name")
                 else "seed0", mol)] if mol is not None else []
    out = []
    for i, mol in enumerate(Chem.SDMolSupplier(str(path), removeHs=True)):
        if mol is None:
            continue
        name = mol.GetProp("_Name") if mol.HasProp("_Name") and mol.GetProp("_Name") else f"seed{i}"
        out.append((name, mol))
    return out


def _aligned_entries(res, conf_mols: dict, ranks: dict):
    """Per-compound ``(mol, conf_id, R, t, tags)`` for ``io.write_aligned_sdf``."""
    entries = []
    rmsd_by_lig = {m.ligand_id: m.rmsd for m in res.manifest}
    for lig, (rot, trans, ci) in res.transforms.items():
        mol, cids = conf_mols.get(lig, (None, None))
        if mol is None or ci >= len(cids):
            continue
        rmsd = round(rmsd_by_lig.get(lig, float("nan")), 3)
        entries.append((mol, cids[ci], rot, trans,
                        {"mol_id": lig, "drugclip_rank": ranks.get(lig, ""),
                         "conformer": ci, "align_rmsd": rmsd}))
    return entries


def _set_feature_directions(pharmacophore, pooled_points, membership_radius: float) -> None:
    """Populate each directional feature's `direction` from the consensus of nearby aligned points.

    For every kept directional feature (Donor/Acceptor/Aromatic), take the mean of the aligned
    pooled points' directions of the same family within ``membership_radius`` of the feature centre
    (unit-normalised). Frozen dataclass, so features are rebuilt via ``replace``. Populates the
    model's previously-unused `direction` field with the orientation the alignment agreed on.
    """
    from .align import _mean_direction
    directional = {"Donor", "Acceptor", "Aromatic"}
    new = []
    for f in pharmacophore.features:
        if f.family in directional:
            centre = np.array([f.x, f.y, f.z])
            dirs = [d for fam, xyz, d, _ in pooled_points
                    if fam == f.family and d is not None
                    and np.linalg.norm(xyz - centre) <= membership_radius]
            md = _mean_direction(dirs)
            if md is not None:
                f = replace(f, direction=(float(md[0]), float(md[1]), float(md[2])))
        new.append(f)
    pharmacophore.features = new


def build_from_seed_alignment(docked_dir: Path, index_csv: Path, out_dir: Path,
                              cfg: PharmacophoreConfig, *, top_n_hits: int,
                              seed_k: int | None = None, name: str | None = None,
                              reference_pdb: Path | None = None,
                              smiles_map: dict[str, str] | None = None,
                              seed_poses: Path | None = None, seedless: bool = False,
                              align_only: bool = False) -> ModelOutputs | None:
    """Feature-alignment build: initialise a consensus frame, align the ranked set onto it.

    Conformer ensembles are embedded for the top-``top_n_hits`` DrugCLIP-ranked compounds
    (high-energy conformers discarded, see ``generate_conformers``), then aligned onto a
    reference by feature-clique matching with EM refinement (``align.seed_align``). The frame is
    initialised one of three ways:

    * **seedless** (default): the top-ranked compound's lowest-energy conformer seeds the frame and
      stays as a member of the consensus;
    * **seed_poses** (``--seed``): an external 3D-coordinate seed (a holo co-crystal ligand, .sdf or
      .mol2) is used as a **bootstrap scaffold** — it anchors the frame through the growing pass
      then is dropped before EM (``bootstrap_seed``), so the model reflects the aligned compounds
      alone but inherits the seed's (binding-site) coordinate frame;
    * **docked**: the top-``seed_k`` docked poses in ``docked_dir`` seed the frame and are members.

    Writes the aligned compound set (``aligned_compounds.sdf``) always. With ``align_only`` it stops
    there (+ points CSV + manifest, no KDE); otherwise the density KDE runs and the full model
    artifacts are written. Returns ``None`` when fewer than ``selection.min_ligands`` align. This
    path is orthogonal to the catalogue build. Directional features are flagged low-confidence.
    """
    tag = "seedless" if seedless else ("seed" if seed_poses else "docked")
    name = name or f"{docked_dir.name}_{tag}"
    acfg = cfg.alignment
    seed_k = seed_k if seed_k is not None else acfg.seed_k
    families = acfg.align_families or cfg.features.families
    hierarchy = cfg.features.feature_hierarchy
    factory = feature_factory(cfg.features.fdef)
    smiles_map = smiles_map or {}
    report = LoadReport()

    def _seed_pts(lig, mol):                          # (family, xyz, direction, ligand_id) per pose
        return [(f, xyz, d, lig)
                for f, xyz, d in conformer_features(mol, factory, families, hierarchy, 0)]

    # 1. seed frame + which mol_ids are excluded from the aligned set
    seed_points: list[tuple] = []                    # (family, xyz, direction, ligand_id)
    seed_mols: list[tuple[str, object]] = []
    excluded_mol_ids: set[str] = set()
    if seedless:
        pass  # built from the top compound after conformers are generated
    elif seed_poses is not None:
        seed_mols = _read_seed_sdf(seed_poses)
        for lig, mol in seed_mols:
            seed_points += _seed_pts(lig, mol)
    else:
        seed_mols, _, _ = load_docked_set(docked_dir, index_csv, seed_k, 1,
                                          pose_score="cnnaffinity")
        if not seed_mols:
            log.warning("[%s] no docked seed poses loaded — cannot seed the model", name)
            return None
        for lig, mol in seed_mols:
            seed_points += _seed_pts(lig, mol)
        excluded_mol_ids = {lig.split("__", 1)[0] for lig, _ in seed_mols}

    # 2. conformer ensembles for the ranked compounds
    compounds: list[tuple[str, list]] = []
    conf_mols: dict = {}
    ranks: dict[str, int] = {}
    for hit in read_rank_index(index_csv)[:max(top_n_hits, 0)]:
        if hit.mol_id in excluded_mol_ids:
            continue
        # Protonation: prefer the docked pH-7.4 protonated_smiles over the neutral index SMILES,
        # so an amine is embedded as its real ammonium (charge + N-H donor). The protonated-amine
        # invertomer is left as the ensemble's natural mixture — the docked pose is NOT used to
        # lock it (see docs/molecule_alignment.md §1: those poses came from the same embedding, so
        # their invertomer is an arbitrary pick, not a bioactive reference).
        smi = (smiles_map.get(hit.mol_id)
               or read_protonated_smiles(docked_dir, hit.mol_id) or hit.smiles)
        gen = generate_conformers(smi, acfg)
        if gen is None:
            continue
        mol, cids, _energies = gen
        compounds.append((hit.mol_id,
                          [conformer_features(mol, factory, families, hierarchy, c) for c in cids]))
        conf_mols[hit.mol_id] = (mol, cids)
        ranks[hit.mol_id] = hit.rank

    if seedless:
        if not compounds:
            log.warning("[%s] no conformers generated — cannot seed seedless", name)
            return None
        top_lig, top_clouds = compounds[0]
        seed_points = [(f, xyz, d, top_lig) for f, xyz, d in top_clouds[0]]  # lowest-energy conf
    if not seed_points:
        log.warning("[%s] empty seed frame — nothing to align to", name)
        return None

    # 3. feature-clique alignment with EM refinement (orientation-aware when configured)
    res = seed_align(seed_points, compounds, dist_tol=acfg.dist_tol, min_clique=acfg.min_clique,
                     membership_radius=cfg.density.membership_radius,
                     max_align_rmsd=acfg.max_align_rmsd, max_clique_nodes=acfg.max_clique_nodes,
                     em_iterations=acfg.em_iterations, em_tol=acfg.em_tol,
                     use_directions=acfg.use_directions, projected_length=acfg.projected_length,
                     bootstrap_seed=(seed_poses is not None))
    aligned_ids = sorted({lig for *_, lig in res.points})
    n_aligned = sum(1 for r in res.manifest if r.source == "aligned" and r.aligned)
    n_dropped = sum(1 for r in res.manifest if r.source == "aligned" and not r.aligned)
    if not aligned_ids:
        log.warning("[%s] no ligands aligned — nothing to build", name)
        return None
    if len(aligned_ids) < cfg.selection.min_ligands:
        log.warning("[%s] only %d aligned ligand(s) < min_ligands=%d — building anyway; the "
                    "consensus is weak with so few molecules, so treat the model as provisional",
                    name, len(aligned_ids), cfg.selection.min_ligands)

    ensure_dir(out_dir)
    aligned_sdf = write_aligned_sdf(_aligned_entries(res, conf_mols, ranks),
                                    out_dir / "aligned_compounds.sdf")
    manifest_file = write_alignment_manifest(res.manifest, out_dir / "alignment_manifest.csv")
    log.info("[%s] %s init: aligned %d/%d compounds -> %d ligands; EM %s",
             name, tag, n_aligned, n_aligned + n_dropped, len(aligned_ids),
             res.convergence[-1] if res.convergence else "off")

    if align_only:
        points_csv = write_aligned_points_csv(res.points, out_dir / "aligned_points.csv")
        log.info("[%s] align-only -> %s", name, out_dir)
        return ModelOutputs(name=name, model_dir=out_dir, pharmacophore=None, report=report,
                            files=[aligned_sdf, manifest_file, points_csv])

    # 4. pooled aligned points -> FeatureTable -> density KDE model
    pts = [FeaturePoint(fam, float(x[0]), float(x[1]), float(x[2]), lig)
           for fam, x, _d, lig in res.points]
    table = FeatureTable(points=pts, ligand_ids=aligned_ids)
    metadata = {
        "source": {"method": "seed_alignment", "init": tag, "docked_dir": str(docked_dir),
                   "index": str(index_csv), "seed_k": seed_k, "top_n_hits": top_n_hits,
                   "dist_tol": acfg.dist_tol, "min_clique": acfg.min_clique,
                   "max_align_rmsd": acfg.max_align_rmsd,
                   "em_iterations": acfg.em_iterations, "em_convergence": res.convergence,
                   "n_seed": len({lig for lig, _ in seed_mols}), "n_aligned": n_aligned,
                   "n_dropped": n_dropped, "n_ligands": len(aligned_ids)},
        "selection": asdict(cfg.selection), "tolerance": asdict(cfg.tolerance),
        "created": date.today().isoformat(), "consensus_method": "density",
    }
    result = build_density(table, cfg.density, cfg.tolerance, name, metadata,
                           min_support=cfg.selection.min_support_fraction)
    if acfg.use_directions:
        _set_feature_directions(result.pharmacophore, res.points,
                                cfg.density.membership_radius)

    rep_id, rep_mol = (seed_mols[0] if seed_mols else (aligned_ids[0], None))
    return _write_model_artifacts(
        result, report, out_dir, cfg, name=name, rep_id=rep_id, rep_mol=rep_mol,
        resolutions=[], n_ligands=len(aligned_ids),
        extra_files=[manifest_file, aligned_sdf], directional_caveat=True)


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
