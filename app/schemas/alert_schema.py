"""
Data transfer objects for security alerts.

Defines the structure and validation for alert data returned by the API.
"""
from pydantic import BaseModel
from datetime import datetime

class SecurityAlert(BaseModel):
    """
    Schema for a security alert response payload.

    Attributes:
        alert_id: Unique ID of the alert.
        threat_type: Classification of the threat.
        source_ip: Originating IP.
        severity: Risk level.
        status: Investigation state.
        timestamp: Time of generation.
        recommended_action: Suggested remediation.
    """
    alert_id: int
    threat_type: str
    source_ip: str
    severity: str
    status: str
    timestamp: datetime
    recommended_action: str
