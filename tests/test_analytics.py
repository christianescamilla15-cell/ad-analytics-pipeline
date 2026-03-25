"""Tests for analytics services."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from services.analytics.anomaly_detector import AnomalyDetector
from services.analytics.dashboard import DashboardService
from services.analytics.reports import ReportGenerator


# ---- Anomaly Detector ----

def test_anomaly_no_data():
    det = AnomalyDetector()
    assert det.detect([], "spend") == []


def test_anomaly_uniform_data():
    det = AnomalyDetector()
    campaigns = [{"id": str(i), "name": f"c{i}", "spend": 100.0} for i in range(5)]
    assert det.detect(campaigns, "spend") == []


def test_anomaly_detects_outlier():
    det = AnomalyDetector()
    campaigns = [
        {"id": "1", "name": "Normal A", "spend": 100.0},
        {"id": "2", "name": "Normal B", "spend": 105.0},
        {"id": "3", "name": "Normal C", "spend": 98.0},
        {"id": "4", "name": "Normal D", "spend": 102.0},
        {"id": "5", "name": "Outlier", "spend": 500.0},
    ]
    anomalies = det.detect(campaigns, "spend")
    assert len(anomalies) > 0
    assert anomalies[0].campaign_name == "Outlier"
    assert anomalies[0].severity in ("warning", "critical")


def test_anomaly_z_score_sign():
    det = AnomalyDetector()
    campaigns = [
        {"id": "1", "name": "High", "spend": 1000.0},
        {"id": "2", "name": "Low A", "spend": 50.0},
        {"id": "3", "name": "Low B", "spend": 55.0},
        {"id": "4", "name": "Low C", "spend": 48.0},
        {"id": "5", "name": "Low D", "spend": 52.0},
    ]
    anomalies = det.detect(campaigns, "spend")
    high = [a for a in anomalies if a.campaign_name == "High"]
    assert len(high) > 0
    assert high[0].z_score > 0


def test_anomaly_detect_all_metrics():
    det = AnomalyDetector()
    campaigns = [
        {"id": "1", "name": "A", "spend": 100, "cpc": 1.0, "ctr": 2.0, "cost_per_conversion": 30},
        {"id": "2", "name": "B", "spend": 100, "cpc": 1.0, "ctr": 2.0, "cost_per_conversion": 30},
        {"id": "3", "name": "C", "spend": 100, "cpc": 1.0, "ctr": 2.0, "cost_per_conversion": 30},
        {"id": "4", "name": "Outlier", "spend": 900, "cpc": 10.0, "ctr": 50.0, "cost_per_conversion": 300},
    ]
    anomalies = det.detect_all_metrics(campaigns)
    assert len(anomalies) > 0


# ---- Dashboard ----

def test_dashboard_kpis():
    svc = DashboardService()
    kpis = svc.get_kpis()
    assert kpis["total_spend"] > 0
    assert kpis["total_conversions"] > 0


def test_dashboard_charts():
    svc = DashboardService()
    charts = svc.get_charts()
    assert "platform_comparison" in charts
    assert "spend_trend" in charts
    assert len(charts["spend_trend"]) == 30


def test_dashboard_anomalies():
    svc = DashboardService()
    anomalies = svc.get_anomalies()
    assert isinstance(anomalies, list)


def test_dashboard_full():
    svc = DashboardService()
    data = svc.get_full_dashboard()
    assert "kpis" in data
    assert "charts" in data
    assert "anomalies" in data
    assert "etl_status" in data


# ---- Reports ----

def test_executive_summary():
    gen = ReportGenerator()
    report = gen.executive_summary()
    assert "kpis" in report
    assert report["kpis"]["total_spend"] > 0
    assert "recommendation" in report


def test_campaign_report():
    gen = ReportGenerator()
    report = gen.campaign_report()
    assert report["total_campaigns"] == 7
    assert report["active"] > 0
