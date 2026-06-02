"""
Security metrics and SOC dashboard routes.

This module provides operational security statistics
used for SOC dashboards and monitoring systems.
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.database.models import Alert
from app.database.session import get_db

router = APIRouter()

@router.get("/metrics/dashboard")
def get_security_dashboard_metrics(
    db: Session = Depends(get_db)
):
    
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
    db: Session = Depends(get_db)
):
    
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
