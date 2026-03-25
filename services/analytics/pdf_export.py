"""Generate PDF executive reports."""

from datetime import datetime, timezone


class PDFReportGenerator:
    def generate_executive_report(
        self, dashboard_data: dict, roi_data: dict, alerts: list
    ) -> dict:
        """Generate a structured report (JSON format that frontend can render as PDF)."""
        return {
            "title": "Ad Analytics Executive Report",
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "period": "Last 30 Days",
            "sections": [
                {
                    "title": "Key Performance Indicators",
                    "data": dashboard_data.get("kpis", {}),
                },
                {
                    "title": "Platform Performance",
                    "data": dashboard_data.get("charts", {}).get(
                        "platform_comparison", []
                    ),
                },
                {
                    "title": "Return on Investment",
                    "data": {
                        "overall_roi": roi_data.get("overall_roi_percent", 0),
                        "overall_roas": roi_data.get("overall_roas", 0),
                        "best_campaign": roi_data.get("best_roi", {}).get(
                            "campaign", ""
                        ),
                        "profitable": roi_data.get("profitable_campaigns", 0),
                        "unprofitable": roi_data.get("unprofitable_campaigns", 0),
                    },
                },
                {
                    "title": "Active Alerts",
                    "data": {
                        "total": len(alerts),
                        "critical": len(
                            [
                                a
                                for a in alerts
                                if a.get("severity") == "critical"
                            ]
                        ),
                        "warnings": len(
                            [
                                a
                                for a in alerts
                                if a.get("severity") == "warning"
                            ]
                        ),
                    },
                },
                {
                    "title": "Recommendations",
                    "data": self._generate_recommendations(
                        dashboard_data, roi_data, alerts
                    ),
                },
            ],
        }

    def _generate_recommendations(
        self, dashboard: dict, roi: dict, alerts: list
    ) -> list[str]:
        recs = []
        if roi.get("unprofitable_campaigns", 0) > 0:
            worst = roi.get("worst_roi", {})
            recs.append(
                f"Review '{worst.get('campaign', 'N/A')}' — negative ROI "
                f"({worst.get('roi_percent', 0)}%). Consider pausing or restructuring."
            )
        critical = [a for a in alerts if a.get("severity") == "critical"]
        if critical:
            recs.append(
                f"{len(critical)} critical alert(s) require immediate attention."
            )
        recs.append(
            "Increase budget on top-performing campaigns to maximize ROAS."
        )
        recs.append(
            "Schedule weekly ETL runs to maintain fresh analytics data."
        )
        return recs
