"""
Centralized configuration loading.

Why this file exists:
- Prevents config sprawl
- Makes behavior explicit
- Avoids hardcoding values in logic
"""

import os
from dotenv import load_dotenv

# Load .env file into environment
load_dotenv()


class Settings:
    # OpenAI
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY")
    OPENAI_BASE_MODEL: str = os.getenv("OPENAI_BASE_MODEL", "gpt-4.1-mini")
    OPENAI_FINE_TUNED_MODEL: str = os.getenv("OPENAI_FINE_TUNED_MODEL", "")
    OPENAI_TIMEOUT_SECONDS: int = int(os.getenv("OPENAI_TIMEOUT_SECONDS", "15"))
    OPENAI_MAX_TOKENS: int = int(os.getenv("OPENAI_MAX_TOKENS", "800"))

    # Environment
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "local")

    # 🔒 Cost controls
    MAX_PROMPT_CHARS = 8_000        # hard cap
    MAX_CONTEXT_CHARS = 6_000       # RAG cap
    MAX_RESPONSE_TOKENS = 300       # predictable cost

    # ⏱ Latency controls
    OPENAI_TIMEOUT_SECONDS = 10

     # ---- Token pricing (USD per 1K tokens) ----
    # Demo pricing (adjust later if needed)
    MODEL_PRICING = {
        "gpt-3.5-turbo": {
            "prompt": 0.0005,
            "completion": 0.0015,
        }
    }

     # ---- Budgets ----
    MAX_COST_PER_REQUEST_USD = 0.01     # hard safety limit
    MAX_INFER_LATENCY_MS = 8000         # SLO (8 seconds)

    # ---- Error thresholds ----
    MAX_ERROR_RATE = 0.05  

    @classmethod
    def validate(cls):
        """
        Fail fast if required configuration is missing.
        """
        if not cls.OPENAI_API_KEY:
            raise RuntimeError("OPENAI_API_KEY is not set")


# Validate on import so failures happen early
Settings.validate()
