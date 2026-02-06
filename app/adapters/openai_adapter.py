"""
OpenAIAdapter

Responsibilities:
- Talk to OpenAI API
- Execute inference calls
- Enforce timeout & token limits

IMPORTANT:
- This class does NOT decide which model to use
- It ONLY executes what the pipeline asks
"""

from openai import OpenAI
from app.config.settings import Settings
from app.observability.metrics import metrics
from app.observability.alerts import emit_alert

class OpenAIAdapter:
    def __init__(self):
        """
        Initialize OpenAI client with timeout control.
        """
        self.client = OpenAI(
            api_key=Settings.OPENAI_API_KEY,
            timeout=Settings.OPENAI_TIMEOUT_SECONDS,
        )
    
    def _estimate_cost(
        self,
        model: str,
        prompt_tokens: int,
        completion_tokens: int,
    ) -> float:
        """
        Estimate USD cost based on model pricing.
        """
        # Match model prefix
        for prefix, pricing in Settings.MODEL_PRICING.items():
            if model.startswith(prefix):
                return (
                    (prompt_tokens / 1000) * pricing["prompt"]
                    + (completion_tokens / 1000) * pricing["completion"]
                )

        return 0.0

    def classify_incident(
        self,
        system_prompt: str,
        user_prompt: str,
        model: str,
        max_tokens: int,
    ) -> str:
        """
        Call OpenAI Chat Completion API.

        Args:
            system_prompt: system-level instructions
            user_prompt: user + context prompt
            model: model name (base or fine-tuned)
            max_tokens: hard response token cap

        Returns:
            Raw text response from the model
        """

        response = self.client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            temperature=0,              # deterministic output
            max_tokens=max_tokens,      # cost control
        )

         # 🔢 Token usage from OpenAI
        usage = response.usage
        prompt_tokens = usage.prompt_tokens
        completion_tokens = usage.completion_tokens

        # 📊 Record metrics
        metrics.add_tokens(prompt_tokens, completion_tokens)

        cost = self._estimate_cost(
            model,
            prompt_tokens,
            completion_tokens,
        )
        metrics.add_cost(cost)

        # 🚨 Cost budget enforcement
        if cost > Settings.MAX_COST_PER_REQUEST_USD:
            emit_alert(
                alert_type="cost_budget_exceeded",
                details={
                    "model": model,
                    "cost_usd": round(cost, 6),
                    "prompt_tokens": prompt_tokens,
                    "completion_tokens": completion_tokens,
                },
            )

        return response.choices[0].message.content
