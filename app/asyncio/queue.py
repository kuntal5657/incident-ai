"""
In-memory job queue (learning + local dev).

Later replace with:
- Redis
- SQS
- Kafka
"""

import queue
from app.asyncio.job import InferenceJob


class InferenceQueue:
    def __init__(self, max_size: int = 100):
        self.queue = queue.Queue(maxsize=max_size)

    def submit(self, job: InferenceJob):
        self.queue.put(job, block=True)

    def get(self) -> InferenceJob:
        return self.queue.get(block=True)

    def task_done(self):
        self.queue.task_done()
