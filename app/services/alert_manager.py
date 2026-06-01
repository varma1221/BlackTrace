"""
Alert management service for BlackTrace.

This module creates structured security alerts from threat detection
results and stores them for retrieval through alert APIs.
"""
from datetime import datetime, timezone
from sqlalchemy.orm import Session
from app.schemas.alert_schema import SecurityAlert
from app.core.logging_config import logger
from app.services.severity_engine import calculate_severity
from app.database.models import Alert

def create_alert(threat_analysis, db: Session):
    """
    Create and store a security alert from a detection result.

    The alert is assigned an ID, severity, active status, UTC timestamp,
    and recommended response action before being added to the alert store.
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
    
    return SecurityAlert(
        alert_id=alert.alert_id,
        threat_type=alert.threat_type,
        source_ip=alert.source_ip,
        severity=alert.severity,
        status=alert.status,
        timestamp=alert.timestamp,
        recommended_action=alert.recommended_action
    )
