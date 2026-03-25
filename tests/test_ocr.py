"""Tests for OCR services."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from services.ocr.extractor import TextExtractor, MockOCREngine, ExtractionResult
from services.ocr.pdf_parser import PDFTextExtractor
from tests.conftest import SAMPLE_INVOICE_TEXT


def test_mock_ocr_engine_returns_text():
    engine = MockOCREngine()
    result = engine.recognize()
    assert isinstance(result, ExtractionResult)
    assert "Invoice" in result.text
    assert result.confidence > 0.5


def test_text_extractor_from_text():
    extractor = TextExtractor()
    result = extractor.extract_from_text(SAMPLE_INVOICE_TEXT)
    assert result.text == SAMPLE_INVOICE_TEXT
    assert "amounts" in result.fields
    assert len(result.fields["amounts"]) >= 3


def test_text_extractor_dates():
    extractor = TextExtractor()
    result = extractor.extract_from_text(SAMPLE_INVOICE_TEXT)
    assert "dates" in result.fields
    assert "03/15/2024" in result.fields["dates"]


def test_text_extractor_invoice_numbers():
    extractor = TextExtractor()
    result = extractor.extract_from_text(SAMPLE_INVOICE_TEXT)
    assert "invoice_numbers" in result.fields


def test_text_extractor_from_image():
    extractor = TextExtractor()
    result = extractor.extract_from_image("fake_image.png")
    assert result.confidence > 0.5
    assert "Invoice" in result.text


def test_text_extractor_missing_file():
    extractor = TextExtractor()
    result = extractor.extract_from_file("/nonexistent/file.txt")
    assert result.text == ""


def test_pdf_extractor_returns_pages():
    extractor = PDFTextExtractor()
    result = extractor.extract()
    assert result.total_pages == 2
    assert len(result.pages) == 2


def test_pdf_extract_text():
    extractor = PDFTextExtractor()
    text = extractor.extract_text()
    assert "ADVERTISING INVOICE" in text
    assert "Total" in text
