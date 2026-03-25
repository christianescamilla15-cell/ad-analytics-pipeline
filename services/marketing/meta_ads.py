"""Meta/Facebook Ads API client with demo mock."""

from __future__ import annotations


class MetaAdsClient:
    """Meta/Facebook Ads API client with demo mock."""

    def __init__(self, access_token: str = "", ad_account_id: str = ""):
        self.access_token = access_token
        self.ad_account_id = ad_account_id
        self._demo_mode = not access_token

    def get_campaigns(self, date_from: str = "", date_to: str = "") -> list[dict]:
        if self._demo_mode:
            return self._mock_campaigns()
        return []

    def get_ad_performance(self, campaign_id: str = "") -> dict:
        if self._demo_mode:
            return self._mock_performance()
        return {}

    def get_account_insights(self, period: str = "last_30d") -> dict:
        if self._demo_mode:
            return self._mock_insights(period)
        return {}

    # ------------------------------------------------------------------
    # Mock data
    # ------------------------------------------------------------------

    def _mock_campaigns(self) -> list[dict]:
        return [
            {
                "id": "camp_001",
                "name": "Brand Awareness Q1",
                "status": "ACTIVE",
                "objective": "BRAND_AWARENESS",
                "budget_daily": 150.0,
                "spend": 3245.50,
                "impressions": 245000,
                "clicks": 4890,
                "ctr": 2.0,
                "cpc": 0.66,
                "conversions": 89,
                "cost_per_conversion": 36.47,
            },
            {
                "id": "camp_002",
                "name": "Lead Gen - Personal Injury",
                "status": "ACTIVE",
                "objective": "LEAD_GENERATION",
                "budget_daily": 300.0,
                "spend": 7890.25,
                "impressions": 189000,
                "clicks": 5670,
                "ctr": 3.0,
                "cpc": 1.39,
                "conversions": 234,
                "cost_per_conversion": 33.72,
            },
            {
                "id": "camp_003",
                "name": "Retargeting Website Visitors",
                "status": "ACTIVE",
                "objective": "CONVERSIONS",
                "budget_daily": 100.0,
                "spend": 2100.00,
                "impressions": 98000,
                "clicks": 3920,
                "ctr": 4.0,
                "cpc": 0.54,
                "conversions": 156,
                "cost_per_conversion": 13.46,
            },
            {
                "id": "camp_004",
                "name": "Video Testimonials",
                "status": "PAUSED",
                "objective": "VIDEO_VIEWS",
                "budget_daily": 75.0,
                "spend": 1560.00,
                "impressions": 167000,
                "clicks": 2505,
                "ctr": 1.5,
                "cpc": 0.62,
                "conversions": 45,
                "cost_per_conversion": 34.67,
            },
        ]

    def _mock_performance(self) -> dict:
        return {
            "campaign_id": "camp_002",
            "date_range": "2024-03-01 to 2024-03-31",
            "impressions": 189000,
            "clicks": 5670,
            "ctr": 3.0,
            "spend": 7890.25,
            "conversions": 234,
            "cost_per_conversion": 33.72,
            "frequency": 2.4,
            "reach": 78750,
        }

    def _mock_insights(self, period: str) -> dict:
        return {
            "period": period,
            "total_spend": 14795.75,
            "total_impressions": 699000,
            "total_clicks": 16985,
            "avg_ctr": 2.43,
            "avg_cpc": 0.87,
            "total_conversions": 524,
            "avg_cost_per_conversion": 28.23,
            "top_campaign": "Lead Gen - Personal Injury",
            "best_performing": {
                "metric": "cost_per_conversion",
                "campaign": "Retargeting Website Visitors",
                "value": 13.46,
            },
        }
