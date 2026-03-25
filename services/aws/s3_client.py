"""AWS S3 client with in-memory mock for demo."""

from __future__ import annotations

from datetime import datetime, timezone


class S3Client:
    """AWS S3 client with in-memory mock for demo."""

    def __init__(self, bucket: str = "ad-analytics-docs", demo_mode: bool = True):
        self.bucket = bucket
        self._demo_mode = demo_mode
        self._mock_storage: dict[str, bytes] = {}

    def upload(
        self,
        key: str,
        data: bytes,
        content_type: str = "application/octet-stream",
    ) -> dict:
        if self._demo_mode:
            self._mock_storage[key] = data
            return {
                "bucket": self.bucket,
                "key": key,
                "size": len(data),
                "content_type": content_type,
                "url": f"s3://{self.bucket}/{key}",
                "uploaded_at": datetime.now(timezone.utc).isoformat(),
            }
        return {}

    def download(self, key: str) -> bytes | None:
        if self._demo_mode:
            return self._mock_storage.get(key)
        return None

    def list_objects(self, prefix: str = "") -> list[dict]:
        if self._demo_mode:
            return [
                {"key": k, "size": len(v), "bucket": self.bucket}
                for k, v in self._mock_storage.items()
                if k.startswith(prefix)
            ]
        return []

    def delete(self, key: str) -> bool:
        if self._demo_mode:
            return self._mock_storage.pop(key, None) is not None
        return False

    def exists(self, key: str) -> bool:
        if self._demo_mode:
            return key in self._mock_storage
        return False
