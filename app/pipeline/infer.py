"""
InferenceStep

Responsible for:
- model selection
- prompt assembly
- OpenAI call
- cost & latency guards
- schema validation
"""

import json

from app.pipeline.base import PipelineStep
from app.adapters.openai_adapter import OpenAIAdapter
from app.models.prompt_factory import system_prompt, user_prompt
from app.strategies.model_strategy import EnvBasedModelStrategy
from app.schemas.incident_output import IncidentClassification
from app.config.settings import Settings
from app.utils.text_limits import trim_text
from app.utils.simple_cache import SimpleCache
from app.observability.logger import get_logger

logger = get_logger("inference")


class InferenceStep(PipelineStep):
    def __init__(self):
        self.llm = OpenAIAdapter()
        self.model_strategy = EnvBasedModelStrategy()
        self.cache = SimpleCache()

    def run(self, normalized: dict, retrieval: dict) -> IncidentClassification:
        """
        Execute LLM inference with full safety controls.
        """

        # 1️⃣ Decide which model to use
        model = self.model_strategy.select(
            has_context=bool(retrieval["context_text"])
        )

        logger.info(
            "Model selected",
            extra={
                "request_id": normalized.get("request_id"),
                "model": model,
            },
        )

        # 2️⃣ Trim retrieved context (cost control)
        context = trim_text(
            retrieval["context_text"],
            Settings.MAX_CONTEXT_CHARS,
        )

        # 3️⃣ Build and trim user prompt
        prompt_text = trim_text(
            user_prompt(normalized, context),
            Settings.MAX_PROMPT_CHARS,
        )

        # 4️⃣ Cache lookup (major cost saver)
        cached = self.cache.get(prompt_text)
        if cached:
            return IncidentClassification(**cached)

        # 5️⃣ Call OpenAI with timeout + fallback
        try:
            raw_response = self.llm.classify_incident(
                system_prompt=system_prompt(),
                user_prompt=prompt_text,
                model=model,
                max_tokens=Settings.MAX_RESPONSE_TOKENS,
            )
        except Exception as e:
            logger.error(
                "Inference failed",
                extra={
                    "request_id": normalized.get("request_id"),
                    "error": str(e),
                },
            )

            # 🔴 Hard fallback (never break prod)
            return IncidentClassification(
                severity="P3",
                category="Unknown",
                probable_root_cause="LLM unavailable",
                recommended_actions=[
                    "Retry later",
                    "Manual investigation required",
                ],
                confidence=0.1,
            )

        # 6️⃣ Parse JSON defensively
        parsed = json.loads(raw_response)

        if "classification" in parsed:
            parsed = parsed["classification"]

        # 7️⃣ Validate schema
        result = IncidentClassification(**parsed)

        # 8️⃣ Cache successful result
        self.cache.set(prompt_text, result.model_dump())

        return result
