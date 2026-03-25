"""AWS Textract client with mock for demo mode."""

from __future__ import annotations

import random


class TextractClient:
    """AWS Textract document analysis with mock."""

    def __init__(self, demo_mode: bool = True):
        self._demo_mode = demo_mode

    def analyze_document(self, document_bytes: bytes = b"") -> dict:
        """Analyze a document and return Textract-style blocks."""
        if self._demo_mode:
            return self._mock_analysis()
        return {}

    def detect_text(self, document_bytes: bytes = b"") -> list[dict]:
        """Detect text in a document image."""
        if self._demo_mode:
            return self._mock_detect_text()
        return []

    def _mock_analysis(self) -> dict:
        rng = random.Random(42)
        return {
            "DocumentMetadata": {"Pages": 2},
            "Blocks": [
                {
                    "BlockType": "PAGE",
                    "Id": "page-1",
                    "Confidence": 99.5,
                    "Geometry": {
                        "BoundingBox": {"Width": 1.0, "Height": 1.0, "Left": 0.0, "Top": 0.0}
                    },
                },
                {
                    "BlockType": "LINE",
                    "Id": "line-1",
                    "Text": "ADVERTISING INVOICE",
                    "Confidence": round(rng.uniform(95, 99.9), 1),
                    "Geometry": {
                        "BoundingBox": {"Width": 0.4, "Height": 0.03, "Left": 0.3, "Top": 0.05}
                    },
                },
                {
                    "BlockType": "LINE",
                    "Id": "line-2",
                    "Text": "Invoice #INV-2024-0042",
                    "Confidence": round(rng.uniform(95, 99.9), 1),
                    "Geometry": {
                        "BoundingBox": {"Width": 0.35, "Height": 0.03, "Left": 0.05, "Top": 0.10}
                    },
                },
                {
                    "BlockType": "LINE",
                    "Id": "line-3",
                    "Text": "Date: 03/15/2024",
                    "Confidence": round(rng.uniform(95, 99.9), 1),
                    "Geometry": {
                        "BoundingBox": {"Width": 0.25, "Height": 0.03, "Left": 0.05, "Top": 0.14}
                    },
                },
                {
                    "BlockType": "LINE",
                    "Id": "line-4",
                    "Text": "From: Meta Platforms Advertising",
                    "Confidence": round(rng.uniform(90, 99), 1),
                    "Geometry": {
                        "BoundingBox": {"Width": 0.45, "Height": 0.03, "Left": 0.05, "Top": 0.18}
                    },
                },
                {
                    "BlockType": "LINE",
                    "Id": "line-5",
                    "Text": "Total: $14,294.61",
                    "Confidence": round(rng.uniform(95, 99.9), 1),
                    "Geometry": {
                        "BoundingBox": {"Width": 0.3, "Height": 0.03, "Left": 0.05, "Top": 0.60}
                    },
                },
                {
                    "BlockType": "KEY_VALUE_SET",
                    "Id": "kv-1",
                    "EntityTypes": ["KEY"],
                    "Text": "Invoice Number",
                    "Confidence": 97.2,
                },
                {
                    "BlockType": "KEY_VALUE_SET",
                    "Id": "kv-2",
                    "EntityTypes": ["VALUE"],
                    "Text": "INV-2024-0042",
                    "Confidence": 98.1,
                },
            ],
            "AnalyzeDocumentModelVersion": "1.0",
        }

    def _mock_detect_text(self) -> list[dict]:
        return [
            {"text": "ADVERTISING INVOICE", "confidence": 99.1, "type": "LINE"},
            {"text": "Invoice #INV-2024-0042", "confidence": 98.5, "type": "LINE"},
            {"text": "Date: 03/15/2024", "confidence": 97.8, "type": "LINE"},
            {"text": "From: Meta Platforms Advertising", "confidence": 96.2, "type": "LINE"},
            {"text": "Total: $14,294.61", "confidence": 98.9, "type": "LINE"},
        ]
