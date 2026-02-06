"""
Sync test entry point for IncidentPipeline.

This script:
- builds the pipeline via app.bootstrap
- runs a single incident through the system
- prints result
- logs metrics snapshot
"""

from app.bootstrap import build_pipeline
from app.observability.metrics import metrics
from app.observability.logger import get_logger

logger = get_logger("metrics")


def main():
    # --------------------------------------------------
    # Build pipeline (shared infra)
    # --------------------------------------------------
    pipeline = build_pipeline()

    # --------------------------------------------------
    # Test payload
    # --------------------------------------------------
    payload = {
        "incident_id": "INC-4001",
        "title": "Database latency spike",
        "service": "orders-db",
        "description": "High latency observed during peak traffic hours",
        "environment": "prod",
    }

    # --------------------------------------------------
    # Run pipeline (SYNC)
    # --------------------------------------------------
    result = pipeline.run(payload)

    print("\n=== PIPELINE RESULT ===")
    print(result)

    # --------------------------------------------------
    # Emit metrics snapshot AFTER execution
    # --------------------------------------------------
    logger.info(
        "Metrics snapshot",
        extra=metrics.snapshot(),
    )


if __name__ == "__main__":
    main()
