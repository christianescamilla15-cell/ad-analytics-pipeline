"""Report generation from analytics data."""

from __future__ import annotations

from datetime import datetime, timezone

from services.marketing.unified_metrics import UnifiedMetrics


class ReportGenerator:
    """Generate analytics reports."""

    def __init__(self, unified: UnifiedMetrics | None = None):
        self.unified = unified or UnifiedMetrics()

    def executive_summary(self) -> dict:
        """High-level executive summary report."""
        overview = self.unified.get_overview()
        comparison = self.unified.get_platform_comparison()

        best_platform = min(comparison, key=lambda p: p["cost_per_conversion"])

        return {
            "title": "Ad Performance Executive Summary",
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "period": "Last 30 Days",
            "kpis": {
                "total_spend": overview["total_ad_spend"],
                "total_conversions": overview["total_conversions"],
                "blended_cpc": overview["blended_cpc"],
                "blended_ctr": overview["blended_ctr"],
                "website_sessions": overview["website_sessions"],
            },
            "platform_comparison": comparison,
            "recommendation": (
                f"{best_platform['platform']} has the lowest cost per conversion "
                f"(${best_platform['cost_per_conversion']:.2f}). Consider shifting "
                f"more budget to this platform."
            ),
        }

    def campaign_report(self) -> dict:
        """Detailed campaign-level report."""
        meta_campaigns = self.unified.meta.get_campaigns()
        google_campaigns = self.unified.google.get_campaigns()

        all_campaigns = [
            {**c, "platform": "Meta"} for c in meta_campaigns
        ] + [
            {**c, "platform": "Google"} for c in google_campaigns
        ]

        return {
            "title": "Campaign Performance Report",
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "total_campaigns": len(all_campaigns),
            "active": sum(
                1
                for c in all_campaigns
                if c.get("status") in ("ACTIVE", "ENABLED")
            ),
            "campaigns": sorted(
                all_campaigns, key=lambda c: c.get("spend", 0), reverse=True
            ),
        }
