"""Tests for the AccountManager service."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from services.accounts import AccountManager


def test_demo_seed():
    mgr = AccountManager()
    accounts = mgr.list_accounts()
    assert len(accounts) == 3


def test_list_accounts_structure():
    mgr = AccountManager()
    accounts = mgr.list_accounts()
    for a in accounts:
        assert "id" in a
        assert "name" in a
        assert "platforms" in a
        assert a["platforms"]["meta"] is True


def test_get_account():
    mgr = AccountManager()
    accounts = mgr.list_accounts()
    first_id = accounts[0]["id"]
    detail = mgr.get_account(first_id)
    assert detail is not None
    assert detail["id"] == first_id
    assert "meta_account_id" in detail


def test_get_account_not_found():
    mgr = AccountManager()
    assert mgr.get_account("nonexistent") is None


def test_create_account():
    mgr = AccountManager()
    new = mgr.create_account(name="Test Corp", meta_id="act_999", google_id="gact_999")
    assert new["name"] == "Test Corp"
    assert new["meta_account_id"] == "act_999"
    # Now should have 4 accounts
    assert len(mgr.list_accounts()) == 4
