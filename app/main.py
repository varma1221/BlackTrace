from fastapi import FastAPI
from app.routes.health import router as health_router

app = FastAPI(
        title="BlackTrace",
        description="AI-Powered Cyber Defence and Threat Hunting System",
        version="0.1.0"
)

@app.get("/")
def root():
    return {
        "project": "BlackTrace",
        "status": "active",
        "message": "BlackTrace backend initialized successfully"
    }

app.include_router(health_router)
