"""
Job definition for async inference.
"""

from dataclasses import dataclass
from typing import Dict


@dataclass
class InferenceJob:
    job_id: str
    payload: Dict
    attempts: int = 0
    max_attempts: int = 3
