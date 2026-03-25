"""Shared test fixtures."""

import sys
from pathlib import Path

import pytest

# Ensure project root is on sys.path
ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from services.marketing.meta_ads import MetaAdsClient
from services.marketing.google_ads import GoogleAdsClient
from services.marketing.ga4 import GA4Client
from services.marketing.unified_metrics import UnifiedMetrics
from services.aws.s3_client import S3Client
from services.ocr.invoice_parser import InvoiceParser
from services.ocr.extractor import TextExtractor
from services.etl.pipeline import ETLPipeline
from services.analytics.anomaly_detector import AnomalyDetector
from services.analytics.dashboard import DashboardService


@pytest.fixture
def meta_client():
    return MetaAdsClient()


@pytest.fixture
def google_client():
    return GoogleAdsClient()


@pytest.fixture
def ga4_client():
    return GA4Client()


@pytest.fixture
def unified(meta_client, google_client, ga4_client):
    return UnifiedMetrics(meta_client, google_client, ga4_client)


@pytest.fixture
def s3_client():
    return S3Client()


@pytest.fixture
def invoice_parser():
    return InvoiceParser()


@pytest.fixture
def text_extractor():
    return TextExtractor()


@pytest.fixture
def pipeline():
    return ETLPipeline()


@pytest.fixture
def anomaly_detector():
    return AnomalyDetector()


@pytest.fixture
def dashboard_service(unified):
    return DashboardService(unified)


SAMPLE_INVOICE_TEXT = """
Invoice #INV-2024-0042
Date: 03/15/2024
From: Meta Platforms Advertising

1  Brand Awareness Campaign - March     $3,245.50
2  Lead Gen Campaign - Q1               $7,890.25
3  Retargeting Display Ads              $2,100.00

Subtotal: $13,235.75
Tax: $1,058.86
Total: $14,294.61
"""
