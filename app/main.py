"""
Main FastAPI application setup for BlackTrace.

This module creates the API app, attaches request logging middleware,
and registers all route modules used by the backend.
"""
from fastapi import FastAPI
from app.routes.health import router as health_router
from app.core.logging_config import logger
from app.core.middleware import RequestLoggingMiddleware
from app.routes.logs import router as logs_router
from app.routes.alerts import router as alerts_router

app = FastAPI(
        title="BlackTrace API",
        description="AI-Powered Cyber Defence and Threat Hunting System",
        version="0.1.0"
)

app.add_middleware(RequestLoggingMiddleware)
logger.info("BlackTrace API initialized")

@app.get("/")
def root():
    logger.info("Root endpoint accessed")
    
    return {
        "project": "BlackTrace",
        "status": "active",
        "message": "BlackTrace backend initialized successfully"
    }

app.include_router(health_router)
app.include_router(logs_router)
app.include_router(alerts_router)
