"""
Security log ingestion and processing routes.

Handles the submission of raw security events and initiates the
asynchronous threat analysis pipeline.
"""
from fastapi import APIRouter, Depends, BackgroundTasks
from sqlalchemy.orm import Session
from app.schemas.log_schema import SecurityLog
from app.core.logging_config import logger
from app.database.session import get_db
from app.services.threat_analyzer import analyze_security_event
from app.services.event_service import store_raw_security_event

router = APIRouter()

def process_security_event(
    log,
    db
):
    """
    Internal task for executing the threat analysis pipeline.

    Executed as a background task to prevent blocking the ingestion response
    while rules and intelligence enrichment run.

    Args:
        log (SecurityLog): The validated security log payload.
        db (Session): Database session for alert persistence.
    """
    analyze_security_event(log, db)

@router.post("/logs")
def ingest_log(
    log: SecurityLog,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """
    Ingests a security log and queues background analysis.

    Validates the incoming log and triggers the threat analyzer via a
    non-blocking background task.

    Args:
        log (SecurityLog): The incoming security event schema.
        background_tasks (BackgroundTasks): FastAPI background task manager.
        db (Session): Database session dependency.

    Returns:
        dict: Status of acceptance and current event metrics.
    """
    logger.info(
        f"Security Event Received: "
        f"{log.event_type} from {log.source_ip} at {log.timestamp}"
    )
    
    store_raw_security_event(log, db)
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
    }
