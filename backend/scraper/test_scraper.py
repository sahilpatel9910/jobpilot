"""
Run this script to test the Seek scraper manually.

Usage (from the /backend folder):
    python -m scraper.test_scraper

It will scrape Seek for your target roles and print
every result to the terminal in a readable format.
"""

import json
from scraper.seek_scraper import SeekScraper

# ─── Config ───────────────────────────────────────────────────────────────────
# Adjust these to match what you're searching for

KEYWORDS = [
    "full stack developer",
    "software developer",
    "junior developer",
]

LOCATION = "Melbourne VIC"
MAX_PAGES = 2  # Keep low for testing — 2 pages = ~44 jobs per keyword


# ─── Run ──────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("=" * 60)
    print("🚀 JobPilot — Seek Scraper Test Run")
    print("=" * 60)

    scraper = SeekScraper(
        keywords=KEYWORDS,
        location=LOCATION,
        max_pages=MAX_PAGES
    )

    jobs = scraper.scrape()

    print("\n" + "=" * 60)
    print(f"📋 Results Summary — {len(jobs)} jobs found")
    print("=" * 60)

    for i, job in enumerate(jobs, 1):
        print(f"\n[{i}] {job.title}")
        print(f"    🏢 {job.company}")
        print(f"    📍 {job.location}")
        print(f"    💰 {job.salary or 'Salary not listed'}")
        print(f"    🕒 {job.job_type or 'Type not listed'}")
        print(f"    📅 {job.date_posted or 'Date not listed'}")
        print(f"    🔗 {job.apply_url}")
        print(f"    📝 {job.description_snippet[:100]}...")

    # Also save to a JSON file so you can inspect the raw data
    output_path = "scraper/test_output.json"
    with open(output_path, "w") as f:
        json.dump([job.model_dump() for job in jobs], f, indent=2)

    print(f"\n💾 Full results saved to: {output_path}")
    print("=" * 60)
