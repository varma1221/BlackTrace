from fastapi import APIRouter

from app.schemas.log_schema import SecurityLog
from app.core.logging_config import logger

router = APIRouter()

security_events = []

@router.post("/logs")
def ingest_log(log: SecurityLog):
    
    logger.info(
        f"Security Event Received: "
        f"{log.event_type} from {log.source_ip} at {log.timestamp}"
    )
    
    security_events.append(log)
    
    return {
        "status": "Success",
        "message": "Security event ingested successfully",
        "total_events": len(security_events)
    }

