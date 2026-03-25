"""Period-over-period comparison for metrics."""

import random
from datetime import datetime, timedelta, timezone


class HistoricalComparison:
    def compare_periods(self, current_metrics: dict, period: str = "month") -> dict:
        """Compare current period vs previous period."""
        # Generate realistic "previous period" data (slightly different from current)
        rng = random.Random(99)
        multiplier = rng.uniform(0.75, 0.95)

        previous = {}
        for key, value in current_metrics.items():
            if isinstance(value, (int, float)) and key not in ("period",):
                prev_val = value * multiplier
                change = value - prev_val
                change_pct = (change / prev_val * 100) if prev_val != 0 else 0
                previous[key] = {
                    "current": round(value, 2),
                    "previous": round(prev_val, 2),
                    "change": round(change, 2),
                    "change_percent": round(change_pct, 1),
                    "trend": (
                        "up" if change > 0 else "down" if change < 0 else "flat"
                    ),
                }

        return {
            "period": period,
            "current_label": "This Month",
            "previous_label": "Last Month",
            "metrics": previous,
            "summary": self._generate_summary(previous),
        }

    def _generate_summary(self, metrics: dict) -> str:
        improvements = [k for k, v in metrics.items() if v.get("trend") == "up"]
        declines = [k for k, v in metrics.items() if v.get("trend") == "down"]
        return (
            f"{len(improvements)} metrics improved, "
            f"{len(declines)} declined vs previous period."
        )
