"""
Operational metrics for SOC monitoring.

Provides aggregated statistics on alert volume and severity distribution
for security dashboarding.
"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.database.models import Alert
from app.database.session import get_db
from app.security.auth import verify_api_key

router = APIRouter()

@router.get("/metrics/dashboard")
def get_security_dashboard_metrics(
    db: Session = Depends(get_db),
    api_key: str = Depends(verify_api_key)
):
    """
    Aggregates high-level alert statistics for the dashboard.

    Args:
        db (Session): Database session dependency.
        api_key (str): Verified API key for authentication.

    Returns:
        dict: Counts of total, active, resolved, and critical alerts.
    """
    total_alerts = db.query(Alert).count()
    
    active_alerts = db.query(Alert).filter(
        Alert.status == "active"
    ).count()
    
    resolved_alerts = db.query(Alert).filter(
        Alert.status == "resolved"
    ).count()
    
    critical_alerts = db.query(Alert).filter(
        Alert.severity == "critical"
    ).count()
    
    return {
        "total_alerts": total_alerts,
        "active_alerts": active_alerts,
        "resolved_alerts": resolved_alerts,
        "critical_alerts": critical_alerts
    }

@router.get("/metrics/severity-distribution")
def get_severity_distribution(
    db: Session = Depends(get_db),
    api_key: str = Depends(verify_api_key)
):
    """
    Calculates the distribution of alerts across all severity levels.

    Args:
        db (Session): Database session dependency.
        api_key (str): Verified API key for authentication.

    Returns:
        dict: A list of severity levels and their corresponding counts.
    """
    severity_counts = db.query(
        Alert.severity,
        func.count(Alert.alert_id)
    ).group_by(
        Alert.severity
    ).all()
    
    return {
        "severity-distribution": [
            {
                "severity": severity,
                "count": count               
            }    
            for severity, count in severity_counts
        ]
    }
