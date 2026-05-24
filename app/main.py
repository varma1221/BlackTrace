from fastapi import FastAPI
from datetime import datetime, timezone

app = FastAPI()

@app.get("/")
def root():
    return {
        "project": "BlackTrace",
        "status": "active",
        "message": "BlackTrace backend initialized successfully"
    }

@app.get("/health")
def health_check():
    return {
        "status": "Healthy",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "service": "BlackTrace API"
    }
