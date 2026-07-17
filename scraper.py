import feedparser
import requests
from bs4 import BeautifulSoup
from db.database import SessionLocal
from db.models import Startup, Event
import datetime

# Using TechCrunch RSS feed for mock data if needed, or we can seed dummy startups
RSS_FEED_URL = "https://techcrunch.com/feed/"

def fetch_rss_news():
    """Fetches news from an RSS feed to simulate startup monitoring"""
    feed = feedparser.parse(RSS_FEED_URL)
    events = []
    for entry in feed.entries[:5]: # Take top 5 recent news
        events.append({
            "title": entry.title,
            "summary": entry.summary,
            "link": entry.link,
            "published": entry.published
        })
    return events

def seed_dummy_startups(db):
    """Seed the database with some dummy startups to demonstrate the system"""
    startups_data = [
        {"name": "NeuroLumina", "description": "AI hardware for edge computing.", "website": "neurolumina.ai", "industry": "AI Hardware"},
        {"name": "EcoChain", "description": "Blockchain for carbon tracking.", "website": "ecochain.io", "industry": "CleanTech"},
        {"name": "QuantumSphere", "description": "Quantum encryption algorithms.", "website": "quantumsphere.co", "industry": "Cybersecurity"},
    ]
    
    for s_data in startups_data:
        existing = db.query(Startup).filter(Startup.name == s_data["name"]).first()
        if not existing:
            new_startup = Startup(**s_data)
            db.add(new_startup)
    db.commit()

def run_scraper():
    print("Running scraper agent...")
    db = SessionLocal()
    
    # 1. Seed dummy startups if DB is empty
    seed_dummy_startups(db)
    
    # 2. Add some dummy events to these startups
    startups = db.query(Startup).all()
    
    if startups:
        # Check if events already exist
        if not db.query(Event).first():
            # Add a funding event to NeuroLumina
            nl = next((s for s in startups if s.name == "NeuroLumina"), None)
            if nl:
                event = Event(
                    startup_id=nl.id,
                    event_type="Funding",
                    title="NeuroLumina raises $15M Series A",
                    description="NeuroLumina today announced it has raised $15 million in a Series A round led by Sequoia.",
                    date=datetime.datetime.utcnow(),
                    source_url="https://mock-news.com/neurolumina-funding"
                )
                db.add(event)
            
            # Add a Launch event to EcoChain
            ec = next((s for s in startups if s.name == "EcoChain"), None)
            if ec:
                event = Event(
                    startup_id=ec.id,
                    event_type="Launch",
                    title="EcoChain launches new API",
                    description="EcoChain has launched a new enterprise API for tracking carbon footprints.",
                    date=datetime.datetime.utcnow(),
                    source_url="https://mock-news.com/ecochain-launch"
                )
                db.add(event)

            # Add an Acquisition event to QuantumSphere
            qs = next((s for s in startups if s.name == "QuantumSphere"), None)
            if qs:
                event = Event(
                    startup_id=qs.id,
                    event_type="Hiring",
                    title="QuantumSphere hires ex-Google security chief",
                    description="QuantumSphere bolsters its leadership team by hiring an industry veteran.",
                    date=datetime.datetime.utcnow(),
                    source_url="https://mock-news.com/qs-hiring"
                )
                db.add(event)
            
            db.commit()

    print("Scraper agent finished.")
    db.close()

if __name__ == "__main__":
    run_scraper()
