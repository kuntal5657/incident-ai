"""
Alert helpers.

Alerts are emitted as structured logs.
Later they can be routed to Slack / PagerDuty.
"""

from app.observability.logger import get_logger

logger = get_logger("alerts")


def emit_alert(alert_type: str, details: dict):
    logger.error(
        f"ALERT: {alert_type}",
        extra={
            "alert_type": alert_type,
            **details,
        },
    )
