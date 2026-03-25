"""Data extractors -- pull raw data from marketing APIs."""

from __future__ import annotations

from services.marketing.meta_ads import MetaAdsClient
from services.marketing.google_ads import GoogleAdsClient
from services.marketing.ga4 import GA4Client


class MarketingExtractor:
    """Extract raw data from marketing platform APIs."""

    def __init__(
        self,
        meta: MetaAdsClient | None = None,
        google: GoogleAdsClient | None = None,
        ga4: GA4Client | None = None,
    ):
        self.meta = meta or MetaAdsClient()
        self.google = google or GoogleAdsClient()
        self.ga4 = ga4 or GA4Client()

    def extract_meta(self) -> dict:
        return {
            "platform": "meta",
            "campaigns": self.meta.get_campaigns(),
            "insights": self.meta.get_account_insights(),
        }

    def extract_google(self) -> dict:
        return {
            "platform": "google",
            "campaigns": self.google.get_campaigns(),
            "insights": self.google.get_account_insights(),
        }

    def extract_ga4(self) -> dict:
        return {
            "platform": "ga4",
            "overview": self.ga4.get_overview(),
            "top_pages": self.ga4.get_top_pages(),
            "traffic_sources": self.ga4.get_traffic_sources(),
        }

    def extract_all(self, sources: list[str] | None = None) -> dict:
        sources = sources or ["meta", "google", "ga4"]
        data: dict = {}
        if "meta" in sources:
            data["meta"] = self.extract_meta()
        if "google" in sources:
            data["google"] = self.extract_google()
        if "ga4" in sources:
            data["ga4"] = self.extract_ga4()
        return data
