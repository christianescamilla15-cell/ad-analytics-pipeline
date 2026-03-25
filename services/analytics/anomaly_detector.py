"""Spend anomaly detection using Z-score analysis."""

from __future__ import annotations

import math
from dataclasses import dataclass


@dataclass
class Anomaly:
    campaign_id: str
    campaign_name: str
    platform: str
    metric: str
    value: float
    mean: float
    std_dev: float
    z_score: float
    severity: str  # "warning" | "critical"
    message: str


class AnomalyDetector:
    """Z-score based anomaly detection on ad spend and performance."""

    def __init__(self, warning_threshold: float = 2.0, critical_threshold: float = 3.0):
        self.warning_threshold = warning_threshold
        self.critical_threshold = critical_threshold

    def detect(self, campaigns: list[dict], metric: str = "spend") -> list[Anomaly]:
        """Detect anomalies in the given metric across campaigns.

        Uses Modified Z-score based on the median and MAD (Median Absolute
        Deviation) which is robust against outliers inflating the standard
        deviation in small datasets.
        """
        values = [float(c.get(metric, 0)) for c in campaigns]
        if len(values) < 2:
            return []

        sorted_vals = sorted(values)
        n = len(sorted_vals)
        median = (
            sorted_vals[n // 2]
            if n % 2
            else (sorted_vals[n // 2 - 1] + sorted_vals[n // 2]) / 2
        )

        abs_devs = sorted(abs(v - median) for v in values)
        mad = (
            abs_devs[n // 2]
            if n % 2
            else (abs_devs[n // 2 - 1] + abs_devs[n // 2]) / 2
        )

        # 0.6745 is the 0.75th quantile of the standard normal distribution
        # This makes the modified z-score comparable to standard z-scores
        mean = sum(values) / n
        std_dev = mad * 1.4826 if mad > 0 else 0

        # Fallback to sample std dev when MAD is 0 (e.g. majority of values identical)
        if std_dev == 0:
            variance = sum((v - mean) ** 2 for v in values) / max(n - 1, 1)
            std_dev = math.sqrt(variance) if variance > 0 else 0

        if std_dev == 0:
            return []

        anomalies: list[Anomaly] = []
        for camp, val in zip(campaigns, values):
            z = (val - median) / std_dev
            abs_z = abs(z)

            if abs_z >= self.critical_threshold:
                severity = "critical"
            elif abs_z >= self.warning_threshold:
                severity = "warning"
            else:
                continue

            direction = "above" if z > 0 else "below"
            anomalies.append(
                Anomaly(
                    campaign_id=camp.get("id", ""),
                    campaign_name=camp.get("name", ""),
                    platform=camp.get("platform", "unknown"),
                    metric=metric,
                    value=val,
                    mean=round(mean, 2),
                    std_dev=round(std_dev, 2),
                    z_score=round(z, 2),
                    severity=severity,
                    message=(
                        f"{camp.get('name', '')} {metric} (${val:,.2f}) is "
                        f"{abs_z:.1f} std devs {direction} average (${mean:,.2f})"
                    ),
                )
            )

        return sorted(anomalies, key=lambda a: abs(a.z_score), reverse=True)

    def detect_all_metrics(self, campaigns: list[dict]) -> list[Anomaly]:
        """Run anomaly detection on multiple metrics."""
        all_anomalies: list[Anomaly] = []
        for metric in ("spend", "cpc", "ctr", "cost_per_conversion"):
            all_anomalies.extend(self.detect(campaigns, metric))
        return all_anomalies
