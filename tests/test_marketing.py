"""Tests for marketing API clients."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from services.marketing.meta_ads import MetaAdsClient
from services.marketing.google_ads import GoogleAdsClient
from services.marketing.ga4 import GA4Client
from services.marketing.unified_metrics import UnifiedMetrics


# ---- Meta Ads ----

def test_meta_demo_mode():
    client = MetaAdsClient()
    assert client._demo_mode is True


def test_meta_campaigns():
    client = MetaAdsClient()
    campaigns = client.get_campaigns()
    assert len(campaigns) == 4
    assert campaigns[0]["name"] == "Brand Awareness Q1"


def test_meta_campaign_fields():
    client = MetaAdsClient()
    camp = client.get_campaigns()[0]
    for field in ("id", "name", "status", "spend", "impressions", "clicks", "ctr", "cpc", "conversions"):
        assert field in camp


def test_meta_insights():
    client = MetaAdsClient()
    insights = client.get_account_insights()
    assert insights["total_spend"] > 0
    assert insights["total_conversions"] > 0


def test_meta_performance():
    client = MetaAdsClient()
    perf = client.get_ad_performance()
    assert "impressions" in perf
    assert perf["spend"] > 0


# ---- Google Ads ----

def test_google_demo_mode():
    client = GoogleAdsClient()
    assert client._demo_mode is True


def test_google_campaigns():
    client = GoogleAdsClient()
    campaigns = client.get_campaigns()
    assert len(campaigns) == 3
    assert campaigns[0]["type"] == "SEARCH"


def test_google_campaign_quality_score():
    client = GoogleAdsClient()
    camp = client.get_campaigns()[0]
    assert "quality_score" in camp
    assert camp["quality_score"] > 0


def test_google_insights():
    client = GoogleAdsClient()
    insights = client.get_account_insights()
    assert insights["total_spend"] > 0


# ---- GA4 ----

def test_ga4_overview():
    client = GA4Client()
    overview = client.get_overview()
    assert overview["sessions"] > 0
    assert "bounce_rate" in overview


def test_ga4_top_pages():
    client = GA4Client()
    pages = client.get_top_pages(5)
    assert len(pages) == 5
    assert pages[0]["page"] == "/"


def test_ga4_traffic_sources():
    client = GA4Client()
    sources = client.get_traffic_sources()
    assert len(sources) > 0
    assert sources[0]["source"] == "google"


def test_ga4_conversions():
    client = GA4Client()
    events = client.get_conversion_events()
    assert len(events) > 0
    assert events[0]["event"] == "form_submit"


# ---- Unified Metrics ----

def test_unified_overview():
    unified = UnifiedMetrics()
    data = unified.get_overview()
    assert data["total_ad_spend"] > 0
    assert data["total_conversions"] > 0
    assert "platforms" in data


def test_unified_blended_metrics():
    unified = UnifiedMetrics()
    data = unified.get_overview()
    assert data["blended_cpc"] > 0
    assert data["blended_ctr"] > 0


def test_unified_platform_comparison():
    unified = UnifiedMetrics()
    comp = unified.get_platform_comparison()
    assert len(comp) == 2
    assert comp[0]["platform"] == "Meta Ads"
    assert comp[1]["platform"] == "Google Ads"


def test_unified_spend_by_day():
    unified = UnifiedMetrics()
    trend = unified.get_spend_by_day(7)
    assert len(trend) == 7
    assert "date" in trend[0]
    assert "total" in trend[0]
