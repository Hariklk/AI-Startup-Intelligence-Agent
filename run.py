from agents.scraper import run_scraper
from agents.analyst import run_analyst
from core.reporter import generate_markdown_report, generate_csv_export
import sys

def main():
    print("=== AI Startup Intelligence Pipeline ===")
    
    print("\n[1/3] Running Data Collection...")
    run_scraper()
    
    print("\n[2/3] Running AI Analysis...")
    run_analyst()
    
    print("\n[3/3] Generating Reports...")
    generate_markdown_report()
    generate_csv_export()
    
    print("\n=== Pipeline Complete ===")

if __name__ == "__main__":
    main()
