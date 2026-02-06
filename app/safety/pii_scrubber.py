"""
PII Scrubber

Why this exists:
- LLMs must never see raw PII
- Logs often contain emails, IPs, tokens
- This is a legal + security requirement
"""

import re
from typing import List


class PIIScrubber:
    EMAIL_REGEX = re.compile(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+")
    IP_REGEX = re.compile(r"\b\d{1,3}(\.\d{1,3}){3}\b")
    TOKEN_REGEX = re.compile(r"(?i)(api[_-]?key|token|secret)[^\\s]*")

    @classmethod
    def scrub_text(cls, text: str) -> str:
        """
        Remove common PII patterns from a string.
        """
        text = cls.EMAIL_REGEX.sub("[REDACTED_EMAIL]", text)
        text = cls.IP_REGEX.sub("[REDACTED_IP]", text)
        text = cls.TOKEN_REGEX.sub("[REDACTED_SECRET]", text)
        return text

    @classmethod
    def scrub_list(cls, values: List[str]) -> List[str]:
        """
        Apply PII scrubbing to a list of strings.
        """
        return [cls.scrub_text(v) for v in values]
