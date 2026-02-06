"""
Incident Output Schema

Why this exists:
- Downstream automation depends on structure
- Prevents hallucinated fields
- Enables validation & retries
"""

from pydantic import BaseModel, Field
from typing import List, Literal


class IncidentClassification(BaseModel):
    severity: Literal["P0", "P1", "P2", "P3"] = Field(
        ..., description="Incident severity level"
    )

    category: str = Field(
        ..., description="High-level incident category"
    )

    probable_root_cause: str = Field(
        ..., description="Most likely root cause"
    )

    recommended_actions: List[str] = Field(
        ..., description="Actionable remediation steps"
    )

    confidence: float = Field(
        ..., ge=0.0, le=1.0, description="Model confidence score"
    )
