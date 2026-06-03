"""
Service for alert orchestration and persistence.

Handles the conversion of detection results into database records and
manages real-time event broadcasting to connected clients.
"""
from datetime import datetime, timezone
from sqlalchemy.orm import Session
from app.schemas.alert_schema import SecurityAlert
from app.core.logging_config import logger
from app.services.severity_engine import calculate_severity
from app.services.websocket_manager import manager
from app.database.models import Alert
import asyncio

def create_alert(threat_analysis, db: Session):
    """
    Creates a security alert and triggers real-time notifications.

    Persists the alert to the database and schedules an asynchronous
    broadcast to all active WebSocket clients.

    Args:
        threat_analysis (dict): Data from the threat detection engine.
        db (Session): Database session for alert persistence.

    Returns:
        SecurityAlert: Pydantic model representation of the generated alert.
    """
    alert = Alert(
        threat_type=threat_analysis["threat_type"],
        source_ip=threat_analysis["source_ip"],
        severity=calculate_severity(threat_analysis),
        status="Active",
        timestamp=datetime.now(timezone.utc),
        recommended_action=threat_analysis[
            "recommended_action"
        ]
    )
    
    db.add(alert)
    db.commit()
    db.refresh(alert)
    
    logger.warning(
        f"Security alert created: "
        f"{alert.threat_type}"
        f"(Alert ID: {alert.alert_id})"
    )

    asyncio.create_task(
        manager.broadcast(
            {
                "event": "new_alert",
                "alert": {
                    "alert_id": alert.alert_id,
                    "threat_type": (
                        alert.threat_type
                    ),
                    "severity": (
                        alert.severity
                    ),
                    "source_ip": (
                        alert.source_ip
                    ),
                    "status": alert.status
                }
            }
        )
    )
    
    return SecurityAlert(
        alert_id=alert.alert_id,
        threat_type=alert.threat_type,
        source_ip=alert.source_ip,
        severity=alert.severity,
        status=alert.status,
        timestamp=alert.timestamp,
        recommended_action=alert.recommended_action
    )
