"""Campaign budget pacing and forecasting."""

from datetime import datetime, timezone


class BudgetPacer:
    def analyze_pacing(self, campaigns: list[dict]) -> list[dict]:
        results = []
        for c in campaigns:
            daily_budget = c.get("budget_daily", 0)
            total_spend = c.get("spend", 0)

            # Assume 30-day month
            monthly_budget = daily_budget * 30
            days_elapsed = 15  # Mock: mid-month
            expected_spend = daily_budget * days_elapsed

            pacing = total_spend / expected_spend if expected_spend > 0 else 0
            projected_monthly = (
                (total_spend / days_elapsed) * 30 if days_elapsed > 0 else 0
            )
            over_under = projected_monthly - monthly_budget

            status = (
                "on_track"
                if 0.85 <= pacing <= 1.15
                else "underspending"
                if pacing < 0.85
                else "overspending"
            )

            results.append(
                {
                    "campaign": c.get("name", ""),
                    "daily_budget": daily_budget,
                    "monthly_budget": monthly_budget,
                    "actual_spend": total_spend,
                    "expected_spend": round(expected_spend, 2),
                    "pacing_ratio": round(pacing, 2),
                    "projected_monthly_spend": round(projected_monthly, 2),
                    "over_under_budget": round(over_under, 2),
                    "status": status,
                    "recommendation": self._get_recommendation(
                        status, pacing, c.get("name", "")
                    ),
                }
            )
        return results

    def _get_recommendation(
        self, status: str, pacing: float, name: str
    ) -> str:
        if status == "overspending":
            return (
                f"Reduce daily budget or pause low-performing ad sets in '{name}'"
            )
        elif status == "underspending":
            return (
                f"Consider increasing bids or expanding audience for '{name}'"
            )
        return f"'{name}' is pacing well — maintain current settings"
