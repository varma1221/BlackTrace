"""
Data transfer objects for security log ingestion.

Defines the validation schema for incoming security events.
"""
from pydantic import BaseModel
from datetime import datetime

class SecurityLog(BaseModel):
    """
    Schema for an incoming security event.

    Ensures ingested logs contain the metadata required for threat analysis.
    """
    source_ip: str
    event_type: str
    severity: str
    message: str
    timestamp: datetime
    