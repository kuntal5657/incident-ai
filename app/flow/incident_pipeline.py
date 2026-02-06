from app.pipeline.normalize import NormalizeStep
from app.pipeline.retrieve import RetrieveContextStep
from app.pipeline.infer import InferenceStep

from app.observability.logger import get_logger
from app.observability.context import generate_request_id
from app.observability.metrics import metrics
from app.observability.timer import Timer

from app.observability.alerts import emit_alert
from app.config.settings import Settings


logger = get_logger("incident_pipeline")


class IncidentPipeline:
    def __init__(self, vector_store):
        self.vector_store = vector_store

    def run(self, incident_payload: dict):
        request_id = generate_request_id()
        metrics.inc("pipeline.requests.total")

        logger.info(
            "Pipeline started",
            extra={"request_id": request_id, "step": "start"},
        )

        try:
             # ---- Normalize ----
            with Timer("pipeline.normalize.latency_ms"):
                normalized = NormalizeStep().run(incident_payload)

            # ---- Retrieve (RAG) ----
            with Timer("pipeline.retrieve.latency_ms"):
                retrieval = RetrieveContextStep(
                    vector_store=self.vector_store
                ).run(normalized)

            # ---- Inference ----
            with Timer("pipeline.infer.latency_ms"):
                classification = InferenceStep().run(
                    normalized=normalized,
                    retrieval=retrieval,
                )

            metrics.inc("pipeline.requests.success")

        except Exception as e:
            metrics.inc("pipeline.requests.failed")

            logger.error(
                "Pipeline failed",
                extra={
                    "request_id": request_id,
                    "step": "error",
                    "error": str(e),
                },
            )

            # 🚨 Error-rate alert
            total = metrics.counters.get("pipeline.requests.total", 0)
            failed = metrics.counters.get("pipeline.requests.failed", 0)

            if total > 0 and (failed / total) > Settings.MAX_ERROR_RATE:
                emit_alert(
                    alert_type="error_rate_exceeded",
                    details={
                        "error_rate": round(failed / total, 3),
                        "threshold": Settings.MAX_ERROR_RATE,
                    },
                )

            raise
        
        # 🚨 Latency SLO enforcement
        infer_timings = metrics.timings.get("pipeline.infer.latency_ms", [])
        if infer_timings:
            last_latency = infer_timings[-1]
            if last_latency > Settings.MAX_INFER_LATENCY_MS:
                emit_alert(
                    alert_type="latency_slo_breach",
                    details={
                        "request_id": request_id,
                        "latency_ms": round(last_latency, 2),
                        "slo_ms": Settings.MAX_INFER_LATENCY_MS,
                    },
                )

        logger.info(
            "Pipeline completed",
            extra={
                "request_id": request_id,
                "step": "complete",
            },
        )

        return {
            "incident_id": normalized["incident_id"],
            "classification": classification.model_dump(),
            "sources": retrieval["sources"],
        }
