"""Data loaders -- persist transformed data to storage."""

from __future__ import annotations

import json
from datetime import datetime, timezone

from services.aws.s3_client import S3Client


class DataLoader:
    """Load transformed data into storage (S3 in demo)."""

    def __init__(self, s3: S3Client | None = None):
        self.s3 = s3 or S3Client()
        self._local_store: list[dict] = []

    def load(self, data: dict) -> dict:
        """Persist transformed data and return load summary."""
        timestamp = datetime.now(timezone.utc).isoformat()
        record = {
            "loaded_at": timestamp,
            "data": data,
        }
        self._local_store.append(record)

        # Also persist to S3 mock
        key = f"etl/output/{timestamp.replace(':', '-')}.json"
        payload = json.dumps(record, default=str).encode()
        self.s3.upload(key, payload, content_type="application/json")

        campaigns = data.get("campaigns", [])
        return {
            "total_records": len(campaigns),
            "storage_key": key,
            "loaded_at": timestamp,
        }

    def get_history(self) -> list[dict]:
        return [
            {"loaded_at": r["loaded_at"], "records": len(r["data"].get("campaigns", []))}
            for r in self._local_store
        ]
