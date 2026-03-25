"""Dashboard data aggregation service."""

from __future__ import annotations

from services.marketing.unified_metrics import UnifiedMetrics
from services.analytics.anomaly_detector import AnomalyDetector
from services.etl.pipeline import ETLPipeline


class DashboardService:
    """Aggregate data for the frontend dashboard."""

    def __init__(
        self,
        unified: UnifiedMetrics | None = None,
        detector: AnomalyDetector | None = None,
        pipeline: ETLPipeline | None = None,
    ):
        self.unified = unified or UnifiedMetrics()
        self.detector = detector or AnomalyDetector()
        self.pipeline = pipeline or ETLPipeline()

    def get_kpis(self) -> dict:
        overview = self.unified.get_overview()
        return {
            "total_spend": overview["total_ad_spend"],
            "total_conversions": overview["total_conversions"],
            "blended_cpc": overview["blended_cpc"],
            "website_sessions": overview["website_sessions"],
        }

    def get_charts(self) -> dict:
        comparison = self.unified.get_platform_comparison()
        spend_trend = self.unified.get_spend_by_day(30)
        return {
            "platform_comparison": comparison,
            "spend_trend": spend_trend,
        }

    def get_anomalies(self) -> list[dict]:
        # Combine all campaigns
        meta = self.unified.meta.get_campaigns()
        google = self.unified.google.get_campaigns()
        all_camps = [
            {**c, "platform": "meta"} for c in meta
        ] + [
            {**c, "platform": "google"} for c in google
        ]
        anomalies = self.detector.detect_all_metrics(all_camps)
        return [
            {
                "campaign": a.campaign_name,
                "platform": a.platform,
                "metric": a.metric,
                "value": a.value,
                "z_score": a.z_score,
                "severity": a.severity,
                "message": a.message,
            }
            for a in anomalies
        ]

    def get_full_dashboard(self) -> dict:
        return {
            "kpis": self.get_kpis(),
            "charts": self.get_charts(),
            "anomalies": self.get_anomalies(),
            "etl_status": self.pipeline.get_status(),
        }
