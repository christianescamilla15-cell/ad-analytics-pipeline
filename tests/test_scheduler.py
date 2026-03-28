"""Tests for the APScheduler-backed Scheduler service."""

import sys
import time
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


def test_scheduler_starts():
    """Scheduler.start() actually starts the APScheduler background thread."""
    s = Scheduler()
    call_log = []
    s.register("ping", 1, func=lambda: call_log.append(1))
    assert not s.running
    s.start()
    assert s.running
    # Give APScheduler a moment to fire the first execution
    time.sleep(1.5)
    s.shutdown()
    assert not s.running
    # The job should have fired at least once
    assert len(call_log) >= 1


def test_register_job_with_callback():
    """Jobs registered with a callback appear in get_status after start."""
    s = Scheduler()
    s.register("heartbeat", 60, func=lambda: None)
    s.start()
    jobs = s.get_status()
    assert len(jobs) == 1
    assert jobs[0]["name"] == "heartbeat"
    assert jobs[0]["next_run"] != ""  # APScheduler sets next_run_time
    s.shutdown()


def test_get_status_returns_jobs():
    """get_status returns all registered jobs with expected fields."""
    s = Scheduler()
    s.register("etl_full", 3600, func=lambda: None)
    s.register("alert_scan", 900, func=lambda: None)
    s.start()
    jobs = s.get_status()
    assert len(jobs) == 2
    for j in jobs:
        assert "name" in j
        assert "interval" in j
        assert "next_run" in j
        assert "runs_completed" in j
        assert "status" in j
    s.shutdown()


def test_job_records_error_on_exception():
    """If a job callback raises, the scheduler records the error."""
    s = Scheduler()

    def bad_job():
        raise ValueError("something broke")

    s.register("failing", 1, func=bad_job)
    s.start()
    time.sleep(1.5)
    s.shutdown()
    job = s.get_job("failing")
    assert job["status"] == "error"
    assert "something broke" in job["last_error"]
    assert job["runs_completed"] >= 1
