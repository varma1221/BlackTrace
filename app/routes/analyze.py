from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.database.session import get_db

from typing import Dict, Union

from detection_engine.inference import predict_telemetry
from intelligence.workflow import intelligence_workflow
from app.services.intelligence_service import save_intelligence_report

router = APIRouter()

class TelemetryRequest(BaseModel):
    telemetry: Dict[str, Union[str, float, int]]

@router.post("/analyze")
def analyze_telemetry(request: TelemetryRequest, db: Session = Depends(get_db)):
    """
    Analyze incoming telemetry using BlackTrace ML inference pipeline.
    """

    predict_result = predict_telemetry(request.telemetry)
    intelligence_result = intelligence_workflow.invoke(
        {
            "alert": predict_result
        }
    )

    save_intelligence_report(
        db=db,
        alert_id=1, #Temporary placeholder
        incident_analysis=intelligence_result["incident_report"],
        recommendations=intelligence_result["recommendations"]
    )

    return {
        "status": "success",
        "detection": predict_result,
        "incident_analysis": intelligence_result["incident_report"],
        "recommendations": intelligence_result["recommendations"]
    }
