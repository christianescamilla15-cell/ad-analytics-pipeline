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
from services.marketing.rate_limiter import RateLimiter
from services.ocr.invoice_parser import InvoiceParser
from services.aws.s3_client import S3Client
from services.aws.lambda_handler import handler as lambda_handler
from services.etl.pipeline import ETLPipeline
from services.analytics.dashboard import DashboardService
from services.analytics.anomaly_detector import AnomalyDetector
from services.analytics.alerts import AlertManager
from services.analytics.roi import ROICalculator
from services.analytics.comparison import HistoricalComparison
from services.analytics.pdf_export import PDFReportGenerator
from services.analytics.budget_pacer import BudgetPacer
from services.scheduler import Scheduler
from services.cache import DataCache
from services.webhooks import WebhookReceiver
from services.accounts import AccountManager

settings = get_settings()

app = FastAPI(
    title=settings.app_name,
    version="2.0.0",
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

# -- New singletons --
scheduler = Scheduler()
scheduler.register("etl_full", interval_seconds=3600)
scheduler.register("etl_meta", interval_seconds=1800)
scheduler.register("etl_google", interval_seconds=1800)
scheduler.register("alert_scan", interval_seconds=900)

# Start the scheduler so jobs actually run on intervals
scheduler.start()

alert_manager = AlertManager()
roi_calculator = ROICalculator()
historical_comparison = HistoricalComparison()
pdf_report_gen = PDFReportGenerator()
budget_pacer = BudgetPacer()
rate_limiter = RateLimiter()
data_cache = DataCache(default_ttl=300)
webhook_receiver = WebhookReceiver()
account_manager = AccountManager()


# ---- Health ----
@app.get("/api/health")
def health():
    return {"status": "ok", "mode": settings.mode, "app": settings.app_name}


# ---- Unified Overview ----
@app.get("/api/overview")
def overview():
    cached = data_cache.get("overview")
    if cached:
        return cached
    result = unified.get_overview()
    data_cache.set("overview", result)
    return result


# ---- Platform-specific ----
@app.get("/api/platforms/meta")
def platform_meta():
    rate_limiter.record("meta")
    return {
        "campaigns": meta.get_campaigns(),
        "insights": meta.get_account_insights(),
    }


@app.get("/api/platforms/google")
def platform_google():
    rate_limiter.record("google")
    return {
        "campaigns": google.get_campaigns(),
        "insights": google.get_account_insights(),
    }


@app.get("/api/platforms/ga4")
def platform_ga4():
    rate_limiter.record("ga4")
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
    scheduler.record_run("etl_full", success=True)
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
    cached = data_cache.get("dashboard")
    if cached:
        return cached
    result = dashboard_svc.get_full_dashboard()
    data_cache.set("dashboard", result, ttl=120)
    return result


# =========================================================================
# NEW ENDPOINTS — Tier 1
# =========================================================================


# ---- Scheduler ----
@app.get("/api/scheduler/status")
def scheduler_status():
    return {"jobs": scheduler.get_status()}


@app.post("/api/scheduler/trigger/{job_name}")
async def scheduler_trigger(job_name: str):
    job = scheduler.get_job(job_name)
    if not job:
        return JSONResponse(status_code=404, content={"error": f"Job '{job_name}' not found"})
    try:
        if job_name.startswith("etl"):
            await pipeline.run()
        elif job_name == "alert_scan":
            all_campaigns = meta.get_campaigns() + google.get_campaigns()
            alert_manager.check_campaigns(all_campaigns)
        scheduler.record_run(job_name, success=True)
        return {"status": "triggered", "job": scheduler.get_job(job_name)}
    except Exception as exc:
        scheduler.record_run(job_name, success=False, error=str(exc))
        return JSONResponse(status_code=500, content={"error": str(exc)})


# ---- Alerts ----
@app.get("/api/alerts")
def get_alerts(severity: str = None, acknowledged: bool = None):
    # Auto-scan if no alerts exist yet
    if not alert_manager.get_alerts():
        all_campaigns = meta.get_campaigns() + google.get_campaigns()
        alert_manager.check_campaigns(all_campaigns)
    return {"alerts": alert_manager.get_alerts(severity=severity, acknowledged=acknowledged)}


@app.post("/api/alerts/{alert_id}/acknowledge")
def acknowledge_alert(alert_id: str):
    success = alert_manager.acknowledge(alert_id)
    if not success:
        return JSONResponse(status_code=404, content={"error": f"Alert '{alert_id}' not found"})
    return {"status": "acknowledged", "alert_id": alert_id}


@app.get("/api/alerts/thresholds")
def get_alert_thresholds():
    return {"thresholds": alert_manager.get_thresholds()}


@app.put("/api/alerts/thresholds")
def update_alert_thresholds(body: dict):
    updated = {}
    for key, value in body.items():
        if alert_manager.update_threshold(key, float(value)):
            updated[key] = float(value)
    return {"updated": updated, "thresholds": alert_manager.get_thresholds()}


# ---- ROI ----
@app.get("/api/analytics/roi")
def analytics_roi():
    all_campaigns = meta.get_campaigns() + google.get_campaigns()
    return roi_calculator.calculate_portfolio_roi(all_campaigns)


# ---- Historical Comparison ----
@app.get("/api/analytics/comparison")
def analytics_comparison(period: str = "month"):
    overview_data = unified.get_overview()
    kpis = {
        "total_spend": overview_data["total_ad_spend"],
        "total_conversions": overview_data["total_conversions"],
        "blended_cpc": overview_data["blended_cpc"],
        "blended_ctr": overview_data["blended_ctr"],
        "website_sessions": overview_data["website_sessions"],
    }
    return historical_comparison.compare_periods(kpis, period=period)


# ---- PDF Report ----
@app.get("/api/reports/executive")
def executive_report():
    dash = dashboard_svc.get_full_dashboard()
    all_campaigns = meta.get_campaigns() + google.get_campaigns()
    roi_data = roi_calculator.calculate_portfolio_roi(all_campaigns)
    alerts = alert_manager.get_alerts()
    return pdf_report_gen.generate_executive_report(dash, roi_data, alerts)


# =========================================================================
# NEW ENDPOINTS — Tier 2
# =========================================================================


# ---- Rate Limiter ----
@app.get("/api/rate-limits")
def rate_limits():
    return {"limits": rate_limiter.get_all_status()}


# ---- Cache Stats ----
@app.get("/api/cache/stats")
def cache_stats():
    return data_cache.get_stats()


# ---- Webhooks ----
@app.post("/api/webhooks/{platform}")
def receive_webhook(platform: str, body: dict):
    event_type = body.get("type", "unknown")
    signature = body.get("signature", "")
    payload = body.get("payload", body)
    event = webhook_receiver.process(platform, event_type, payload, signature)
    return {
        "status": "received",
        "platform": event.platform,
        "event_type": event.event_type,
        "verified": event.verified,
    }


@app.get("/api/webhooks/events")
def webhook_events(platform: str = None, limit: int = 50):
    return {"events": webhook_receiver.get_events(platform=platform, limit=limit)}


# ---- Budget Pacing ----
@app.get("/api/analytics/budget-pacing")
def budget_pacing():
    all_campaigns = meta.get_campaigns() + google.get_campaigns()
    return {"pacing": budget_pacer.analyze_pacing(all_campaigns)}


# ---- Accounts ----
@app.get("/api/accounts")
def list_accounts():
    return {"accounts": account_manager.list_accounts()}


@app.get("/api/accounts/{account_id}")
def get_account(account_id: str):
    account = account_manager.get_account(account_id)
    if not account:
        return JSONResponse(status_code=404, content={"error": "Account not found"})
    return account


@app.post("/api/accounts")
def create_account(body: dict):
    account = account_manager.create_account(
        name=body.get("name", ""),
        meta_id=body.get("meta_account_id", ""),
        google_id=body.get("google_account_id", ""),
        ga4_id=body.get("ga4_property_id", ""),
    )
    return account
