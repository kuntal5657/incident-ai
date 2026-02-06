"""
NormalizeStep

Why this step exists:
- Converts raw input into LLM-safe, canonical form
- Applies safety guards
- Enforces token-conscious structure
"""

from app.pipeline.base import PipelineStep
from app.schemas.incident_input import IncidentInput
from app.safety.pii_scrubber import PIIScrubber
from app.safety.injection_guard import PromptInjectionGuard


class NormalizeStep(PipelineStep):
    def run(self, raw_payload: dict) -> dict:
        """
        Normalize raw incident input into a clean, safe dictionary.

        Input:
        - raw_payload: dict (untrusted)

        Output:
        - normalized dict (LLM-safe)
        """

        # 1️⃣ Validate and parse input
        incident = IncidentInput(**raw_payload)

        # 2️⃣ Scrub PII
        clean_logs = PIIScrubber.scrub_list(incident.logs)
        clean_alerts = PIIScrubber.scrub_list(incident.alerts)

        # 3️⃣ Guard against prompt injection
        safe_logs = PromptInjectionGuard.sanitize_list(clean_logs)
        safe_alerts = PromptInjectionGuard.sanitize_list(clean_alerts)

        # 4️⃣ Build normalized representation
        normalized = {
            "incident_id": incident.incident_id,
            "title": incident.title,
            "description": incident.description or "",
            "service": incident.service,
            "environment": incident.environment,
            "logs": safe_logs,
            "alerts": safe_alerts,
        }

        return normalized
