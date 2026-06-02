"""
Security log ingestion routes for the BlackTrace API.

This module exposes the endpoint where validated security events enter
the threat detection pipeline.
"""
from fastapi import APIRouter, Depends, BackgroundTasks
from sqlalchemy.orm import Session
from app.schemas.log_schema import SecurityLog
from app.core.logging_config import logger
from app.database.session import get_db
from app.services.threat_analyzer import analyze_security_event

router = APIRouter()

security_events = []

def process_security_event(
    log,
    db
):
    """
    Process security events asynchronously.

    This function executes the threat analysis
    pipeline independently from the request cycle.
    """
    analyze_security_event(log, db)

@router.post("/logs")
def ingest_log(
    log: SecurityLog,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
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
    background_tasks.add_task(
        process_security_event,
        log,
        db
    )
    
    return {
        "status": "accepted",
        "message": (
            "Security event received and queued for background analysis"
        ),
        "total_events": len(security_events),
    }
