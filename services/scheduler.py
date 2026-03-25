"""Cron-like ETL scheduler with configurable intervals."""

import asyncio
from datetime import datetime, timezone
from dataclasses import dataclass, field


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
    def __init__(self):
        self._jobs: dict[str, ScheduledJob] = {}
        self._running = False

    def register(self, name: str, interval_seconds: int):
        self._jobs[name] = ScheduledJob(name=name, interval_seconds=interval_seconds)

    def get_status(self) -> list[dict]:
        return [
            {
                "name": j.name,
                "interval": j.interval_seconds,
                "last_run": j.last_run,
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
            "runs_completed": j.runs_completed,
            "status": j.status,
            "last_error": j.last_error,
        }

    def list_jobs(self) -> list[str]:
        return list(self._jobs.keys())
