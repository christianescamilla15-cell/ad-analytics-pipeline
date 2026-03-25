"""Unified metrics across all marketing platforms."""

from __future__ import annotations

import random
from datetime import datetime, timedelta

from .meta_ads import MetaAdsClient
from .google_ads import GoogleAdsClient
from .ga4 import GA4Client


class UnifiedMetrics:
    """Combine Meta + Google + GA4 into a single view."""

    def __init__(
        self,
        meta: MetaAdsClient | None = None,
        google: GoogleAdsClient | None = None,
        ga4: GA4Client | None = None,
    ):
        self.meta = meta or MetaAdsClient()
        self.google = google or GoogleAdsClient()
        self.ga4 = ga4 or GA4Client()

    def get_overview(self) -> dict:
        meta_insights = self.meta.get_account_insights()
        google_insights = self.google.get_account_insights()
        ga4_data = self.ga4.get_overview()

        total_spend = meta_insights["total_spend"] + google_insights["total_spend"]
        total_clicks = meta_insights["total_clicks"] + google_insights["total_clicks"]
        total_impressions = (
            meta_insights["total_impressions"] + google_insights["total_impressions"]
        )
        total_conversions = (
            meta_insights["total_conversions"] + google_insights["total_conversions"]
        )

        blended_cpc = total_spend / total_clicks if total_clicks else 0
        blended_ctr = (total_clicks / total_impressions * 100) if total_impressions else 0

        return {
            "total_ad_spend": round(total_spend, 2),
            "total_conversions": total_conversions,
            "blended_cpc": round(blended_cpc, 2),
            "blended_ctr": round(blended_ctr, 2),
            "website_sessions": ga4_data["sessions"],
            "platforms": {
                "meta": meta_insights,
                "google": google_insights,
                "ga4": ga4_data,
            },
        }

    def get_platform_comparison(self) -> list[dict]:
        """Compare performance across platforms."""
        meta = self.meta.get_account_insights()
        google = self.google.get_account_insights()

        return [
            {
                "platform": "Meta Ads",
                "spend": meta["total_spend"],
                "conversions": meta["total_conversions"],
                "cpc": meta["avg_cpc"],
                "ctr": meta["avg_ctr"],
                "cost_per_conversion": meta["avg_cost_per_conversion"],
            },
            {
                "platform": "Google Ads",
                "spend": google["total_spend"],
                "conversions": google["total_conversions"],
                "cpc": google["avg_cpc"],
                "ctr": google["avg_ctr"],
                "cost_per_conversion": google["avg_cost_per_conversion"],
            },
        ]

    def get_spend_by_day(self, days: int = 30) -> list[dict]:
        """Daily spend across all platforms (mock)."""
        rng = random.Random(42)
        result = []
        base_date = datetime(2024, 3, 31)
        for i in range(days):
            d = base_date - timedelta(days=days - 1 - i)
            meta_spend = round(rng.uniform(350, 650), 2)
            google_spend = round(rng.uniform(700, 1100), 2)
            result.append(
                {
                    "date": d.strftime("%Y-%m-%d"),
                    "meta": meta_spend,
                    "google": google_spend,
                    "total": round(meta_spend + google_spend, 2),
                }
            )
        return result
