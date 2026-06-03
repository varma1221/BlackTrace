"""
WebSocket routes for real-time alert streaming.

Provides bidirectional communication for live updates to the SOC dashboard.
"""
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from app.services.websocket_manager import manager

router = APIRouter()

@router.websocket("/ws/alerts")
async def websocket_alert_stream(websocket: WebSocket):
    """
    Manages a WebSocket connection for live security broadcasting.

    Args:
        websocket (WebSocket): The incoming client connection.
    """
    await manager.connect(websocket)

    try:
        while True:
            await websocket.receive_text()
    
    except WebSocketDisconnect:
        manager.disconnect(websocket)
