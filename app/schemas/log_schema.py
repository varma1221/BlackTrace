from pydantic import BaseModel
from datetime import datetime

class SecurityLog(BaseModel):
    source_ip: str
    event_type: str
    severity: str
    message: str
    timestamp: datetime
    