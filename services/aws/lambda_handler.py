"""AWS Lambda handler for document processing.

Triggered by S3 PUT events -- extracts text, parses invoices, stores results.
"""

from __future__ import annotations

from datetime import datetime, timezone

from services.ocr.invoice_parser import InvoiceParser


def handler(event: dict, context: dict | None = None) -> dict:
    """Process an uploaded document and return parsed invoice data."""
    bucket = event.get("bucket", "")
    key = event.get("key", "")
    content = event.get("content", "")

    parser = InvoiceParser()
    invoice = parser.parse(content)

    return {
        "statusCode": 200,
        "body": {
            "source": f"s3://{bucket}/{key}",
            "invoice": invoice.model_dump(),
            "processed_at": datetime.now(timezone.utc).isoformat(),
        },
    }
