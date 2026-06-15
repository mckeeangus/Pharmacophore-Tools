"""Load config/efficacy.yaml into typed efficacy / reference-state annotations.

The pipeline never infers efficacy; it only looks it up here. A lookup returns a
fully-resolved :class:`EfficacyCall` so callers don't re-implement the
default/unknown fallback logic.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import yaml

from ..util.paths import CONFIG_DIR

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

    def call(self, het: str) -> EfficacyCall:
        entry = self.ligands.get(het.upper())
        if entry is None:
            if self.default_efficacy:
                return EfficacyCall(self.default_efficacy, REVERSIBLE,
                                    source=f"{self.default_source} (target default)",
                                    note=f"{self.klass} target default")
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


def load_efficacy(path: str | Path | None = None) -> EfficacyConfig:
    path = Path(path) if path else CONFIG_DIR / "efficacy.yaml"
    raw = yaml.safe_load(Path(path).read_text(encoding="utf-8")) or {}
    default_source = (raw.get("defaults") or {}).get("source", "curated")
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
        )
    return EfficacyConfig(default_source=default_source, targets=targets)
