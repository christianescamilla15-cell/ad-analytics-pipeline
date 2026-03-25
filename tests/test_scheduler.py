"""Tests for the Scheduler service."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from services.scheduler import Scheduler


def test_register_job():
    s = Scheduler()
    s.register("test_job", 600)
    jobs = s.get_status()
    assert len(jobs) == 1
    assert jobs[0]["name"] == "test_job"
    assert jobs[0]["interval"] == 600


def test_get_status_multiple():
    s = Scheduler()
    s.register("job_a", 300)
    s.register("job_b", 900)
    jobs = s.get_status()
    assert len(jobs) == 2
    names = [j["name"] for j in jobs]
    assert "job_a" in names
    assert "job_b" in names


def test_record_run_success():
    s = Scheduler()
    s.register("etl", 3600)
    s.record_run("etl", success=True)
    job = s.get_job("etl")
    assert job["runs_completed"] == 1
    assert job["status"] == "completed"
    assert job["last_run"] != ""


def test_record_run_failure():
    s = Scheduler()
    s.register("etl", 3600)
    s.record_run("etl", success=False, error="Connection timeout")
    job = s.get_job("etl")
    assert job["status"] == "error"
    assert job["last_error"] == "Connection timeout"
