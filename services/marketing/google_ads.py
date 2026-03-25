"""Google Ads API client with demo mock."""

from __future__ import annotations


class GoogleAdsClient:
    """Google Ads API client with demo mock."""

    def __init__(self, developer_token: str = "", customer_id: str = ""):
        self.developer_token = developer_token
        self.customer_id = customer_id
        self._demo_mode = not developer_token

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
                "id": "gcamp_001",
                "name": "Search - Personal Injury Attorney",
                "status": "ENABLED",
                "type": "SEARCH",
                "budget_daily": 500.0,
                "spend": 12450.00,
                "impressions": 89000,
                "clicks": 6230,
                "ctr": 7.0,
                "cpc": 2.00,
                "conversions": 312,
                "cost_per_conversion": 39.90,
                "quality_score": 8,
                "impression_share": 0.72,
            },
            {
                "id": "gcamp_002",
                "name": "Display - Brand Remarketing",
                "status": "ENABLED",
                "type": "DISPLAY",
                "budget_daily": 200.0,
                "spend": 4890.50,
                "impressions": 456000,
                "clicks": 9120,
                "ctr": 2.0,
                "cpc": 0.54,
                "conversions": 178,
                "cost_per_conversion": 27.47,
                "quality_score": 7,
                "impression_share": 0.45,
            },
            {
                "id": "gcamp_003",
                "name": "Performance Max - All Channels",
                "status": "ENABLED",
                "type": "PERFORMANCE_MAX",
                "budget_daily": 350.0,
                "spend": 8920.75,
                "impressions": 312000,
                "clicks": 8424,
                "ctr": 2.7,
                "cpc": 1.06,
                "conversions": 267,
                "cost_per_conversion": 33.41,
                "quality_score": 0,
                "impression_share": 0.58,
            },
        ]

    def _mock_performance(self) -> dict:
        return {
            "campaign_id": "gcamp_001",
            "date_range": "2024-03-01 to 2024-03-31",
            "impressions": 89000,
            "clicks": 6230,
            "ctr": 7.0,
            "spend": 12450.00,
            "conversions": 312,
            "cost_per_conversion": 39.90,
            "search_impression_share": 0.72,
            "top_keywords": [
                {"keyword": "personal injury attorney", "clicks": 2100, "cpc": 3.45},
                {"keyword": "car accident lawyer", "clicks": 1890, "cpc": 2.90},
                {"keyword": "injury lawyer near me", "clicks": 1450, "cpc": 1.85},
            ],
        }

    def _mock_insights(self, period: str) -> dict:
        return {
            "period": period,
            "total_spend": 26261.25,
            "total_impressions": 857000,
            "total_clicks": 23774,
            "avg_ctr": 2.77,
            "avg_cpc": 1.10,
            "total_conversions": 757,
            "avg_cost_per_conversion": 34.69,
            "top_campaign": "Search - Personal Injury Attorney",
            "best_performing": {
                "metric": "cost_per_conversion",
                "campaign": "Display - Brand Remarketing",
                "value": 27.47,
            },
        }
