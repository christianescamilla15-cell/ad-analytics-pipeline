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
