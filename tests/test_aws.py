"""Tests for AWS services."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from services.aws.s3_client import S3Client
from services.aws.lambda_handler import handler
from services.aws.textract_client import TextractClient
from tests.conftest import SAMPLE_INVOICE_TEXT


# ---- S3 ----

def test_s3_upload():
    s3 = S3Client()
    result = s3.upload("test/doc.txt", b"hello world")
    assert result["key"] == "test/doc.txt"
    assert result["size"] == 11


def test_s3_download():
    s3 = S3Client()
    s3.upload("test/file.txt", b"content here")
    data = s3.download("test/file.txt")
    assert data == b"content here"


def test_s3_download_missing():
    s3 = S3Client()
    assert s3.download("nonexistent.txt") is None


def test_s3_list_objects():
    s3 = S3Client()
    s3.upload("invoices/a.txt", b"a")
    s3.upload("invoices/b.txt", b"bb")
    s3.upload("other/c.txt", b"ccc")
    objects = s3.list_objects("invoices/")
    assert len(objects) == 2


def test_s3_delete():
    s3 = S3Client()
    s3.upload("del.txt", b"data")
    assert s3.delete("del.txt") is True
    assert s3.download("del.txt") is None


def test_s3_delete_missing():
    s3 = S3Client()
    assert s3.delete("nope.txt") is False


def test_s3_exists():
    s3 = S3Client()
    s3.upload("exists.txt", b"yes")
    assert s3.exists("exists.txt") is True
    assert s3.exists("nope.txt") is False


# ---- Lambda ----

def test_lambda_handler():
    event = {
        "bucket": "ad-analytics-docs",
        "key": "invoices/test.txt",
        "content": SAMPLE_INVOICE_TEXT,
    }
    result = handler(event)
    assert result["statusCode"] == 200
    assert "invoice" in result["body"]
    assert result["body"]["invoice"]["total"] > 0


def test_lambda_handler_empty():
    result = handler({"bucket": "", "key": "", "content": ""})
    assert result["statusCode"] == 200
    assert result["body"]["invoice"]["confidence"] == 0.0


# ---- Textract ----

def test_textract_analyze():
    client = TextractClient()
    result = client.analyze_document()
    assert "Blocks" in result
    assert len(result["Blocks"]) > 0


def test_textract_block_types():
    client = TextractClient()
    result = client.analyze_document()
    types = {b["BlockType"] for b in result["Blocks"]}
    assert "PAGE" in types
    assert "LINE" in types


def test_textract_detect_text():
    client = TextractClient()
    lines = client.detect_text()
    assert len(lines) > 0
    assert lines[0]["type"] == "LINE"
    assert lines[0]["confidence"] > 90
