"""ROI and ROAS calculation for campaigns."""


class ROICalculator:
    # Estimated revenue per conversion by campaign type
    REVENUE_ESTIMATES = {
        "LEAD_GENERATION": 250.0,
        "CONVERSIONS": 150.0,
        "BRAND_AWARENESS": 50.0,
        "VIDEO_VIEWS": 25.0,
        "SEARCH": 300.0,
        "DISPLAY": 75.0,
        "PERFORMANCE_MAX": 200.0,
    }

    def calculate_campaign_roi(self, campaign: dict) -> dict:
        objective = campaign.get("objective", campaign.get("type", "CONVERSIONS"))
        revenue_per_conv = self.REVENUE_ESTIMATES.get(objective, 150.0)
        conversions = campaign.get("conversions", 0)
        spend = campaign.get("spend", 0)

        estimated_revenue = conversions * revenue_per_conv
        roi = ((estimated_revenue - spend) / spend * 100) if spend > 0 else 0
        roas = estimated_revenue / spend if spend > 0 else 0

        return {
            "campaign": campaign.get("name", ""),
            "spend": spend,
            "conversions": conversions,
            "estimated_revenue": round(estimated_revenue, 2),
            "roi_percent": round(roi, 1),
            "roas": round(roas, 2),
            "profitable": roi > 0,
            "revenue_per_conversion": revenue_per_conv,
        }

    def calculate_portfolio_roi(self, campaigns: list[dict]) -> dict:
        results = [self.calculate_campaign_roi(c) for c in campaigns]
        total_spend = sum(r["spend"] for r in results)
        total_revenue = sum(r["estimated_revenue"] for r in results)
        overall_roi = (
            ((total_revenue - total_spend) / total_spend * 100)
            if total_spend > 0
            else 0
        )

        return {
            "campaigns": results,
            "total_spend": round(total_spend, 2),
            "total_estimated_revenue": round(total_revenue, 2),
            "overall_roi_percent": round(overall_roi, 1),
            "overall_roas": (
                round(total_revenue / total_spend, 2) if total_spend > 0 else 0
            ),
            "profitable_campaigns": len([r for r in results if r["profitable"]]),
            "unprofitable_campaigns": len(
                [r for r in results if not r["profitable"]]
            ),
            "best_roi": (
                max(results, key=lambda r: r["roi_percent"]) if results else None
            ),
            "worst_roi": (
                min(results, key=lambda r: r["roi_percent"]) if results else None
            ),
        }
