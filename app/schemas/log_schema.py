"""
Schema definitions for security log ingestion.

This module defines the data contract for security events submitted to
the BlackTrace detection pipeline.
"""
from pydantic import BaseModel
from datetime import datetime

class SecurityLog(BaseModel):
    """
    Request model for an incoming security event.

    Validates incoming log payloads against this schema before
    passing them to route handlers and threat detection services.
    """
    source_ip: str
    event_type: str
    severity: str
    message: str
    timestamp: datetime
    