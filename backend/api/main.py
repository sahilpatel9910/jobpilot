from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from scraper.seek_scraper import SeekScraper
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(
    title="JobPilot API",
    description="Automated job discovery and tracking API",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def health_check():
    return {"status": "JobPilot API is running 🚀"}


@app.post("/scraper/run")
def run_scraper():
    """
    Triggers a fresh Seek scrape using config from .env
    Returns all scraped jobs as JSON
    """
    try:
        keywords_raw = os.getenv("SEEK_KEYWORDS", "full stack developer,software developer")
        keywords = [k.strip() for k in keywords_raw.split(",")]
        location = os.getenv("SEEK_LOCATION", "Melbourne VIC")

        scraper = SeekScraper(keywords=keywords, location=location, max_pages=2)
        jobs = scraper.scrape()

        return {
            "success": True,
            "total": len(jobs),
            "jobs": [job.model_dump() for job in jobs]
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
