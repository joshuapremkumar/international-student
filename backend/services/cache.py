"""In-memory TTL cache for AnalysisResult objects.

Prevents redundant Tavily + Tinyfish API calls for repeated identical queries.
Cache is keyed by (normalized_degree, top_n) and expires after CACHE_TTL_SECONDS.
"""
import time
from typing import Optional
from backend.models.response import AnalysisResult

_store: dict[str, tuple[AnalysisResult, float]] = {}


def _normalize_key(degree: str, top_n: int) -> str:
    return f"{degree.strip().lower()}::{top_n}"


def get(degree: str, top_n: int) -> Optional[AnalysisResult]:
    """Return a cached AnalysisResult or None if expired / not present."""
    key = _normalize_key(degree, top_n)
    entry = _store.get(key)
    if entry is None:
        return None
    result, expires_at = entry
    if time.time() > expires_at:
        del _store[key]
        return None
    return result


def set(degree: str, top_n: int, value: AnalysisResult, ttl_seconds: int = 3600) -> None:
    """Store an AnalysisResult with a TTL."""
    key = _normalize_key(degree, top_n)
    _store[key] = (value, time.time() + ttl_seconds)


def clear() -> None:
    """Flush the entire cache (useful for testing)."""
    _store.clear()
