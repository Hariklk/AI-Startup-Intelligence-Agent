from db.database import SessionLocal
from db.models import Startup, Insight
import pandas as pd
import datetime
import os

def generate_markdown_report():
    db = SessionLocal()
    startups = db.query(Startup).all()
    
    report_path = "executive_report.md"
    
    with open(report_path, "w") as f:
        f.write("# AI Startup Intelligence: Executive Report\n\n")
        f.write(f"**Generated on:** {datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')}\n\n")
        f.write("## Overview\n")
        f.write("This report provides automated insights into key startups tracked by the intelligence system.\n\n")
        
        for startup in startups:
            f.write(f"### {startup.name}\n")
            f.write(f"**Industry:** {startup.industry} | **Stage:** {startup.growth_stage} | **Website:** [{startup.website}](http://{startup.website})\n\n")
            f.write(f"> {startup.description}\n\n")
            
            latest_insight = db.query(Insight).filter(Insight.startup_id == startup.id).order_by(Insight.created_at.desc()).first()
            if latest_insight:
                f.write(f"**AI Analysis:** {latest_insight.analysis}\n\n")
                f.write(f"**Sentiment:** {latest_insight.sentiment} | **Recommendation:** {latest_insight.recommendation}\n\n")
            else:
                f.write("*No insights generated yet.*\n\n")
                
            f.write("---\n")
            
    print(f"Executive report generated successfully at {os.path.abspath(report_path)}")
    db.close()
    
def generate_csv_export():
    db = SessionLocal()
    startups = db.query(Startup).all()
    
    data = []
    for startup in startups:
        latest_insight = db.query(Insight).filter(Insight.startup_id == startup.id).order_by(Insight.created_at.desc()).first()
        data.append({
            "Name": startup.name,
            "Industry": startup.industry,
            "Growth Stage": startup.growth_stage,
            "Website": startup.website,
            "Description": startup.description,
            "AI Analysis": latest_insight.analysis if latest_insight else "",
            "Sentiment": latest_insight.sentiment if latest_insight else "",
            "Recommendation": latest_insight.recommendation if latest_insight else ""
        })
        
    df = pd.DataFrame(data)
    csv_path = "startup_export.csv"
    df.to_csv(csv_path, index=False)
    print(f"Data exported successfully to {os.path.abspath(csv_path)}")
    db.close()

if __name__ == "__main__":
    generate_markdown_report()
    generate_csv_export()
