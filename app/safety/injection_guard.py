"""
Prompt Injection Guard

Why this exists:
- Logs can contain malicious instructions
- Stack traces may include "ignore previous instructions"
- We must neutralize that content
"""

from typing import List


class PromptInjectionGuard:
    SUSPICIOUS_PATTERNS = [
        "ignore previous",
        "disregard instructions",
        "system prompt",
        "you are chatgpt",
        "act as",
    ]

    @classmethod
    def sanitize(cls, text: str) -> str:
        """
        Remove or neutralize suspicious instruction-like content.
        """
        lowered = text.lower()
        for pattern in cls.SUSPICIOUS_PATTERNS:
            if pattern in lowered:
                return "[POTENTIALLY MALICIOUS CONTENT REMOVED]"
        return text

    @classmethod
    def sanitize_list(cls, values: List[str]) -> List[str]:
        """
        Apply injection sanitization to list of strings.
        """
        return [cls.sanitize(v) for v in values]
