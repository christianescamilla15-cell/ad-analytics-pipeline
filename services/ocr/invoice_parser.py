"""Structured invoice data extraction from text."""

from __future__ import annotations

import re
from pydantic import BaseModel
from typing import Optional


class InvoiceData(BaseModel):
    invoice_number: str = ""
    vendor_name: str = ""
    date: Optional[str] = None
    subtotal: float = 0.0
    tax: float = 0.0
    total: float = 0.0
    currency: str = "USD"
    line_items: list[dict] = []
    raw_text: str = ""
    confidence: float = 0.0


class InvoiceParser:
    """Parse invoice text into structured data."""

    PATTERNS = {
        "invoice_number": r"(?:Invoice|Inv|#)\s*[:#]?\s*(\w+[-/]?\w+)",
        "date": r"(?:Date|Fecha)[:\s]+(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})",
        "total": r"(?:Total|Amount Due|Grand Total)[:\s]*\$?([\d,]+\.?\d*)",
        "subtotal": r"(?:Subtotal|Sub-total)[:\s]*\$?([\d,]+\.?\d*)",
        "tax": r"(?:Tax|IVA|VAT)[:\s]*\$?([\d,]+\.?\d*)",
        "vendor": r"(?:From|Bill From|Vendor)[:\s]*([A-Za-z\s&.,]+)",
    }

    def parse(self, text: str) -> InvoiceData:
        data: dict = {"raw_text": text, "confidence": 0.0}
        matches = 0

        for field_name, pattern in self.PATTERNS.items():
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                value: str | float = match.group(1).strip()
                if field_name in ("total", "subtotal", "tax"):
                    value = float(str(value).replace(",", ""))
                data[field_name] = value
                matches += 1

        # Extract line items
        item_pattern = r"(\d+)\s+(.+?)\s+\$?([\d,]+\.?\d*)"
        items = re.findall(item_pattern, text)
        data["line_items"] = [
            {
                "qty": int(q),
                "description": d.strip(),
                "amount": float(a.replace(",", "")),
            }
            for q, d, a in items
        ]

        data["confidence"] = min(matches / 4, 1.0)

        # Map vendor -> vendor_name
        if "vendor" in data:
            data["vendor_name"] = data.pop("vendor")

        if "invoice_number" not in data:
            data["invoice_number"] = ""

        safe = {k: v for k, v in data.items() if k in InvoiceData.model_fields}
        return InvoiceData(**safe)
