"""Cron-like ETL scheduler powered by APScheduler with configurable intervals."""

from __future__ import annotations

import logging
from datetime import datetime, timezone
from dataclasses import dataclass, field
from typing import Callable

from apscheduler.schedulers.background import BackgroundScheduler

logger = logging.getLogger(__name__)


@dataclass
class ScheduledJob:
    name: str
    interval_seconds: int
    last_run: str = ""
    next_run: str = ""
    runs_completed: int = 0
    status: str = "idle"  # idle, running, error
    last_error: str = ""


class Scheduler:
    """Background job scheduler backed by APScheduler.

    Jobs are registered with a name, interval, and optional callable.
    When started, APScheduler runs each callable on its interval.
    """

    def __init__(self):
        self._jobs: dict[str, ScheduledJob] = {}
        self._callbacks: dict[str, Callable] = {}
        self._scheduler = BackgroundScheduler()
        self._started = False

    # -- Registration ----------------------------------------------------------

    def register(self, name: str, interval_seconds: int, func: Callable | None = None):
        """Register a job. If *func* is provided it will be scheduled when start() is called."""
        self._jobs[name] = ScheduledJob(name=name, interval_seconds=interval_seconds)
        if func is not None:
            self._callbacks[name] = func

    # -- Lifecycle -------------------------------------------------------------

    def start(self):
        """Start the background scheduler and add all registered jobs that have callbacks."""
        if self._started:
            return
        for name, func in self._callbacks.items():
            job_meta = self._jobs[name]
            self._scheduler.add_job(
                self._wrap(name, func),
                "interval",
                seconds=job_meta.interval_seconds,
                id=name,
                replace_existing=True,
            )
        self._scheduler.start()
        self._started = True
        logger.info("Scheduler started with %d jobs", len(self._callbacks))

    def shutdown(self):
        """Gracefully shut down the scheduler."""
        if self._started:
            self._scheduler.shutdown(wait=False)
            self._started = False

    @property
    def running(self) -> bool:
        return self._started

    # -- Job execution wrapper -------------------------------------------------

    def _wrap(self, name: str, func: Callable) -> Callable:
        """Wrap a callback so it automatically records success/failure."""
        def _inner():
            try:
                self._jobs[name].status = "running"
                func()
                self.record_run(name, success=True)
            except Exception as exc:
                self.record_run(name, success=False, error=str(exc))
                logger.exception("Job %s failed", name)
        return _inner

    # -- Status ----------------------------------------------------------------

    def get_status(self) -> list[dict]:
        self._sync_next_run_times()
        return [
            {
                "name": j.name,
                "interval": j.interval_seconds,
                "last_run": j.last_run,
                "next_run": j.next_run,
                "runs_completed": j.runs_completed,
                "status": j.status,
                "last_error": j.last_error,
            }
            for j in self._jobs.values()
        ]

    def record_run(self, name: str, success: bool, error: str = ""):
        if name in self._jobs:
            j = self._jobs[name]
            j.last_run = datetime.now(timezone.utc).isoformat()
            j.runs_completed += 1
            j.status = "completed" if success else "error"
            j.last_error = error

    def get_job(self, name: str) -> dict | None:
        j = self._jobs.get(name)
        if not j:
            return None
        return {
            "name": j.name,
            "interval": j.interval_seconds,
            "last_run": j.last_run,
            "next_run": j.next_run,
            "runs_completed": j.runs_completed,
            "status": j.status,
            "last_error": j.last_error,
        }

    def list_jobs(self) -> list[str]:
        return list(self._jobs.keys())

    # -- Internals -------------------------------------------------------------

    def _sync_next_run_times(self):
        """Pull next_run_time from APScheduler into our dataclass."""
        if not self._started:
            return
        for ap_job in self._scheduler.get_jobs():
            if ap_job.id in self._jobs:
                nrt = ap_job.next_run_time
                self._jobs[ap_job.id].next_run = str(nrt) if nrt else ""
