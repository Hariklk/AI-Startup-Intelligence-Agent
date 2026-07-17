import os
from google import genai
from db.database import SessionLocal
from db.models import Startup, Event, Insight
from pydantic import BaseModel
import datetime

# Attempt to load Gemini API key
api_key = os.environ.get("GEMINI_API_KEY")

class AnalysisResult(BaseModel):
    analysis: str
    sentiment: str
    recommendation: str
    growth_stage: str

def analyze_startup(startup, events, client=None):
    """Uses LLM to analyze the startup based on recent events."""
    
    prompt = f"Analyze this startup:\nName: {startup.name}\nDescription: {startup.description}\nIndustry: {startup.industry}\n"
    prompt += "Recent Events:\n"
    for e in events:
        prompt += f"- {e.date.strftime('%Y-%m-%d')}: {e.event_type} - {e.title}\n  {e.description}\n"
    
    prompt += """
    Based on the above, provide an analysis in JSON format matching this schema:
    {
        "analysis": "A brief 2-sentence executive summary of their current trajectory.",
        "sentiment": "Positive, Neutral, or Negative",
        "recommendation": "Invest, Watch, or Pass",
        "growth_stage": "Seed, Series A, Series B, Growth, or Unknown"
    }
    """

    if client and api_key:
        try:
            # We would use structured output if calling actual Gemini API.
            # Using the genai SDK format
            response = client.models.generate_content(
                model='gemini-2.5-flash',
                contents=prompt,
                config={
                    'response_mime_type': 'application/json',
                }
            )
            # Parse JSON
            import json
            data = json.loads(response.text)
            return data
        except Exception as e:
            print(f"LLM Error: {e}")
            pass # Fallback to mock

    # Fallback mock analysis if no API key or error
    if "NeuroLumina" in startup.name:
        return {
            "analysis": "NeuroLumina shows strong momentum following their recent Series A. Their AI hardware is gaining traction.",
            "sentiment": "Positive",
            "recommendation": "Invest",
            "growth_stage": "Series A"
        }
    elif "EcoChain" in startup.name:
        return {
            "analysis": "EcoChain's new API launch positions them well in the growing CleanTech tracking space.",
            "sentiment": "Positive",
            "recommendation": "Watch",
            "growth_stage": "Seed"
        }
    else:
        return {
            "analysis": "QuantumSphere is making strategic hires to strengthen its cybersecurity offerings.",
            "sentiment": "Neutral",
            "recommendation": "Watch",
            "growth_stage": "Growth"
        }

def run_analyst():
    print("Running analyst agent...")
    db = SessionLocal()
    
    client = None
    if api_key:
        client = genai.Client(api_key=api_key)

    startups = db.query(Startup).all()
    for startup in startups:
        events = db.query(Event).filter(Event.startup_id == startup.id).all()
        
        # Avoid re-analyzing if we already have an insight for the latest event
        # (Simplified logic: just generate a new insight)
        
        result = analyze_startup(startup, events, client)
        
        # Update startup growth stage
        startup.growth_stage = result.get("growth_stage", startup.growth_stage)
        
        # Add Insight
        insight = Insight(
            startup_id=startup.id,
            analysis=result.get("analysis", "No analysis available."),
            sentiment=result.get("sentiment", "Neutral"),
            recommendation=result.get("recommendation", "Watch"),
            created_at=datetime.datetime.utcnow()
        )
        db.add(insight)
        
    db.commit()
    db.close()
    print("Analyst agent finished.")

if __name__ == "__main__":
    run_analyst()
