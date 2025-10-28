import requests
import json
from datetime import datetime, timedelta, UTC
from app.db import SessionLocal
from app import schemas, crud


class RemoteOKScraper:
    API_URL = "https://remoteok.com/api"

    def fetch_jobs(self, persist: bool = True):
        headers = {
            "User-Agent": "Mozilla/5.0"
        }
        response = requests.get(self.API_URL, headers=headers)
        response.raise_for_status()
        jobs = response.json()
        # Filter jobs from last 2 days (timezone-aware)
        date_cutoff = datetime.now(UTC) - timedelta(days=2)
        filtered_jobs = []
        for job in jobs[1:]:  # skip metadata
            job_date_str = job.get("date")
            if job_date_str:
                try:
                    job_date = datetime.fromisoformat(
                        job_date_str.replace("Z", "+00:00")).astimezone(UTC)
                except Exception:
                    continue
                if job_date >= date_cutoff:
                    filtered_jobs.append(job)
        print(f"Found {len(filtered_jobs)} jobs from last 2 days\n")
        if persist:
            db = SessionLocal()
            existing_urls = set(j.url for j in crud.jobs.get_jobs(db))
        for job in filtered_jobs:
            title = job.get("position", "No title")
            company = job.get("company", "Unknown")
            location = job.get("location", "Unknown")
            url = job.get("url", "-")
            description = job.get("description", None)
            posted_date = None
            try:
                posted_date = datetime.fromisoformat(
                    job.get("date").replace("Z", "+00:00")).astimezone(UTC)
            except Exception:
                pass
            tags = job.get("tags", [])
            is_remote = "remote" in (location or "").lower() or "remote" in [
                t.lower() for t in tags]
            source = "remoteok"

            print(f"Title: {title}")
            print(f"Company: {company}")
            print(f"Location: {location}")
            print(f"URL: {url}")
            print(
                f"Description: {description[:200]}{'...' if description and len(description) > 200 else ''}")
            print(f"Posted: {posted_date}")
            print(f"Tags: {', '.join(tags)}")
            print(f"Source: {source}")
            print(f"Is Remote: {is_remote}")
            print("-"*40)

            if persist:
                existing_job = crud.jobs.get_job_by_url(db, url)
                if existing_job:
                    print(f"Job already exists, skipping: {title}")
                else:
                    job_create = schemas.JobCreate(
                        title=title,
                        company=company,
                        location=location,
                        url=url,
                        description=description,
                        posted_date=posted_date,
                        source=source,
                        tags=tags,
                        is_remote=is_remote
                    )
                    crud.jobs.create_job(db, job_create)
                    print(f"Saved new job to DB: {title}")
        if persist:
            db.close()


if __name__ == "__main__":
    scraper = RemoteOKScraper()
    scraper.fetch_jobs()
