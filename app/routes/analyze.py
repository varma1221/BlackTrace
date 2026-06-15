from fastapi import APIRouter
from pydantic import BaseModel

from typing import Dict, Union

from detection_engine.inference import predict_telemetry

router = APIRouter()

class TelemetryRequest(BaseModel):
    telemetry: Dict[str, Union[str, float, int]]

@router.post("/analyze")
def analyze_telemetry(request: TelemetryRequest):
    """
    Analyze incoming telemetry using BlackTrace ML inference pipeline.
    """

    prediction_result = predict_telemetry(request.telemetry)

    return {
        "status": "success",
        "detection": prediction_result
    }
