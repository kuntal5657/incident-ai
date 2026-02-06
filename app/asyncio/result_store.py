"""
In-memory job result store.

Later replace with:
- Redis
- Database
"""

from typing import Dict
from app.asyncio.status import JobStatus


class JobResultStore:
    def __init__(self):
        self.status: Dict[str, JobStatus] = {}
        self.results: Dict[str, dict] = {}
        self.errors: Dict[str, str] = {}

    def set_pending(self, job_id: str):
        self.status[job_id] = JobStatus.PENDING

    def set_running(self, job_id: str):
        self.status[job_id] = JobStatus.RUNNING

    def set_success(self, job_id: str, result: dict):
        self.status[job_id] = JobStatus.SUCCEEDED
        self.results[job_id] = result

    def set_failed(self, job_id: str, error: str):
        self.status[job_id] = JobStatus.FAILED
        self.errors[job_id] = error

    def get_status(self, job_id: str):
        return self.status.get(job_id)

    def get_result(self, job_id: str):
        return self.results.get(job_id)

    def get_error(self, job_id: str):
        return self.errors.get(job_id)
