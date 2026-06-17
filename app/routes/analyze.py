from fastapi import APIRouter
from pydantic import BaseModel

from typing import Dict, Union

from detection_engine.inference import predict_telemetry
from intelligence.workflow import intelligence_workflow

router = APIRouter()

class TelemetryRequest(BaseModel):
    telemetry: Dict[str, Union[str, float, int]]

@router.post("/analyze")
def analyze_telemetry(request: TelemetryRequest):
    """
    Analyze incoming telemetry using BlackTrace ML inference pipeline.
    """

    predict_result = predict_telemetry(request.telemetry)
    intelligence_result = intelligence_workflow.invoke(
        {
            "alert": predict_result
        }
    )

    return {
        "status": "success",
        "detection": predict_result,
        "incident_analysis": intelligence_result["incident_report"],
        "recommendations": intelligence_result["recommendations"]
    }
