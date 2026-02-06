"""
Retry classification logic.
"""


def is_retryable_error(error: Exception) -> bool:
    message = str(error).lower()

    # Retryable (transient)
    retryable_signals = [
        "timeout",
        "temporarily",
        "rate limit",
        "connection error",
    ]

    # Non-retryable (bad input, schema, logic)
    non_retryable_signals = [
        "validation error",
        "field required",
        "pydantic",
    ]

    if any(sig in message for sig in non_retryable_signals):
        return False

    if any(sig in message for sig in retryable_signals):
        return True

    # Default: do NOT retry unknown errors
    return False
