"""Tests for the real pdfplumber-based PDF parser."""

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))


def test_pdfplumber_import():
    """Verify pdfplumber is installed and importable."""
    import pdfplumber  # noqa: F401
    assert hasattr(pdfplumber, "open")


def test_extract_handles_missing_file():
    """extract_text_from_pdf raises FileNotFoundError for non-existent paths."""
    from services.ocr.pdf_parser import extract_text_from_pdf

    with pytest.raises(FileNotFoundError, match="PDF not found"):
        extract_text_from_pdf("/non/existent/file.pdf")


def test_extract_returns_correct_structure(tmp_path):
    """If a real PDF exists, verify the returned dict has the right keys."""
    try:
        from reportlab.pdfgen import canvas
    except ImportError:
        pytest.skip("reportlab not installed — cannot generate test PDF")

    # Create a simple PDF with reportlab
    pdf_file = tmp_path / "test_invoice.pdf"
    c = canvas.Canvas(str(pdf_file))
    c.drawString(100, 750, "ADVERTISING INVOICE")
    c.drawString(100, 730, "Total: $14,294.61")
    c.showPage()
    c.save()

    from services.ocr.pdf_parser import extract_text_from_pdf

    result = extract_text_from_pdf(str(pdf_file))
    assert "page_count" in result
    assert "full_text" in result
    assert "pages" in result
    assert "metadata" in result
    assert result["page_count"] >= 1
    assert isinstance(result["pages"], list)
    assert len(result["pages"]) == result["page_count"]
    # Check page structure
    page = result["pages"][0]
    assert "page" in page
    assert "text" in page
    assert "tables" in page


def test_extract_from_real_pdf(tmp_path):
    """End-to-end: create a PDF, extract text, verify content is present."""
    try:
        from reportlab.pdfgen import canvas
    except ImportError:
        pytest.skip("reportlab not installed — cannot generate test PDF")

    pdf_file = tmp_path / "sample.pdf"
    c = canvas.Canvas(str(pdf_file))
    c.drawString(100, 750, "MindScrolling LLC Invoice")
    c.drawString(100, 730, "Amount: $5,000.00")
    c.showPage()
    c.drawString(100, 750, "Page Two Content")
    c.showPage()
    c.save()

    from services.ocr.pdf_parser import extract_text_from_pdf

    result = extract_text_from_pdf(str(pdf_file))
    assert result["page_count"] == 2
    assert "MindScrolling" in result["full_text"]
    assert "Page Two" in result["full_text"]


def test_extractor_class_mock_fallback():
    """PDFTextExtractor still returns mock data when no file is given."""
    from services.ocr.pdf_parser import PDFTextExtractor

    extractor = PDFTextExtractor()
    result = extractor.extract()
    assert result.total_pages == 2
    assert "ADVERTISING INVOICE" in result.pages[0].text


def test_extractor_class_real_file(tmp_path):
    """PDFTextExtractor uses pdfplumber when a real file is provided."""
    try:
        from reportlab.pdfgen import canvas
    except ImportError:
        pytest.skip("reportlab not installed — cannot generate test PDF")

    pdf_file = tmp_path / "real.pdf"
    c = canvas.Canvas(str(pdf_file))
    c.drawString(100, 750, "Test Real Extraction")
    c.showPage()
    c.save()

    from services.ocr.pdf_parser import PDFTextExtractor

    extractor = PDFTextExtractor()
    result = extractor.extract(str(pdf_file))
    assert result.total_pages == 1
    assert result.full_text != ""
    assert result.pages[0].page_number == 1
