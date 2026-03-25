"""Tests for the BudgetPacer service."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from services.analytics.budget_pacer import BudgetPacer


def test_on_track_pacing():
    pacer = BudgetPacer()
    # daily_budget=100, spend after 15 days = 1500 (expected = 100*15 = 1500, pacing=1.0)
    result = pacer.analyze_pacing([{"name": "OnTrack", "budget_daily": 100, "spend": 1500}])
    assert len(result) == 1
    assert result[0]["status"] == "on_track"
    assert result[0]["pacing_ratio"] == 1.0


def test_overspending():
    pacer = BudgetPacer()
    # daily_budget=100, expected=1500, spend=2000, pacing=1.33
    result = pacer.analyze_pacing([{"name": "Overbudget", "budget_daily": 100, "spend": 2000}])
    assert result[0]["status"] == "overspending"
    assert result[0]["pacing_ratio"] > 1.15


def test_underspending():
    pacer = BudgetPacer()
    # daily_budget=100, expected=1500, spend=500, pacing=0.33
    result = pacer.analyze_pacing([{"name": "Underspend", "budget_daily": 100, "spend": 500}])
    assert result[0]["status"] == "underspending"
    assert result[0]["pacing_ratio"] < 0.85


def test_recommendations():
    pacer = BudgetPacer()
    results = pacer.analyze_pacing([
        {"name": "Over", "budget_daily": 100, "spend": 2000},
        {"name": "Under", "budget_daily": 100, "spend": 500},
        {"name": "Good", "budget_daily": 100, "spend": 1500},
    ])
    assert "Reduce" in results[0]["recommendation"]
    assert "increasing" in results[1]["recommendation"]
    assert "pacing well" in results[2]["recommendation"]
