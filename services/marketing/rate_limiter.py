"""API rate limiter for marketing platform APIs."""

import time
from collections import defaultdict


class RateLimiter:
    LIMITS = {
        "meta": {"requests_per_hour": 200, "requests_per_minute": 10},
        "google": {"requests_per_hour": 300, "requests_per_minute": 15},
        "ga4": {"requests_per_hour": 500, "requests_per_minute": 25},
    }

    def __init__(self):
        self._calls: dict[str, list[float]] = defaultdict(list)

    def check(self, platform: str) -> dict:
        now = time.time()
        limit = self.LIMITS.get(
            platform, {"requests_per_hour": 100, "requests_per_minute": 5}
        )

        # Clean old entries
        self._calls[platform] = [
            t for t in self._calls[platform] if now - t < 3600
        ]

        calls_last_hour = len(self._calls[platform])
        calls_last_minute = len(
            [t for t in self._calls[platform] if now - t < 60]
        )

        can_call = (
            calls_last_hour < limit["requests_per_hour"]
            and calls_last_minute < limit["requests_per_minute"]
        )

        return {
            "platform": platform,
            "can_call": can_call,
            "calls_last_hour": calls_last_hour,
            "calls_last_minute": calls_last_minute,
            "limit_per_hour": limit["requests_per_hour"],
            "limit_per_minute": limit["requests_per_minute"],
            "remaining_hour": max(
                0, limit["requests_per_hour"] - calls_last_hour
            ),
            "remaining_minute": max(
                0, limit["requests_per_minute"] - calls_last_minute
            ),
        }

    def record(self, platform: str):
        self._calls[platform].append(time.time())

    def get_all_status(self) -> list[dict]:
        return [self.check(p) for p in self.LIMITS]
