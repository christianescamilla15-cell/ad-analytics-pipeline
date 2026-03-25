"""Tests for the ROICalculator service."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from services.analytics.roi import ROICalculator


def test_single_campaign_profitable():
    calc = ROICalculator()
    result = calc.calculate_campaign_roi({
        "name": "Lead Gen", "objective": "LEAD_GENERATION",
        "conversions": 100, "spend": 5000,
    })
    # 100 * 250 = 25000 revenue, ROI = (25000-5000)/5000 * 100 = 400%
    assert result["profitable"] is True
    assert result["roi_percent"] == 400.0
    assert result["roas"] == 5.0


def test_single_campaign_unprofitable():
    calc = ROICalculator()
    result = calc.calculate_campaign_roi({
        "name": "Expensive Ads", "objective": "VIDEO_VIEWS",
        "conversions": 2, "spend": 5000,
    })
    # 2 * 25 = 50 revenue, ROI = (50-5000)/5000 * 100 = -99%
    assert result["profitable"] is False
    assert result["roi_percent"] < 0


def test_zero_spend():
    calc = ROICalculator()
    result = calc.calculate_campaign_roi({
        "name": "No Spend", "conversions": 10, "spend": 0,
    })
    assert result["roi_percent"] == 0
    assert result["roas"] == 0


def test_portfolio_roi():
    calc = ROICalculator()
    campaigns = [
        {"name": "A", "objective": "SEARCH", "conversions": 50, "spend": 3000},
        {"name": "B", "objective": "DISPLAY", "conversions": 20, "spend": 2000},
    ]
    result = calc.calculate_portfolio_roi(campaigns)
    assert result["total_spend"] == 5000
    assert len(result["campaigns"]) == 2
    assert result["best_roi"] is not None
    assert result["worst_roi"] is not None


def test_portfolio_profitable_count():
    calc = ROICalculator()
    campaigns = [
        {"name": "Good", "objective": "SEARCH", "conversions": 50, "spend": 1000},
        {"name": "Bad", "objective": "VIDEO_VIEWS", "conversions": 1, "spend": 5000},
    ]
    result = calc.calculate_portfolio_roi(campaigns)
    assert result["profitable_campaigns"] == 1
    assert result["unprofitable_campaigns"] == 1


def test_empty_portfolio():
    calc = ROICalculator()
    result = calc.calculate_portfolio_roi([])
    assert result["total_spend"] == 0
    assert result["best_roi"] is None
