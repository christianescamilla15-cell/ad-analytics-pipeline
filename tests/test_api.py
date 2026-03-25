"""Tests for FastAPI endpoints."""

import sys
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from api.main import app

client = TestClient(app)


def test_health():
    r = client.get("/api/health")
    assert r.status_code == 200
    data = r.json()
    assert data["status"] == "ok"
    assert data["mode"] == "demo"


def test_overview():
    r = client.get("/api/overview")
    assert r.status_code == 200
    data = r.json()
    assert data["total_ad_spend"] > 0
    assert "platforms" in data


def test_platform_meta():
    r = client.get("/api/platforms/meta")
    assert r.status_code == 200
    data = r.json()
    assert len(data["campaigns"]) == 4


def test_platform_google():
    r = client.get("/api/platforms/google")
    assert r.status_code == 200
    data = r.json()
    assert len(data["campaigns"]) == 3


def test_platform_ga4():
    r = client.get("/api/platforms/ga4")
    assert r.status_code == 200
    data = r.json()
    assert data["overview"]["sessions"] > 0


def test_comparison():
    r = client.get("/api/comparison")
    assert r.status_code == 200
    data = r.json()
    assert len(data) == 2


def test_document_parse():
    r = client.post("/api/documents/parse", json={
        "text": "Invoice #INV-001\nDate: 01/01/2024\nTotal: $500.00"
    })
    assert r.status_code == 200
    data = r.json()
    assert data["invoice_number"] == "INV-001"
    assert data["total"] == 500.0


def test_document_list_empty():
    r = client.get("/api/documents")
    assert r.status_code == 200


def test_etl_run():
    r = client.post("/api/etl/run")
    assert r.status_code == 200
    data = r.json()
    assert data["status"] == "completed"


def test_etl_status():
    r = client.get("/api/etl/status")
    assert r.status_code == 200


def test_analytics_anomalies():
    r = client.get("/api/analytics/anomalies")
    assert r.status_code == 200
    assert isinstance(r.json(), list)


def test_analytics_spend_trend():
    r = client.get("/api/analytics/spend-trend")
    assert r.status_code == 200
    data = r.json()
    assert len(data) == 30


def test_s3_objects():
    r = client.get("/api/s3/objects")
    assert r.status_code == 200


def test_dashboard():
    r = client.get("/api/dashboard")
    assert r.status_code == 200
    data = r.json()
    assert "kpis" in data
    assert "charts" in data


# =========================================================================
# New endpoint tests — Tier 1
# =========================================================================


def test_scheduler_status():
    r = client.get("/api/scheduler/status")
    assert r.status_code == 200
    data = r.json()
    assert "jobs" in data
    assert len(data["jobs"]) >= 3


def test_scheduler_trigger():
    r = client.post("/api/scheduler/trigger/etl_full")
    assert r.status_code == 200
    data = r.json()
    assert data["status"] == "triggered"


def test_scheduler_trigger_not_found():
    r = client.post("/api/scheduler/trigger/nonexistent_job")
    assert r.status_code == 404


def test_alerts_get():
    r = client.get("/api/alerts")
    assert r.status_code == 200
    data = r.json()
    assert "alerts" in data


def test_alerts_acknowledge():
    # First get alerts to find an ID
    r = client.get("/api/alerts")
    alerts = r.json()["alerts"]
    if alerts:
        alert_id = alerts[0]["id"]
        r2 = client.post(f"/api/alerts/{alert_id}/acknowledge")
        assert r2.status_code == 200
        assert r2.json()["status"] == "acknowledged"


def test_alerts_acknowledge_not_found():
    r = client.post("/api/alerts/nonexistent/acknowledge")
    assert r.status_code == 404


def test_alerts_thresholds_get():
    r = client.get("/api/alerts/thresholds")
    assert r.status_code == 200
    data = r.json()
    assert "thresholds" in data
    assert "cpc_max" in data["thresholds"]


def test_alerts_thresholds_update():
    r = client.put("/api/alerts/thresholds", json={"cpc_max": 8.0})
    assert r.status_code == 200
    data = r.json()
    assert data["thresholds"]["cpc_max"] == 8.0


def test_analytics_roi():
    r = client.get("/api/analytics/roi")
    assert r.status_code == 200
    data = r.json()
    assert "campaigns" in data
    assert "overall_roi_percent" in data
    assert "total_spend" in data


def test_analytics_comparison():
    r = client.get("/api/analytics/comparison")
    assert r.status_code == 200
    data = r.json()
    assert "period" in data
    assert "metrics" in data
    assert "summary" in data


def test_executive_report():
    r = client.get("/api/reports/executive")
    assert r.status_code == 200
    data = r.json()
    assert data["title"] == "Ad Analytics Executive Report"
    assert "sections" in data
    assert len(data["sections"]) == 5


# =========================================================================
# New endpoint tests — Tier 2
# =========================================================================


def test_rate_limits():
    r = client.get("/api/rate-limits")
    assert r.status_code == 200
    data = r.json()
    assert "limits" in data
    assert len(data["limits"]) == 3


def test_cache_stats():
    r = client.get("/api/cache/stats")
    assert r.status_code == 200
    data = r.json()
    assert "hits" in data
    assert "misses" in data
    assert "hit_rate" in data


def test_webhook_receive():
    r = client.post("/api/webhooks/meta", json={
        "type": "campaign_updated",
        "payload": {"campaign_id": "123", "status": "paused"},
    })
    assert r.status_code == 200
    data = r.json()
    assert data["status"] == "received"
    assert data["platform"] == "meta"


def test_webhook_events():
    # First send a webhook
    client.post("/api/webhooks/google", json={
        "type": "budget_changed",
        "payload": {"amount": 500},
    })
    r = client.get("/api/webhooks/events")
    assert r.status_code == 200
    data = r.json()
    assert "events" in data
    assert len(data["events"]) >= 1


def test_budget_pacing():
    r = client.get("/api/analytics/budget-pacing")
    assert r.status_code == 200
    data = r.json()
    assert "pacing" in data
    assert len(data["pacing"]) == 7  # 4 meta + 3 google campaigns


def test_accounts_list():
    r = client.get("/api/accounts")
    assert r.status_code == 200
    data = r.json()
    assert "accounts" in data
    assert len(data["accounts"]) >= 3


def test_accounts_get():
    r = client.get("/api/accounts")
    accounts = r.json()["accounts"]
    first_id = accounts[0]["id"]
    r2 = client.get(f"/api/accounts/{first_id}")
    assert r2.status_code == 200
    assert r2.json()["id"] == first_id


def test_accounts_get_not_found():
    r = client.get("/api/accounts/nonexistent")
    assert r.status_code == 404


def test_accounts_create():
    r = client.post("/api/accounts", json={
        "name": "New Agency Client",
        "meta_account_id": "act_new",
        "google_account_id": "gact_new",
    })
    assert r.status_code == 200
    data = r.json()
    assert data["name"] == "New Agency Client"
