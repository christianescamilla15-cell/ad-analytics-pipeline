"""Text extraction from images and documents."""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class ExtractionResult:
    text: str = ""
    confidence: float = 0.0
    fields: dict = field(default_factory=dict)
    source: str = ""


class MockOCREngine:
    """Simulates Tesseract-style OCR output for demo mode."""

    SAMPLE_OUTPUT = (
        "Invoice #INV-2024-0042\n"
        "Date: 03/15/2024\n"
        "From: Meta Platforms Advertising\n\n"
        "1  Brand Awareness Campaign - March  $3,245.50\n"
        "2  Lead Gen Campaign - Q1           $7,890.25\n"
        "3  Retargeting Display Ads          $2,100.00\n\n"
        "Subtotal: $13,235.75\n"
        "Tax: $1,058.86\n"
        "Total: $14,294.61\n"
    )

    def recognize(self, image_path: str = "") -> ExtractionResult:
        """Return simulated OCR text regardless of input."""
        return ExtractionResult(
            text=self.SAMPLE_OUTPUT,
            confidence=0.92,
            source=image_path or "mock",
        )


class TextExtractor:
    """Rule-based text extractor for plain text files and OCR output."""

    FIELD_PATTERNS = {
        "dates": r"\d{1,2}[/-]\d{1,2}[/-]\d{2,4}",
        "amounts": r"\$[\d,]+\.?\d*",
        "invoice_numbers": r"(?:Invoice|Inv|#)\s*[:#]?\s*(\w+[-/]?\w+)",
        "emails": r"[\w.+-]+@[\w-]+\.[\w.]+",
        "vendor_names": r"(?:From|Vendor|Bill From)[:\s]+([A-Za-z\s&.,]+)",
    }

    def __init__(self, ocr_engine: MockOCREngine | None = None):
        self.ocr = ocr_engine or MockOCREngine()

    def extract_from_text(self, text: str) -> ExtractionResult:
        """Extract structured fields from raw text."""
        fields: dict[str, list[str]] = {}
        for name, pattern in self.FIELD_PATTERNS.items():
            matches = re.findall(pattern, text, re.IGNORECASE)
            if matches:
                fields[name] = matches

        confidence = min(len(fields) / 3, 1.0)
        return ExtractionResult(
            text=text,
            confidence=confidence,
            fields=fields,
            source="text",
        )

    def extract_from_file(self, file_path: str) -> ExtractionResult:
        """Read a text file and extract structured data."""
        path = Path(file_path)
        if not path.exists():
            return ExtractionResult(source=file_path)

        content = path.read_text(encoding="utf-8", errors="replace")
        result = self.extract_from_text(content)
        result.source = file_path
        return result

    def extract_from_image(self, image_path: str = "") -> ExtractionResult:
        """Use OCR engine (mock) to extract text from an image."""
        ocr_result = self.ocr.recognize(image_path)
        fields_result = self.extract_from_text(ocr_result.text)
        fields_result.confidence = ocr_result.confidence
        fields_result.source = image_path or "mock_image"
        return fields_result
