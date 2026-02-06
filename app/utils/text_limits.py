def trim_text(text: str, max_chars: int) -> str:
    """
    Hard-trim text to avoid runaway token usage.
    """
    if len(text) <= max_chars:
        return text
    return text[:max_chars] + "\n[TRUNCATED]"
