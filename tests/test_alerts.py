"""Tests for the AlertManager service."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from services.analytics.alerts import AlertManager


def _sample_campaigns():
    return [
        {"name": "High CPC Campaign", "cpc": 6.50, "ctr": 3.0, "cost_per_conversion": 40.0, "platform": "meta"},
        {"name": "Low CTR Campaign", "cpc": 1.00, "ctr": 0.2, "cost_per_conversion": 20.0, "platform": "google"},
        {"name": "Good Campaign", "cpc": 1.50, "ctr": 3.5, "cost_per_conversion": 25.0, "platform": "meta"},
        {"name": "Expensive Conversions", "cpc": 2.00, "ctr": 2.0, "cost_per_conversion": 75.0, "platform": "google"},
    ]


def test_check_campaigns_generates_alerts():
    mgr = AlertManager()
    alerts = mgr.check_campaigns(_sample_campaigns())
    assert len(alerts) > 0


def test_cpc_alert_generated():
    mgr = AlertManager()
    alerts = mgr.check_campaigns(_sample_campaigns())
    cpc_alerts = [a for a in alerts if a.campaign == "High CPC Campaign" and a.type == "spend_anomaly"]
    assert len(cpc_alerts) >= 1
    assert cpc_alerts[0].value == 6.50


def test_ctr_alert_generated():
    mgr = AlertManager()
    alerts = mgr.check_campaigns(_sample_campaigns())
    ctr_alerts = [a for a in alerts if a.campaign == "Low CTR Campaign" and a.type == "performance_drop"]
    assert len(ctr_alerts) >= 1


def test_cost_per_conversion_alert():
    mgr = AlertManager()
    alerts = mgr.check_campaigns(_sample_campaigns())
    conv_alerts = [a for a in alerts if a.campaign == "Expensive Conversions" and a.severity == "critical"]
    assert len(conv_alerts) >= 1


def test_good_campaign_no_alert():
    mgr = AlertManager()
    alerts = mgr.check_campaigns(_sample_campaigns())
    good = [a for a in alerts if a.campaign == "Good Campaign"]
    assert len(good) == 0


def test_get_alerts_filter_severity():
    mgr = AlertManager()
    mgr.check_campaigns(_sample_campaigns())
    critical = mgr.get_alerts(severity="critical")
    assert all(a["severity"] == "critical" for a in critical)


def test_acknowledge_alert():
    mgr = AlertManager()
    mgr.check_campaigns(_sample_campaigns())
    alerts = mgr.get_alerts()
    assert len(alerts) > 0
    alert_id = alerts[0]["id"]
    assert mgr.acknowledge(alert_id) is True
    acked = mgr.get_alerts(acknowledged=True)
    assert any(a["id"] == alert_id for a in acked)


def test_thresholds_crud():
    mgr = AlertManager()
    thresholds = mgr.get_thresholds()
    assert "cpc_max" in thresholds
    assert mgr.update_threshold("cpc_max", 10.0) is True
    assert mgr.get_thresholds()["cpc_max"] == 10.0
    assert mgr.update_threshold("nonexistent", 1.0) is False
