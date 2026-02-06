"""
Incident Input Schema

Why this exists:
- Defines the contract for incoming incidents
- Fails fast on bad or incomplete input
- Prevents garbage from reaching the LLM
"""

from pydantic import BaseModel, Field
from typing import Optional, List


class IncidentInput(BaseModel):
    """
    Canonical incident representation expected by the system.
    """

    incident_id: str = Field(
        ...,
        description="Unique identifier of the incident"
    )

    title: str = Field(
        ...,
        description="Short human-readable summary of the incident"
    )

    description: Optional[str] = Field(
        None,
        description="Detailed incident description"
    )

    service: str = Field(
        ...,
        description="Impacted service or system name"
    )

    environment: str = Field(
        ...,
        description="Environment (prod, staging, dev)"
    )

    logs: Optional[List[str]] = Field(
        default_factory=list,
        description="Relevant log lines or stack traces"
    )

    alerts: Optional[List[str]] = Field(
        default_factory=list,
        description="Alert messages or monitoring signals"
    )

    reported_by: Optional[str] = Field(
        None,
        description="Who reported the incident (email, username, system)"
    )
