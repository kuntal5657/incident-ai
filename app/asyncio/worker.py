import threading
import time

from app.asyncio.queue import InferenceQueue
from app.asyncio.result_store import JobResultStore
from app.asyncio.retry_policy import is_retryable_error
from app.asyncio.dlq import DeadLetterQueue
from app.observability.logger import get_logger

logger = get_logger("worker")


class InferenceWorker(threading.Thread):
    def __init__(
        self,
        queue: InferenceQueue,
        pipeline,
        result_store: JobResultStore,
        dlq: DeadLetterQueue,
    ):
        super().__init__(daemon=True)
        self.queue = queue
        self.pipeline = pipeline
        self.result_store = result_store
        self.dlq = dlq

    def run(self):
        logger.info("Inference worker started")

        while True:
            job = self.queue.get()
            job_id = job.job_id

            self.result_store.set_running(job_id)

            try:
                logger.info(
                    "Processing job",
                    extra={
                        "job_id": job_id,
                        "attempt": job.attempts + 1,
                    },
                )

                result = self.pipeline.run(job.payload)

                self.result_store.set_success(job_id, result)

                logger.info(
                    "Job completed",
                    extra={
                        "job_id": job_id,
                        "severity": result["classification"]["severity"],
                    },
                )

            except Exception as e:
                job.attempts += 1

                retryable = is_retryable_error(e)

                logger.error(
                    "Job failed",
                    extra={
                        "job_id": job_id,
                        "attempt": job.attempts,
                        "retryable": retryable,
                        "error": str(e),
                    },
                )

                if retryable and job.attempts < job.max_attempts:
                    logger.info(
                        "Retrying job",
                        extra={
                            "job_id": job_id,
                            "next_attempt": job.attempts + 1,
                        },
                    )
                    time.sleep(2)  # simple backoff
                    self.queue.submit(job)

                else:
                    self.result_store.set_failed(job_id, str(e))
                    self.dlq.add(job, reason=str(e))

                    logger.error(
                        "Job sent to DLQ",
                        extra={
                            "job_id": job_id,
                            "attempts": job.attempts,
                        },
                    )

            finally:
                self.queue.task_done()
