from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List

from db import models, database

# Create tables
models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(title="AI Startup Intelligence API")

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def read_root():
    return {"message": "AI Startup Intelligence API is running"}

@app.get("/api/startups")
def get_startups(db: Session = Depends(get_db)):
    startups = db.query(models.Startup).all()
    # We will format this to include related events and insights
    result = []
    for startup in startups:
        events = db.query(models.Event).filter(models.Event.startup_id == startup.id).all()
        insights = db.query(models.Insight).filter(models.Insight.startup_id == startup.id).all()
        
        result.append({
            "id": startup.id,
            "name": startup.name,
            "description": startup.description,
            "website": startup.website,
            "growth_stage": startup.growth_stage,
            "industry": startup.industry,
            "events": [{"type": e.event_type, "title": e.title, "date": e.date} for e in events],
            "insight": insights[-1].analysis if insights else "Analysis pending...",
            "recommendation": insights[-1].recommendation if insights else "Neutral"
        })
    return result

@app.post("/api/trigger_collection")
def trigger_collection():
    # This will trigger our agents. For now, it's a placeholder.
    from agents.scraper import run_scraper
    from agents.analyst import run_analyst
    
    # Run pipeline
    run_scraper()
    run_analyst()
    
    return {"message": "Data collection and analysis triggered successfully"}
