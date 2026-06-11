"""Polite, cached HTTP client for the RCSB / UniProt APIs.

Caps concurrency at the caller's discretion, retries with exponential backoff,
and caches every response on disk so re-runs are offline-friendly (a hard
requirement on Gadi compute nodes, which have no internet).
"""

from __future__ import annotations

import hashlib
import json
import logging
import time
from pathlib import Path
from typing import Any

import requests

from .paths import CACHE_DIR, ensure_dir

log = logging.getLogger("pharmpipe.http")

USER_AGENT = "pharmpipe/0.1 (PDB ligand catalogue; mailto:u7457676@anu.edu.au)"

_SESSION: requests.Session | None = None


def session() -> requests.Session:
    global _SESSION
    if _SESSION is None:
        s = requests.Session()
        s.headers.update({"User-Agent": USER_AGENT})
        _SESSION = s
    return _SESSION


def _cache_path(category: str, key: str, suffix: str) -> Path:
    digest = hashlib.sha1(key.encode("utf-8")).hexdigest()[:16]
    return ensure_dir(CACHE_DIR / category) / f"{digest}{suffix}"


class HttpConfig:
    """Retry/backoff knobs, populated from config.SearchOptions."""

    def __init__(self, retries: int = 4, backoff_seconds: float = 2.0, timeout: float = 60.0):
        self.retries = retries
        self.backoff_seconds = backoff_seconds
        self.timeout = timeout


def _request(method: str, url: str, cfg: HttpConfig, **kwargs: Any) -> requests.Response:
    last_exc: Exception | None = None
    for attempt in range(cfg.retries):
        try:
            resp = session().request(method, url, timeout=cfg.timeout, **kwargs)
            # 404 is a definitive "not found" — do not retry, let caller decide.
            if resp.status_code == 404:
                return resp
            if resp.status_code in (429, 500, 502, 503, 504):
                raise requests.HTTPError(f"{resp.status_code} for {url}")
            resp.raise_for_status()
            return resp
        except (requests.RequestException, requests.HTTPError) as exc:  # noqa: PERF203
            last_exc = exc
            wait = cfg.backoff_seconds * (2**attempt)
            log.warning("%s %s failed (attempt %d/%d): %s; retrying in %.1fs",
                        method, url, attempt + 1, cfg.retries, exc, wait)
            time.sleep(wait)
    raise RuntimeError(f"{method} {url} failed after {cfg.retries} attempts") from last_exc


def get_json(url: str, cfg: HttpConfig, *, category: str, cache_key: str | None = None,
             allow_404: bool = False) -> Any | None:
    """Cached GET returning parsed JSON. Returns None on 404 if allow_404."""
    key = cache_key or url
    path = _cache_path(category, key, ".json")
    if path.exists():
        return json.loads(path.read_text(encoding="utf-8"))
    resp = _request("GET", url, cfg)
    if resp.status_code == 404:
        if allow_404:
            return None
        resp.raise_for_status()
    data = resp.json()
    path.write_text(json.dumps(data), encoding="utf-8")
    return data


def post_json(url: str, payload: dict, cfg: HttpConfig, *, category: str) -> Any | None:
    """Cached POST (JSON body) returning parsed JSON. None on 204/empty."""
    key = url + "\n" + json.dumps(payload, sort_keys=True)
    path = _cache_path(category, key, ".json")
    if path.exists():
        text = path.read_text(encoding="utf-8")
        return json.loads(text) if text else None
    resp = _request("POST", url, cfg, json=payload)
    if resp.status_code == 204 or not resp.text.strip():
        path.write_text("", encoding="utf-8")
        return None
    data = resp.json()
    path.write_text(json.dumps(data), encoding="utf-8")
    return data


def get_text(url: str, cfg: HttpConfig, *, category: str, cache_key: str | None = None,
             allow_404: bool = False) -> str | None:
    """Cached GET returning text (used for mmCIF / CCD files)."""
    key = cache_key or url
    path = _cache_path(category, key, ".txt")
    if path.exists():
        return path.read_text(encoding="utf-8")
    resp = _request("GET", url, cfg)
    if resp.status_code == 404:
        if allow_404:
            return None
        resp.raise_for_status()
    path.write_text(resp.text, encoding="utf-8")
    return resp.text
