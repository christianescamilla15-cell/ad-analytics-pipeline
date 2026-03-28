"""PDF text extraction using pdfplumber for real OCR processing."""

from __future__ import annotations

import os
from dataclasses import dataclass, field


@dataclass
class PDFPage:
    page_number: int = 1
    text: str = ""
    tables: list = field(default_factory=list)
    word_count: int = 0


@dataclass
class PDFResult:
    pages: list[PDFPage] = field(default_factory=list)
    total_pages: int = 0
    full_text: str = ""
    metadata: dict = field(default_factory=dict)


def extract_text_from_pdf(pdf_path: str) -> dict:
    """Extract text, tables, and metadata from a PDF using pdfplumber.

    Args:
        pdf_path: Path to the PDF file.

    Returns:
        dict with page_count, full_text, pages (list), and metadata.

    Raises:
        FileNotFoundError: If the PDF file does not exist.
    """
    import pdfplumber

    if not os.path.isfile(pdf_path):
        raise FileNotFoundError(f"PDF not found: {pdf_path}")

    with pdfplumber.open(pdf_path) as pdf:
        pages = []
        full_text = ""
        for i, page in enumerate(pdf.pages):
            text = page.extract_text() or ""
            tables = page.extract_tables() or []
            pages.append({"page": i + 1, "text": text, "tables": tables})
            full_text += text + "\n"
        return {
            "page_count": len(pdf.pages),
            "full_text": full_text.strip(),
            "pages": pages,
            "metadata": pdf.metadata or {},
        }


class PDFTextExtractor:
    """Extract text from PDF files using pdfplumber.

    Falls back to mock data when no file is provided (demo mode).
    """

    MOCK_PAGES = [
        PDFPage(
            page_number=1,
            text=(
                "ADVERTISING INVOICE\n"
                "Invoice #INV-2024-0042\n"
                "Date: 03/15/2024\n"
                "Bill To: MindScrolling LLC\n"
                "From: Meta Platforms Advertising\n\n"
                "Campaign Summary - March 2024\n"
            ),
            word_count=18,
        ),
        PDFPage(
            page_number=2,
            text=(
                "Line Items:\n"
                "1  Brand Awareness Campaign - March  $3,245.50\n"
                "2  Lead Gen Campaign - Q1           $7,890.25\n"
                "3  Retargeting Display Ads          $2,100.00\n\n"
                "Subtotal: $13,235.75\n"
                "Tax: $1,058.86\n"
                "Total: $14,294.61\n\n"
                "Payment Terms: Net 30\n"
            ),
            word_count=32,
        ),
    ]

    def extract(self, file_path: str = "") -> PDFResult:
        """Extract text from a PDF.

        If a valid file_path is given, uses pdfplumber for real extraction.
        Otherwise returns mock data for demo purposes.
        """
        if file_path and os.path.isfile(file_path):
            data = extract_text_from_pdf(file_path)
            pages = [
                PDFPage(
                    page_number=p["page"],
                    text=p["text"],
                    tables=p["tables"],
                    word_count=len(p["text"].split()),
                )
                for p in data["pages"]
            ]
            return PDFResult(
                pages=pages,
                total_pages=data["page_count"],
                full_text=data["full_text"],
                metadata=data["metadata"],
            )

        # Fallback: mock data for demo mode
        return PDFResult(
            pages=self.MOCK_PAGES,
            total_pages=len(self.MOCK_PAGES),
            full_text="\n".join(p.text for p in self.MOCK_PAGES),
            metadata={
                "source": file_path or "mock.pdf",
                "producer": "Demo PDF Engine",
            },
        )

    def extract_text(self, file_path: str = "") -> str:
        """Get all text from a PDF as a single string."""
        result = self.extract(file_path)
        return result.full_text or "\n".join(page.text for page in result.pages)
