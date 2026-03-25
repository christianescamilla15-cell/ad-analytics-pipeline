# Ad Analytics Pipeline

Full-stack analytics pipeline combining **AWS services** (S3, Lambda, Textract), **OCR/document parsing**, and **Marketing APIs** (Meta Ads, Google Ads, GA4) into a unified dashboard.

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | Python 3.12, FastAPI, Pydantic |
| Frontend | React 18, Vite |
| Cloud | AWS S3, Lambda, Textract (mock) |
| Marketing | Meta Ads API, Google Ads API, GA4 Data API |
| OCR | Tesseract-style extractor, PDF parser, Invoice parser |
| ETL | Custom Extract-Transform-Load pipeline |
| Analytics | Z-score anomaly detection, unified metrics |
| Deploy | Docker, Vercel (frontend) |

## Features

- **Unified Dashboard** -- KPIs, charts, campaign table across Meta + Google + GA4
- **OCR Invoice Parsing** -- Regex-based text extraction with structured output
- **AWS Integration** -- S3 storage, Lambda document processing, Textract OCR
- **ETL Pipeline** -- Extract from APIs, transform/normalize, load to storage
- **Anomaly Detection** -- Z-score based spend anomaly alerts
- **Bilingual UI** -- English/Spanish with automatic detection
- **Demo Mode** -- Full functionality with realistic mock data (no API keys needed)

## Quick Start

```bash
# Backend
pip install fastapi uvicorn pydantic pydantic-settings httpx
uvicorn api.main:app --reload

# Frontend
cd frontend && npm install && npm run dev

# Tests
pip install pytest pytest-asyncio
python -m pytest tests/ -v

# Docker
docker compose up --build
```

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | /api/health | Health check |
| GET | /api/overview | Unified metrics overview |
| GET | /api/platforms/meta | Meta Ads campaigns + insights |
| GET | /api/platforms/google | Google Ads campaigns + insights |
| GET | /api/platforms/ga4 | GA4 overview + pages + sources |
| GET | /api/comparison | Platform comparison |
| POST | /api/documents/upload | Upload invoice for OCR |
| POST | /api/documents/parse | Parse invoice text |
| GET | /api/documents | List parsed documents |
| POST | /api/etl/run | Trigger ETL pipeline |
| GET | /api/etl/status | ETL pipeline status |
| GET | /api/analytics/anomalies | Spend anomaly alerts |
| GET | /api/analytics/spend-trend | 30-day spend trend |
| GET | /api/s3/objects | List S3 objects |
| GET | /api/dashboard | Full dashboard data |

## Project Structure

```
ad-analytics-pipeline/
├── config.py                 # Pydantic Settings
├── api/main.py               # FastAPI app (15 endpoints)
├── services/
│   ├── ocr/                  # Text extraction, PDF parsing, invoice parsing
│   ├── marketing/            # Meta Ads, Google Ads, GA4, unified metrics
│   ├── aws/                  # S3, Lambda, Textract
│   ├── etl/                  # Extract-Transform-Load pipeline
│   └── analytics/            # Dashboard, reports, anomaly detection
├── frontend/                 # React + Vite dashboard
├── tests/                    # 45+ tests
└── data/samples/             # Sample invoices and API responses
```

## License

This project is licensed for non-commercial, educational, and portfolio use only.
