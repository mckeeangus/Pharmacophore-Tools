"""Load config/efficacy.yaml into typed efficacy / reference-state annotations.

The pipeline never infers efficacy; it only looks it up here. A lookup returns a
fully-resolved :class:`EfficacyCall` so callers don't re-implement the
default/unknown fallback logic.
"""

from __future__ import annotations

import csv
from dataclasses import dataclass, field
from pathlib import Path

import yaml

from ..util.paths import CATALOGUE_DIR, CONFIG_DIR

# Allowed efficacy signs (plus the explicit "unknown" review bucket).
EFFICACY_SIGNS = ("positive", "neutral", "negative")
REVERSIBLE = "reversible"
SEPARATE_STATE = "separate_state"


@dataclass(frozen=True)
class EfficacyCall:
    """The resolved annotation for one ligand at its pocket."""
    efficacy: str           # positive | neutral | negative | unknown
    track: str              # reversible | separate_state
    source: str             # provenance of the call
    note: str = ""          # human-readable rationale / drug identity
    reason: str = ""        # why it was routed to separate_state

    @property
    def is_separate_state(self) -> bool:
        return self.track == SEPARATE_STATE

    @property
    def is_unknown(self) -> bool:
        return self.track == REVERSIBLE and self.efficacy == "unknown"


@dataclass
class TargetEfficacy:
    slug: str
    klass: str
    default_efficacy: str | None
    ligands: dict[str, dict]
    default_source: str
    # Stage 3.3: ChEMBL-resolved calls, used only as a fallback below curated
    # config and the target default (so curation always wins).
    resolved: dict[str, EfficacyCall] = field(default_factory=dict)

    def call(self, het: str) -> EfficacyCall:
        het = het.upper()
        entry = self.ligands.get(het)
        if entry is None:
            if self.default_efficacy:
                return EfficacyCall(self.default_efficacy, REVERSIBLE,
                                    source=f"{self.default_source} (target default)",
                                    note=f"{self.klass} target default")
            if het in self.resolved:
                return self.resolved[het]
            return EfficacyCall("unknown", REVERSIBLE, source="", note="no annotation")
        if entry.get("track") == SEPARATE_STATE:
            return EfficacyCall("n/a", SEPARATE_STATE,
                                source=entry.get("source", self.default_source),
                                note=entry.get("note", ""),
                                reason=entry.get("reason", "separate reference state"))
        return EfficacyCall(entry.get("efficacy", "unknown"), REVERSIBLE,
                            source=entry.get("source", self.default_source),
                            note=entry.get("note", ""))


@dataclass
class EfficacyConfig:
    default_source: str
    targets: dict[str, TargetEfficacy]

    def get(self, slug: str) -> TargetEfficacy:
        if slug in self.targets:
            return self.targets[slug]
        # A target with no config block still resolves (everything -> unknown).
        return TargetEfficacy(slug=slug, klass="unspecified", default_efficacy=None,
                              ligands={}, default_source=self.default_source)


def load_resolved(path: str | Path | None = None) -> dict[str, dict[str, EfficacyCall]]:
    """Load ChEMBL-resolved calls (Stage 3.3) keyed ``{slug: {het: call}}``.

    Reads ``catalogue/stage3_efficacy_resolved.csv`` if present. Only rows with a
    decided sign or a separate-state route are kept; ``unknown`` rows are dropped
    so they remain on the review list rather than masking the no-annotation path.
    """
    path = Path(path) if path else CATALOGUE_DIR / "stage3_efficacy_resolved.csv"
    out: dict[str, dict[str, EfficacyCall]] = {}
    if not Path(path).exists():
        return out
    for row in csv.DictReader(Path(path).open(encoding="utf-8")):
        slug, het = row.get("target", ""), row.get("het", "").upper()
        track = row.get("track", "cell")
        sign = row.get("sign", "unknown")
        if not slug or not het:
            continue
        source = f"{row.get('source', 'chembl')} ({row.get('confidence', '')})".strip()
        if track == SEPARATE_STATE:
            call = EfficacyCall("n/a", SEPARATE_STATE, source=source,
                                note=row.get("note", ""),
                                reason=row.get("note", "") or "degrader/separate state")
        elif sign in EFFICACY_SIGNS:
            call = EfficacyCall(sign, REVERSIBLE, source=source, note=row.get("note", ""))
        else:
            continue  # unknown -> stays on the review list
        out.setdefault(slug, {})[het] = call
    return out


def load_efficacy(path: str | Path | None = None,
                  resolved_path: str | Path | None = None) -> EfficacyConfig:
    path = Path(path) if path else CONFIG_DIR / "efficacy.yaml"
    raw = yaml.safe_load(Path(path).read_text(encoding="utf-8")) or {}
    default_source = (raw.get("defaults") or {}).get("source", "curated")
    resolved = load_resolved(resolved_path)
    targets: dict[str, TargetEfficacy] = {}
    for slug, body in (raw.get("targets") or {}).items():
        body = body or {}
        ligands = {k.upper(): dict(v or {}) for k, v in (body.get("ligands") or {}).items()}
        targets[slug] = TargetEfficacy(
            slug=slug,
            klass=str(body.get("class", "unspecified")),
            default_efficacy=body.get("default_efficacy"),
            ligands=ligands,
            default_source=default_source,
            resolved=resolved.get(slug, {}),
        )
    return EfficacyConfig(default_source=default_source, targets=targets)
