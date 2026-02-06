"""
Dead Letter Queue (DLQ).

Stores jobs that exceeded retry limits.
"""

from typing import Dict
from app.asyncio.job import InferenceJob


class DeadLetterQueue:
    def __init__(self):
        self.jobs: Dict[str, InferenceJob] = {}

    def add(self, job: InferenceJob, reason: str):
        self.jobs[job.job_id] = {
            "job": job,
            "reason": reason,
        }

    def list_jobs(self):
        return self.jobs
