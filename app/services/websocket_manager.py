"""
WebSocket connection manager for real-time SOC streaming.

Handles client registration, lifecycle management, and asynchronous
message broadcasting for live security alerts.
"""
from fastapi import WebSocket

class ConnectionManager:
    """
    Manages active WebSocket connections for the application.

    Attributes:
        active_connections (list[WebSocket]): Registry of currently connected clients.
    """
    def __init__(self):
        self.active_connections = []

    async def connect(self, websocket: WebSocket): # Represents connected dashboard client
        """
        Accepts and registers a new WebSocket client connection.

        Args:
            websocket (WebSocket): The client connection to register.
        """
        await websocket.accept()
        self.active_connections.append(
            websocket
        )
    
    def disconnect( self, websocket: WebSocket):
        """
        Removes a WebSocket client from the active registry.

        Args:
            websocket (WebSocket): The client connection to remove.
        """
        self.active_connections.remove(websocket)
    
    async def broadcast(self, message: dict): # Deletes disconnected client from registry
        """
        Broadcasts a JSON payload to all registered WebSocket clients.

        Args:
            message (dict): The data payload to send to clients.
        """
        for connection in self.active_connections:
            await connection.send_json(
                message
            )

manager = ConnectionManager() # Creates single shared manager object
