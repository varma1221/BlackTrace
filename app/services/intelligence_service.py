import json
from app.database.models import IntelligenceReport

def save_intelligence_report(db, alert_id, incident_analysis, recommendations):
    """
    Persist AI-generated intelligence linked to a specific alert
    """

    report = IntelligenceReport(
        alert_id=alert_id,
        incident_analysis=json.dumps(incident_analysis),
        recommendations=json.dumps(recommendations)
    )

    db.add(report)
    db.commit()
    db.refresh(report)

    return report
