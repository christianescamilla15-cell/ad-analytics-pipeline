"""In-memory cache with TTL for API responses."""

import time
from dataclasses import dataclass, field
from typing import Any


@dataclass
class CacheEntry:
    data: Any
    expires_at: float
    hits: int = 0


class DataCache:
    def __init__(self, default_ttl: int = 300):
        self._cache: dict[str, CacheEntry] = {}
        self.default_ttl = default_ttl
        self.total_hits = 0
        self.total_misses = 0

    def get(self, key: str) -> Any:
        entry = self._cache.get(key)
        if entry and time.time() < entry.expires_at:
            entry.hits += 1
            self.total_hits += 1
            return entry.data
        self.total_misses += 1
        return None

    def set(self, key: str, data: Any, ttl: int = None):
        self._cache[key] = CacheEntry(
            data=data, expires_at=time.time() + (ttl or self.default_ttl)
        )

    def invalidate(self, key: str):
        self._cache.pop(key, None)

    def clear(self):
        self._cache.clear()

    def get_stats(self) -> dict:
        now = time.time()
        active = sum(1 for e in self._cache.values() if now < e.expires_at)
        return {
            "active_entries": active,
            "total_entries": len(self._cache),
            "hits": self.total_hits,
            "misses": self.total_misses,
            "hit_rate": round(
                self.total_hits
                / max(self.total_hits + self.total_misses, 1)
                * 100,
                1,
            ),
        }
