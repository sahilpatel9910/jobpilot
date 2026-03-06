from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class JobListing(BaseModel):
    job_id: str                        # Unique ID derived from Seek listing URL
    title: str                         # Job title e.g. "Full Stack Developer"
    company: str                       # Company name
    location: str                      # e.g. "Melbourne VIC"
    salary: Optional[str] = None       # e.g. "$80,000 - $100,000" (not always listed)
    job_type: Optional[str] = None     # e.g. "Full Time", "Contract"
    description_snippet: str           # Short preview of the job description
    apply_url: str                     # Direct link to apply
    date_posted: Optional[str] = None  # When the job was listed
    scraped_at: str = datetime.utcnow().isoformat()  # When we scraped it
    status: str = "new"                # new | saved | applied | interviewing | rejected
    match_score: Optional[int] = None  # 0-100, filled in Phase 4
