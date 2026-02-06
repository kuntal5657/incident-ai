import uuid
import time

from app.asyncio.queue import InferenceQueue
from app.asyncio.worker import InferenceWorker
from app.asyncio.job import InferenceJob
from app.asyncio.result_store import JobResultStore
from app.asyncio.status import JobStatus
from app.asyncio.dlq import DeadLetterQueue
from app.bootstrap import build_pipeline

# ---- Build shared infra ----
pipeline = build_pipeline()
queue = InferenceQueue(max_size=50)
result_store = JobResultStore()
dlq = DeadLetterQueue()

# ---- Start worker ----
worker = InferenceWorker(queue, pipeline, result_store, dlq)
worker.start()

# ---- Submit job ----
job_id = str(uuid.uuid4())

payload = {
    "incident_id": "INC-5003",
    "title": "Checkout timeout",
    "service": "checkout-api",
    "description": "Requests timing out under load",
    "environment": "prod",
    "logs": [],
    "alerts": [],
}

job = InferenceJob(job_id=job_id, payload=payload)
result_store.set_pending(job_id)
queue.submit(job)

print("Job submitted:", job_id)

# ---- Poll for result ----
while True:
    status = result_store.get_status(job_id)
    print("Status:", status)

    if status == JobStatus.SUCCEEDED:
        print("\n=== RESULT ===")
        print(result_store.get_result(job_id))
        break

    if status == JobStatus.FAILED:
        print("\n=== ERROR ===")
        print(result_store.get_error(job_id))
        break

    time.sleep(1)

print("\n=== DLQ CONTENTS ===")
print(dlq.list_jobs())
