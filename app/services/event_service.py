"""
Security event persistence services.

provides database operations for storing and retrieving raw
security telemetry within the BlackTrace platform.
"""

from sqlalchemy.orm import Session
from app.database.models import SecurityEvent
from app.schemas.log_schema import SecurityLog

def store_raw_security_event(log: SecurityLog, db: Session):
    """
    Persists a raw security event before threat analysis execution.

    Args:
        log (SecurityLog): Validated incoming security event payload.
        db (Session): Active SQLAlchemy database session.

    Return:
        SecurityEvent: Persisted ORM instance representing the stored security event.
    """

    security_event = SecurityEvent(
        source_ip=log.source_ip,
        event_type=log.event_type,
        severity=log.severity,
        message=log.message,
        event_timestamp=log.timestamp
    )

    db.add(security_event)
    db.commit()
    db.refresh(security_event)

    return security_event
