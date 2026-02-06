"""
FastAPI entry point for Incident AI system.

This file exposes HTTP APIs and delegates
all heavy work to async background workers.
"""

import uuid
from fastapi import FastAPI, HTTPException

from app.asyncio.queue import InferenceQueue
from app.asyncio.worker import InferenceWorker
from app.asyncio.job import InferenceJob
from app.asyncio.result_store import JobResultStore
from app.asyncio.status import JobStatus
from app.asyncio.dlq import DeadLetterQueue
from app.bootstrap import build_pipeline
from app.observability.logger import get_logger
from app.api.schemas import IncidentRequest, JobSubmitResponse, JobStatusResponse

logger = get_logger("api")

# ---------------------------------------------------
# Create FastAPI app
# ---------------------------------------------------
app = FastAPI(title="Incident AI API")

# ---------------------------------------------------
# Shared infrastructure (created ONCE)
# ---------------------------------------------------
pipeline = build_pipeline()
queue = InferenceQueue(max_size=100)
result_store = JobResultStore()
dlq = DeadLetterQueue()

# Start background worker
worker = InferenceWorker(queue, pipeline, result_store, dlq)
worker.start()

@app.post("/incidents", response_model=JobSubmitResponse)
def submit_incident(incident: IncidentRequest):
    """
    Submit an incident for async processing.
    """

    job_id = str(uuid.uuid4())

    job = InferenceJob(
        job_id=job_id,
        payload=incident.model_dump(),
    )

    result_store.set_pending(job_id)
    queue.submit(job)

    logger.info(
        "Incident submitted",
        extra={"job_id": job_id},
    )

    return JobSubmitResponse(
        job_id=job_id,
        status=JobStatus.PENDING,
    )

@app.get("/jobs/{job_id}", response_model=JobStatusResponse)
def get_job_status(job_id: str):
    """
    Get status or result of an async job.
    """

    status = result_store.get_status(job_id)

    if not status:
        raise HTTPException(status_code=404, detail="Job not found")

    if status == JobStatus.SUCCEEDED:
        return JobStatusResponse(
            job_id=job_id,
            status=status,
            result=result_store.get_result(job_id),
        )

    if status == JobStatus.FAILED:
        return JobStatusResponse(
            job_id=job_id,
            status=status,
            error=result_store.get_error(job_id),
        )

    return JobStatusResponse(
        job_id=job_id,
        status=status,
    )
