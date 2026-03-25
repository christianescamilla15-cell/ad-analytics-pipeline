"""Tests for the DataCache service."""

import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from services.cache import DataCache


def test_set_and_get():
    cache = DataCache(default_ttl=60)
    cache.set("key1", {"data": "hello"})
    result = cache.get("key1")
    assert result == {"data": "hello"}


def test_get_miss():
    cache = DataCache(default_ttl=60)
    result = cache.get("nonexistent")
    assert result is None


def test_ttl_expiry():
    cache = DataCache(default_ttl=1)
    cache.set("expire_me", "value", ttl=1)
    assert cache.get("expire_me") == "value"
    time.sleep(1.1)
    assert cache.get("expire_me") is None


def test_invalidate():
    cache = DataCache(default_ttl=60)
    cache.set("key", "value")
    cache.invalidate("key")
    assert cache.get("key") is None


def test_clear():
    cache = DataCache(default_ttl=60)
    cache.set("a", 1)
    cache.set("b", 2)
    cache.clear()
    assert cache.get("a") is None
    assert cache.get("b") is None


def test_stats():
    cache = DataCache(default_ttl=60)
    cache.set("x", 10)
    cache.get("x")  # hit
    cache.get("x")  # hit
    cache.get("y")  # miss
    stats = cache.get_stats()
    assert stats["hits"] == 2
    assert stats["misses"] == 1
    assert stats["active_entries"] == 1
    assert stats["hit_rate"] == 66.7
