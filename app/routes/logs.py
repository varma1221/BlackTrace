"""
Security log ingestion routes for the BlackTrace API.

This module exposes the endpoint where validated security events enter
the threat detection pipeline.
"""
from fastapi import APIRouter
from app.schemas.log_schema import SecurityLog
from app.core.logging_config import logger
from app.services.threat_analyzer import analyze_security_event

router = APIRouter()

security_events = []

@router.post("/logs")
def ingest_log(log: SecurityLog):
    """
    Ingest a security event and submit it for threat analysis.

    The incoming request body is validated as a SecurityLog before this
    function runs. The validated event is stored in memory and passed to
    the threat analysis service for rule-based detection.
    """
    logger.info(
        f"Security Event Received: "
        f"{log.event_type} from {log.source_ip} at {log.timestamp}"
    )
    
    security_events.append(log)
    threat_analysis = analyze_security_event(log)
    
    return {
        "status": "Success",
        "message": "Security event ingested successfully",
        "total_events": len(security_events),
        "result": threat_analysis
    }
