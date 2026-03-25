"""Google Analytics 4 client with demo mock."""

from __future__ import annotations


class GA4Client:
    """Google Analytics 4 Data API client with demo mock."""

    def __init__(self, property_id: str = ""):
        self.property_id = property_id
        self._demo_mode = not property_id

    def get_overview(self, period: str = "last_30d") -> dict:
        if self._demo_mode:
            return self._mock_overview(period)
        return {}

    def get_top_pages(self, limit: int = 10) -> list[dict]:
        if self._demo_mode:
            return self._mock_top_pages()[:limit]
        return []

    def get_traffic_sources(self) -> list[dict]:
        if self._demo_mode:
            return self._mock_traffic_sources()
        return []

    def get_conversion_events(self) -> list[dict]:
        if self._demo_mode:
            return self._mock_conversions()
        return []

    # ------------------------------------------------------------------
    # Mock data
    # ------------------------------------------------------------------

    def _mock_overview(self, period: str) -> dict:
        return {
            "period": period,
            "sessions": 34520,
            "page_views": 98450,
            "users": 28100,
            "new_users": 19870,
            "bounce_rate": 42.3,
            "avg_session_duration": 185.4,
            "pages_per_session": 2.85,
            "engagement_rate": 57.7,
        }

    def _mock_top_pages(self) -> list[dict]:
        return [
            {"page": "/", "views": 24500, "avg_time": 45.2},
            {"page": "/services/personal-injury", "views": 12300, "avg_time": 120.5},
            {"page": "/contact", "views": 8900, "avg_time": 65.3},
            {"page": "/about", "views": 7200, "avg_time": 90.1},
            {"page": "/blog/car-accident-guide", "views": 6800, "avg_time": 210.7},
            {"page": "/testimonials", "views": 5400, "avg_time": 95.6},
            {"page": "/services/workers-comp", "views": 4900, "avg_time": 105.2},
            {"page": "/faq", "views": 4100, "avg_time": 150.3},
            {"page": "/blog/slip-and-fall", "views": 3800, "avg_time": 190.4},
            {"page": "/free-consultation", "views": 3200, "avg_time": 55.8},
        ]

    def _mock_traffic_sources(self) -> list[dict]:
        return [
            {"source": "google", "medium": "cpc", "sessions": 12400, "conversions": 620},
            {"source": "facebook", "medium": "cpc", "sessions": 8900, "conversions": 445},
            {"source": "google", "medium": "organic", "sessions": 6800, "conversions": 204},
            {"source": "(direct)", "medium": "(none)", "sessions": 3200, "conversions": 96},
            {"source": "bing", "medium": "organic", "sessions": 1800, "conversions": 54},
            {"source": "referral", "medium": "avvo.com", "sessions": 1420, "conversions": 71},
        ]

    def _mock_conversions(self) -> list[dict]:
        return [
            {"event": "form_submit", "count": 1245, "value": 0.0},
            {"event": "phone_call", "count": 890, "value": 0.0},
            {"event": "chat_started", "count": 567, "value": 0.0},
            {"event": "page_view_contact", "count": 8900, "value": 0.0},
            {"event": "consultation_booked", "count": 423, "value": 0.0},
        ]
