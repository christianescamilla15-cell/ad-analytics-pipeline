"""FastAPI application -- Ad Analytics Pipeline API."""

from __future__ import annotations

from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from config import get_settings
from services.marketing.meta_ads import MetaAdsClient
from services.marketing.google_ads import GoogleAdsClient
from services.marketing.ga4 import GA4Client
from services.marketing.unified_metrics import UnifiedMetrics
from services.ocr.invoice_parser import InvoiceParser
from services.aws.s3_client import S3Client
from services.aws.lambda_handler import handler as lambda_handler
from services.etl.pipeline import ETLPipeline
from services.analytics.dashboard import DashboardService
from services.analytics.anomaly_detector import AnomalyDetector

settings = get_settings()

app = FastAPI(
    title=settings.app_name,
    version="1.0.0",
    description="AWS + OCR + Marketing APIs analytics pipeline",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -- Singletons --
meta = MetaAdsClient(settings.meta_access_token, settings.meta_ad_account_id)
google = GoogleAdsClient(settings.google_ads_developer_token, settings.google_ads_customer_id)
ga4 = GA4Client(settings.ga4_property_id)
unified = UnifiedMetrics(meta, google, ga4)
s3 = S3Client(settings.s3_bucket)
pipeline = ETLPipeline()
dashboard_svc = DashboardService(unified)
anomaly_detector = AnomalyDetector()
invoice_parser = InvoiceParser()


# ---- Health ----
@app.get("/api/health")
def health():
    return {"status": "ok", "mode": settings.mode, "app": settings.app_name}


# ---- Unified Overview ----
@app.get("/api/overview")
def overview():
    return unified.get_overview()


# ---- Platform-specific ----
@app.get("/api/platforms/meta")
def platform_meta():
    return {
        "campaigns": meta.get_campaigns(),
        "insights": meta.get_account_insights(),
    }


@app.get("/api/platforms/google")
def platform_google():
    return {
        "campaigns": google.get_campaigns(),
        "insights": google.get_account_insights(),
    }


@app.get("/api/platforms/ga4")
def platform_ga4():
    return {
        "overview": ga4.get_overview(),
        "top_pages": ga4.get_top_pages(),
        "traffic_sources": ga4.get_traffic_sources(),
        "conversions": ga4.get_conversion_events(),
    }


@app.get("/api/comparison")
def comparison():
    return unified.get_platform_comparison()


# ---- Documents / OCR ----
@app.post("/api/documents/upload")
async def document_upload(file: UploadFile = File(...)):
    content = await file.read()
    text = content.decode("utf-8", errors="replace")

    # Store in S3 mock
    key = f"invoices/{file.filename}"
    s3.upload(key, content, content_type=file.content_type or "text/plain")

    # Process through lambda handler
    result = lambda_handler({"bucket": s3.bucket, "key": key, "content": text})
    return result["body"]


@app.post("/api/documents/parse")
async def document_parse(body: dict):
    text = body.get("text", "")
    invoice = invoice_parser.parse(text)
    return invoice.model_dump()


@app.get("/api/documents")
def document_list():
    return s3.list_objects(prefix="invoices/")


# ---- ETL ----
@app.post("/api/etl/run")
async def etl_run():
    result = await pipeline.run()
    return result


@app.get("/api/etl/status")
def etl_status():
    return pipeline.get_status()


# ---- Analytics ----
@app.get("/api/analytics/anomalies")
def analytics_anomalies():
    return dashboard_svc.get_anomalies()


@app.get("/api/analytics/spend-trend")
def analytics_spend_trend():
    return unified.get_spend_by_day(30)


# ---- S3 ----
@app.get("/api/s3/objects")
def s3_objects(prefix: str = ""):
    return s3.list_objects(prefix)


# ---- Dashboard ----
@app.get("/api/dashboard")
def dashboard():
    return dashboard_svc.get_full_dashboard()
