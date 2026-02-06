from pydantic import BaseModel
from typing import List, Optional


class IncidentRequest(BaseModel):
    incident_id: str
    title: str
    description: str
    service: str
    environment: str
    logs: Optional[List[str]] = []
    alerts: Optional[List[str]] = []


class JobSubmitResponse(BaseModel):
    job_id: str
    status: str


class JobStatusResponse(BaseModel):
    job_id: str
    status: str
    result: Optional[dict] = None
    error: Optional[str] = None
