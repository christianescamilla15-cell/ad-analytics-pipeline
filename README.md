# Ad Analytics Pipeline

Unified analytics pipeline for marketing and product data across paid media and document workflows.

## Overview
Ad Analytics Pipeline is a full-stack analytics platform that combines marketing APIs, OCR/document parsing, ETL processing, anomaly detection, and dashboard visualization into a single workflow.

## Problem
Marketing and product data is fragmented across multiple platforms. Teams need a unified way to ingest, normalize, analyze, and visualize campaign performance and related documents.

## Solution
This project brings together:
- Meta Ads API integration
- Google Ads API integration
- GA4 Data API integration
- OCR / invoice parsing with confidence scoring
- ETL normalization pipeline
- Z-score anomaly detection
- React dashboard with bilingual support

## System Architecture

```text
Marketing APIs + Documents
          ↓
FastAPI ETL Layer
          ↓
Normalization / Parsing / OCR
          ↓
Analytics + Anomaly Detection (z-score)
          ↓
React Frontend Dashboard
```

## Engineering Decisions

### Why FastAPI for ETL?
To centralize API integration, transformation, and analytics logic in one service layer with async support.

### Why React + Vite?
To keep the dashboard responsive and modular with fast HMR during development.

### Why anomaly detection?
To make the platform useful beyond passive reporting — proactive alerts on spending anomalies.

## Tech Stack
| Layer | Technology |
|-------|-----------|
| Backend | Python 3.12, FastAPI, Pydantic |
| Frontend | React 18, Vite |
| APIs | Meta Ads, Google Ads, GA4 |
| Processing | OCR, z-score detection |
| Infra | Docker, Docker Compose |
| Testing | pytest (124 tests) |

## Repo Structure
```
api/              # FastAPI backend
frontend/         # React dashboard
services/         # ETL & analytics services
tests/            # 124 automated tests
data/samples/     # Sample datasets
```

## Key Metrics
| Metric | Value |
|--------|-------|
| APIs Integrated | 3 major platforms |
| Tests | 124 |
| Endpoints | 28 |
| Commits | 9 |

## How to Run
```bash
cp .env.example .env
docker compose up --build
```

## Roadmap
- [ ] Benchmark pipeline latency
- [ ] Richer campaign attribution views
- [ ] Alerting workflows
- [ ] Data warehouse integration

---
Built by [Christian Hernandez](https://ch65-portfolio.vercel.app) · AI Engineer
