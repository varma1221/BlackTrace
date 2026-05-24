from fastapi import FastAPI
from app.routes.health import router as health_router
from app.core.logging_config import logger

app = FastAPI(
        title="BlackTrace",
        description="AI-Powered Cyber Defence and Threat Hunting System",
        version="0.1.0"
)

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
