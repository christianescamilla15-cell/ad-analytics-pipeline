"""ETL pipeline orchestration."""

from __future__ import annotations

from datetime import datetime, timezone

from .extractors import MarketingExtractor
from .transformers import MarketingTransformer
from .loaders import DataLoader


class ETLPipeline:
    """Orchestrates the full ETL flow: Extract -> Transform -> Load."""

    def __init__(
        self,
        extractor: MarketingExtractor | None = None,
        transformer: MarketingTransformer | None = None,
        loader: DataLoader | None = None,
    ):
        self.extractor = extractor or MarketingExtractor()
        self.transformer = transformer or MarketingTransformer()
        self.loader = loader or DataLoader()
        self._last_run: dict | None = None

    async def run(self, sources: list[str] | None = None) -> dict:
        """Execute the full ETL pipeline."""
        sources = sources or ["meta", "google", "ga4"]
        started = datetime.now(timezone.utc)

        # Extract
        raw_data = self.extractor.extract_all(sources)

        # Transform
        clean_data = self.transformer.transform(raw_data)

        # Load
        load_result = self.loader.load(clean_data)

        finished = datetime.now(timezone.utc)
        elapsed = (finished - started).total_seconds()

        self._last_run = {
            "status": "completed",
            "sources": sources,
            "records": load_result["total_records"],
            "storage_key": load_result["storage_key"],
            "started_at": started.isoformat(),
            "finished_at": finished.isoformat(),
            "elapsed_seconds": round(elapsed, 3),
        }
        return self._last_run

    def get_status(self) -> dict:
        if self._last_run:
            return self._last_run
        return {"status": "idle", "message": "Pipeline has not been run yet."}
