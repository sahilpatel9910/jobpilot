import requests
import hashlib
import os
from datetime import datetime
from typing import List, Optional
from dotenv import load_dotenv
from .models import JobListing

load_dotenv()

# ─── Constants ────────────────────────────────────────────────────────────────

# Adzuna's Australian API endpoint
# Results per page — Adzuna allows up to 50
ADZUNA_BASE_URL = "https://api.adzuna.com/v1/api/jobs/au/search"
RESULTS_PER_PAGE = 20


# ─── Helpers ──────────────────────────────────────────────────────────────────

def generate_job_id(url: str) -> str:
    """
    Creates a unique, consistent ID for each job by hashing its URL.
    This means the same job will always produce the same ID —
    which is how we deduplicate listings across multiple scrape runs.
    """
    return hashlib.md5(url.encode()).hexdigest()[:12]


def format_salary(minimum: Optional[float], maximum: Optional[float]) -> Optional[str]:
    """
    Adzuna returns salary as two separate numbers (min and max).
    This combines them into a readable string like "$80,000 - $100,000".
    If only one value exists, returns just that value.
    """
    if minimum and maximum:
        return f"${int(minimum):,} - ${int(maximum):,}"
    elif minimum:
        return f"From ${int(minimum):,}"
    elif maximum:
        return f"Up to ${int(maximum):,}"
    return None


# ─── Core Fetcher ─────────────────────────────────────────────────────────────

class SeekScraper:
    """
    Despite the class name (kept for consistency with the rest of the codebase),
    this now uses the Adzuna API instead of scraping Seek directly.
    Adzuna aggregates jobs from Seek and other Australian job boards.
    """

    def __init__(self, keywords: List[str], location: str, max_pages: int = 3):
        """
        keywords  : list of search terms e.g. ["full stack developer", "software engineer"]
        location  : location string e.g. "Melbourne VIC"
        max_pages : pages to fetch per keyword (20 results per page)
        """
        self.keywords = keywords
        self.location = location
        self.max_pages = max_pages
        self.seen_ids = set()  # Tracks job IDs we've already processed — prevents duplicates

        # Load API credentials from .env
        self.app_id = os.getenv("ADZUNA_APP_ID")
        self.app_key = os.getenv("ADZUNA_APP_KEY")

        if not self.app_id or not self.app_key:
            raise ValueError("Missing ADZUNA_APP_ID or ADZUNA_APP_KEY in .env file")

    def scrape(self) -> List[JobListing]:
        """
        Main entry point. Loops over every keyword + every page,
        fetches all listings from Adzuna, deduplicates, and returns a clean list.
        """
        all_jobs: List[JobListing] = []

        for keyword in self.keywords:
            print(f"\n🔍 Searching: '{keyword}' in {self.location}")

            for page in range(1, self.max_pages + 1):
                print(f"   📄 Page {page}...")

                jobs = self._fetch_page(keyword, page)

                if not jobs:
                    print(f"   ⚠️  No results on page {page}, stopping this keyword.")
                    break

                all_jobs.extend(jobs)
                print(f"   ✅ Found {len(jobs)} jobs (running total: {len(all_jobs)})")

        print(f"\n🎯 Complete. Total unique jobs found: {len(all_jobs)}")
        return all_jobs

    def _fetch_page(self, keyword: str, page: int) -> List[JobListing]:
        """
        Calls the Adzuna API for a single keyword + page combination.
        Adzuna returns clean JSON — no HTML parsing needed.

        API docs: https://developer.adzuna.com/docs/search
        """
        params = {
            "app_id": self.app_id,
            "app_key": self.app_key,
            "results_per_page": RESULTS_PER_PAGE,
            "what": keyword,           # The job title / keywords to search
            "where": self.location,    # Location filter
            "content-type": "application/json",
            "sort_by": "date",         # Get freshest jobs first
        }

        try:
            response = requests.get(
                f"{ADZUNA_BASE_URL}/{page}",
                params=params,
                timeout=10
            )
            response.raise_for_status()
            data = response.json()

        except requests.RequestException as e:
            print(f"   ❌ API request failed: {e}")
            return []

        # Adzuna wraps results in a "results" array
        raw_jobs = data.get("results", [])

        jobs = []
        for raw in raw_jobs:
            job = self._parse_job(raw)
            if job and job.job_id not in self.seen_ids:
                self.seen_ids.add(job.job_id)
                jobs.append(job)

        return jobs

    def _parse_job(self, raw: dict) -> Optional[JobListing]:
        """
        Converts a single raw Adzuna API result (dict) into a JobListing object.
        Adzuna's field names are documented at: https://developer.adzuna.com/docs/search
        """
        try:
            apply_url = raw.get("redirect_url", "")
            job_id = generate_job_id(apply_url)

            # Adzuna nests company and location inside sub-objects
            company = raw.get("company", {}).get("display_name", "Not listed")
            location = raw.get("location", {}).get("display_name", self.location)

            # Salary comes as two separate floats
            salary = format_salary(
                raw.get("salary_min"),
                raw.get("salary_max")
            )

            # Date posted comes as ISO 8601 e.g. "2024-07-01T00:00:00Z"
            # We trim it to just the date part for readability
            created_raw = raw.get("created", "")
            date_posted = created_raw[:10] if created_raw else None

            return JobListing(
                job_id=job_id,
                title=raw.get("title", "Unknown Title"),
                company=company,
                location=location,
                salary=salary,
                job_type=raw.get("contract_time", None),   # "full_time" or "part_time"
                description_snippet=raw.get("description", "No description available.")[:300],
                apply_url=apply_url,
                date_posted=date_posted,
            )

        except Exception as e:
            print(f"   ⚠️  Failed to parse a job result: {e}")
            return None
