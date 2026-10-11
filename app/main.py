
import os
from datetime import datetime, timezone

import psycopg
from fastapi import FastAPI, HTTPException


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


@app.get("/ready")
def readiness():
    try:
        with psycopg.connect(
            os.environ["DATABASE_URL"],
            connect_timeout=3
        ) as conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT 1")
                cursor.fetchone()

        return {
            "status": "ready",
            "database": "connected"
        }

    except (psycopg.Error, OSError):
        raise HTTPException(
            status_code=503,
            detail="Database unavailable"
        )

from pydantic import BaseModel, Field

class IncidentCreate(BaseModel):
    title: str = Field(min_length=1, max_length=150)
    severity: str = Field(pattern=r"^SEV-[1-4]$")


@app.post("/incidents", status_code=201)
def create_incident(incident: IncidentCreate):
    with psycopg.connect(os.environ["DATABASE_URL"]) as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO incident_tickets (title, severity)
                VALUES (%s, %s)
                RETURNING id, title, severity, status
                """,
                (incident.title, incident.severity)
            )
            row = cursor.fetchone()

    return {
        "id": row[0],
        "title": row[1],
        "severity": row[2],
        "status": row[3]
    }


@app.get("/incidents")
def list_incidents():
    with psycopg.connect(os.environ["DATABASE_URL"]) as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                SELECT id, title, severity, status
                FROM incident_tickets
                ORDER BY id
                """
            )
            rows = cursor.fetchall()

    return [
        {
            "id": row[0],
            "title": row[1],
            "severity": row[2],
            "status": row[3]
        }
        for row in rows
    ]
