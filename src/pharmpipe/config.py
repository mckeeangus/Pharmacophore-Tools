"""Load and validate config/targets.yaml into typed objects."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

import yaml

from .util.http import HttpConfig


@dataclass
class Surrogate:
    name: str
    uniprot: str
    kind: str = "surrogate"


@dataclass
class Target:
    name: str
    slug: str
    genes: list[str] = field(default_factory=list)
    organism: str = "human"
    uniprot_hint: list[str] = field(default_factory=list)
    surrogates: list[Surrogate] = field(default_factory=list)
    notes: str = ""
    # Per-target curation overrides (HET codes), take precedence over defaults.
    keep_extra: list[str] = field(default_factory=list)
    exclude_extra: list[str] = field(default_factory=list)


@dataclass
class SearchOptions:
    organism_policy: str = "human_preferred"   # human_preferred | human_only | any
    human_taxonomy_id: int = 9606
    include_surrogates: bool = True
    extract_mode: str = "all_instances"        # all_instances | representative
    max_parallel_downloads: int = 4
    request_retries: int = 4
    request_backoff_seconds: float = 2.0
    cache_offline_ok: bool = True

    def http(self) -> HttpConfig:
        return HttpConfig(retries=self.request_retries,
                          backoff_seconds=self.request_backoff_seconds)


@dataclass
class Config:
    search: SearchOptions
    targets: list[Target]


def load_config(path: str | Path) -> Config:
    raw = yaml.safe_load(Path(path).read_text(encoding="utf-8"))
    search = SearchOptions(**(raw.get("search") or {}))
    targets: list[Target] = []
    for t in raw.get("targets", []):
        surrogates = [Surrogate(**s) for s in (t.get("surrogates") or [])]
        targets.append(Target(
            name=t["name"],
            slug=t["slug"],
            genes=t.get("genes") or [],
            organism=t.get("organism", "human"),
            uniprot_hint=t.get("uniprot_hint") or [],
            surrogates=surrogates,
            notes=t.get("notes", ""),
            keep_extra=t.get("keep_extra") or [],
            exclude_extra=t.get("exclude_extra") or [],
        ))
    return Config(search=search, targets=targets)
