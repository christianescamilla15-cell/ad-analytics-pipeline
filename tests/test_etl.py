"""Tests for ETL pipeline."""

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from services.etl.extractors import MarketingExtractor
from services.etl.transformers import MarketingTransformer
from services.etl.loaders import DataLoader
from services.etl.pipeline import ETLPipeline


def test_extractor_all():
    ext = MarketingExtractor()
    data = ext.extract_all()
    assert "meta" in data
    assert "google" in data
    assert "ga4" in data


def test_extractor_single_source():
    ext = MarketingExtractor()
    data = ext.extract_all(["meta"])
    assert "meta" in data
    assert "google" not in data


def test_transformer_normalize():
    ext = MarketingExtractor()
    raw = ext.extract_all()
    t = MarketingTransformer()
    result = t.transform(raw)
    assert "campaigns" in result
    assert len(result["campaigns"]) == 7  # 4 meta + 3 google


def test_transformer_campaign_fields():
    ext = MarketingExtractor()
    raw = ext.extract_all()
    t = MarketingTransformer()
    result = t.transform(raw)
    camp = result["campaigns"][0]
    assert "platform" in camp
    assert camp["platform"] in ("meta", "google")


def test_transformer_summary():
    ext = MarketingExtractor()
    raw = ext.extract_all()
    t = MarketingTransformer()
    result = t.transform(raw)
    s = result["summary"]
    assert s["total_campaigns"] == 7
    assert s["total_spend"] > 0
    assert s["blended_cpc"] > 0


def test_loader():
    loader = DataLoader()
    data = {"campaigns": [{"id": "1"}, {"id": "2"}]}
    result = loader.load(data)
    assert result["total_records"] == 2
    assert result["storage_key"].startswith("etl/output/")


def test_loader_history():
    loader = DataLoader()
    loader.load({"campaigns": [{"id": "1"}]})
    loader.load({"campaigns": [{"id": "2"}, {"id": "3"}]})
    history = loader.get_history()
    assert len(history) == 2


@pytest.mark.asyncio
async def test_pipeline_run():
    p = ETLPipeline()
    result = await p.run()
    assert result["status"] == "completed"
    assert result["records"] == 7


@pytest.mark.asyncio
async def test_pipeline_status_after_run():
    p = ETLPipeline()
    assert p.get_status()["status"] == "idle"
    await p.run()
    assert p.get_status()["status"] == "completed"
