from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():
    return {
        "project": "BlackTrace",
        "status": "active",
        "message": "BlackTrace backend initialized successfully"
    }
