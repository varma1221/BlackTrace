"""
Entry point for the BlackTrace API.

This module initializes the FastAPI application, configures global middleware,
and registers all service-layer routers. It also handles initial database
schema synchronization during startup.
"""
from fastapi import FastAPI
from app.routes.health import router as health_router
from app.core.logging_config import logger
from app.core.middleware import RequestLoggingMiddleware
from app.routes.logs import router as logs_router
from app.routes.alerts import router as alerts_router
from app.routes.metrics import router as metrics_router
from app.routes.stream import router as stream_router
from app.routes.analyze import router as analyze_router
from app.routes.intelligence import router as intelligence_router
from app.database.connection import engine
from app.database.models import Base

app = FastAPI(
        title="BlackTrace API",
        description="AI-Powered Cyber Defence and Threat Hunting System",
        version="0.1.0"
)

app.add_middleware(RequestLoggingMiddleware)
logger.info("BlackTrace API initialized")

@app.get("/")
def root():
    """
    Root endpoint for basic service health and metadata.

    Returns:
        dict: A dictionary containing project name, status, and greeting.
    """
    logger.info("Root endpoint accessed")
    
    return {
        "project": "BlackTrace",
        "status": "Active",
        "message": "BlackTrace backend initialized successfully."
    }

app.include_router(health_router)
app.include_router(logs_router)
app.include_router(alerts_router)
app.include_router(metrics_router)
app.include_router(stream_router)
app.include_router(analyze_router)
app.include_router(intelligence_router)
Base.metadata.create_all(bind=engine)
