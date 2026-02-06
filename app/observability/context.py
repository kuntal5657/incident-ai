"""
Request context utilities.

Used to correlate logs across pipeline steps.
"""

import uuid


def generate_request_id() -> str:
    return str(uuid.uuid4())
