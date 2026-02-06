"""
Model selection strategy.

Decides whether to use:
- fine-tuned model (if configured)
- base model (fallback)

This keeps model decisions out of pipeline logic.
"""

from app.config.settings import Settings


class ModelStrategy:
    def select(self, has_context: bool) -> str:
        raise NotImplementedError


class EnvBasedModelStrategy(ModelStrategy):
    """
    Cost-aware strategy:
    - Prefer fine-tuned model when context exists
    - Otherwise fall back to base model
    """

    def select(self, has_context: bool) -> str:
        if Settings.OPENAI_FINE_TUNED_MODEL and has_context:
            return Settings.OPENAI_FINE_TUNED_MODEL

        return Settings.OPENAI_BASE_MODEL
