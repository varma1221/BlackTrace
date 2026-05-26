from pydantic import BaseModel
from datetime import datetime

class SecurityAlert(BaseModel):
    alert_id: int
    threat_type: str
    source_ip: str
    severity: str
    timestamp: datetime
    recommended_action: str
