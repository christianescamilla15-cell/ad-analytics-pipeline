"""PDF text extraction (mock-based for demo)."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class PDFPage:
    page_number: int = 1
    text: str = ""
    word_count: int = 0


@dataclass
class PDFResult:
    pages: list[PDFPage] = field(default_factory=list)
    total_pages: int = 0
    metadata: dict = field(default_factory=dict)


class PDFTextExtractor:
    """Extract text from PDF files. Uses mock data in demo mode."""

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
        """Extract text from a PDF. Returns mock data in demo mode."""
        return PDFResult(
            pages=self.MOCK_PAGES,
            total_pages=len(self.MOCK_PAGES),
            metadata={
                "source": file_path or "mock.pdf",
                "producer": "Demo PDF Engine",
            },
        )

    def extract_text(self, file_path: str = "") -> str:
        """Get all text from a PDF as a single string."""
        result = self.extract(file_path)
        return "\n".join(page.text for page in result.pages)
