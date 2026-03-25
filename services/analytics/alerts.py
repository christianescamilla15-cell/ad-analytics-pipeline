"""Spend alert system with configurable thresholds."""

from dataclasses import dataclass, field
from datetime import datetime, timezone


@dataclass
class Alert:
    id: str
    severity: str  # info, warning, critical
    type: str  # spend_anomaly, budget_exceeded, performance_drop, roi_negative
    message: str
    campaign: str = ""
    platform: str = ""
    value: float = 0.0
    threshold: float = 0.0
    created_at: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )
    acknowledged: bool = False


class AlertManager:
    def __init__(self):
        self._alerts: list[Alert] = []
        self._thresholds = {
            "cpc_max": 5.0,
            "ctr_min": 0.5,
            "daily_spend_max": 1000.0,
            "cost_per_conversion_max": 50.0,
            "budget_utilization_max": 0.9,
        }

    def check_campaigns(self, campaigns: list[dict]) -> list[Alert]:
        """Scan campaigns and generate alerts."""
        new_alerts = []
        for c in campaigns:
            # CPC too high
            if c.get("cpc", 0) > self._thresholds["cpc_max"]:
                alert = Alert(
                    id=f"alert-{len(self._alerts) + len(new_alerts)}",
                    severity="warning",
                    type="spend_anomaly",
                    message=(
                        f"{c['name']}: CPC ${c['cpc']:.2f} exceeds "
                        f"threshold ${self._thresholds['cpc_max']:.2f}"
                    ),
                    campaign=c.get("name", ""),
                    platform=c.get("platform", ""),
                    value=c["cpc"],
                    threshold=self._thresholds["cpc_max"],
                )
                new_alerts.append(alert)

            # CTR too low
            if c.get("ctr", 100) < self._thresholds["ctr_min"]:
                alert = Alert(
                    id=f"alert-{len(self._alerts) + len(new_alerts)}",
                    severity="warning",
                    type="performance_drop",
                    message=(
                        f"{c['name']}: CTR {c['ctr']:.1f}% below "
                        f"minimum {self._thresholds['ctr_min']:.1f}%"
                    ),
                    campaign=c.get("name", ""),
                    platform=c.get("platform", ""),
                    value=c["ctr"],
                    threshold=self._thresholds["ctr_min"],
                )
                new_alerts.append(alert)

            # Cost per conversion too high
            if c.get("cost_per_conversion", 0) > self._thresholds[
                "cost_per_conversion_max"
            ]:
                alert = Alert(
                    id=f"alert-{len(self._alerts) + len(new_alerts)}",
                    severity="critical",
                    type="spend_anomaly",
                    message=(
                        f"{c['name']}: Cost/conversion "
                        f"${c['cost_per_conversion']:.2f} exceeds "
                        f"${self._thresholds['cost_per_conversion_max']:.2f}"
                    ),
                    campaign=c.get("name", ""),
                    platform=c.get("platform", ""),
                    value=c["cost_per_conversion"],
                    threshold=self._thresholds["cost_per_conversion_max"],
                )
                new_alerts.append(alert)

        self._alerts.extend(new_alerts)
        return new_alerts

    def get_alerts(
        self, severity: str = None, acknowledged: bool = None
    ) -> list[dict]:
        filtered = self._alerts
        if severity:
            filtered = [a for a in filtered if a.severity == severity]
        if acknowledged is not None:
            filtered = [a for a in filtered if a.acknowledged == acknowledged]
        return [
            {
                "id": a.id,
                "severity": a.severity,
                "type": a.type,
                "message": a.message,
                "campaign": a.campaign,
                "platform": a.platform,
                "value": a.value,
                "threshold": a.threshold,
                "created_at": a.created_at,
                "acknowledged": a.acknowledged,
            }
            for a in filtered
        ]

    def acknowledge(self, alert_id: str) -> bool:
        for a in self._alerts:
            if a.id == alert_id:
                a.acknowledged = True
                return True
        return False

    def get_thresholds(self) -> dict:
        return self._thresholds.copy()

    def update_threshold(self, key: str, value: float) -> bool:
        if key in self._thresholds:
            self._thresholds[key] = value
            return True
        return False
