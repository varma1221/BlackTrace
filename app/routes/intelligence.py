import json

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.database.models import IntelligenceReport

router = APIRouter(prefix="/intelligence", tags=["intelligence"])

@router.get("/")
def get_intelligence_reports(db: Session = Depends(get_db)):
    reports = (db.query(IntelligenceReport).order_by(IntelligenceReport.report_id.desc()).all())
    result = []

    for report in reports:
        result.append(
            {
                "report_id": report.report_id,
                "alert_id": report.alert_id,
                "incident_analysis": json.loads(report.incident_analysis),
                "recommendations": json.loads(report.recommendations),
                "created_at": report.created_at
            }
        )
    return result

@router.get("/{report_id}")
def get_intelligence_report(report_id: int, db: Session = Depends(get_db)):
    report = (db.query(IntelligenceReport).filter(IntelligenceReport.report_id == report_id).first())

    return {
        "report_id": report.report_id,
        "alert_id": report.alert_id,
        "incident_analysis": json.loads(
            report.incident_analysis
        ),
        "recommendations": json.loads(
            report.recommendations
        ),
        "created_at": report.created_at
    }
