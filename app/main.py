
from fastapi import FastAPI
from datetime import datetime, timezone

app = FastAPI(title="AWS Systems Engineering Lab")

@app.get("/")
def home():
    return {
        "message": "AWS Systems Engineering Lab",
        "status": "running"
    }

@app.get("/health")
def health():
    return {
        "status": "healthy",
        "timestamp": datetime.now(timezone.utc).isoformat()
    }
