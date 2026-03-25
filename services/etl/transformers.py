"""Data transformers -- clean and normalize raw marketing data."""

from __future__ import annotations


class MarketingTransformer:
    """Transform raw marketing data into a clean, unified format."""

    def transform(self, raw_data: dict) -> dict:
        result: dict = {"campaigns": [], "summary": {}}

        all_campaigns: list[dict] = []

        if "meta" in raw_data:
            for c in raw_data["meta"].get("campaigns", []):
                all_campaigns.append(self._normalize_campaign(c, "meta"))

        if "google" in raw_data:
            for c in raw_data["google"].get("campaigns", []):
                all_campaigns.append(self._normalize_campaign(c, "google"))

        result["campaigns"] = all_campaigns
        result["summary"] = self._compute_summary(all_campaigns, raw_data)
        return result

    def _normalize_campaign(self, campaign: dict, platform: str) -> dict:
        return {
            "id": campaign.get("id", ""),
            "name": campaign.get("name", ""),
            "platform": platform,
            "status": campaign.get("status", "UNKNOWN").upper(),
            "spend": round(float(campaign.get("spend", 0)), 2),
            "impressions": int(campaign.get("impressions", 0)),
            "clicks": int(campaign.get("clicks", 0)),
            "ctr": round(float(campaign.get("ctr", 0)), 2),
            "cpc": round(float(campaign.get("cpc", 0)), 2),
            "conversions": int(campaign.get("conversions", 0)),
            "cost_per_conversion": round(
                float(campaign.get("cost_per_conversion", 0)), 2
            ),
        }

    def _compute_summary(self, campaigns: list[dict], raw_data: dict) -> dict:
        total_spend = sum(c["spend"] for c in campaigns)
        total_clicks = sum(c["clicks"] for c in campaigns)
        total_impressions = sum(c["impressions"] for c in campaigns)
        total_conversions = sum(c["conversions"] for c in campaigns)

        ga4_sessions = 0
        if "ga4" in raw_data:
            ga4_sessions = raw_data["ga4"].get("overview", {}).get("sessions", 0)

        return {
            "total_campaigns": len(campaigns),
            "total_spend": round(total_spend, 2),
            "total_clicks": total_clicks,
            "total_impressions": total_impressions,
            "total_conversions": total_conversions,
            "blended_cpc": round(total_spend / total_clicks, 2) if total_clicks else 0,
            "blended_ctr": (
                round(total_clicks / total_impressions * 100, 2)
                if total_impressions
                else 0
            ),
            "website_sessions": ga4_sessions,
        }
