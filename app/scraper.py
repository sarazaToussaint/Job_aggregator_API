import requests
import json
from datetime import datetime, timedelta, UTC


class RemoteOKScraper:
    API_URL = "https://remoteok.com/api"

    def fetch_jobs(self):
        headers = {
            "User-Agent": "Mozilla/5.0"
        }
        response = requests.get(self.API_URL, headers=headers)
        response.raise_for_status()
        jobs = response.json()
        # Filter jobs from last 7 days (timezone-aware)
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
        for job in filtered_jobs:
            title = job.get("position", "No title")
            company = job.get("company", "Unknown")
            location = job.get("location", "Unknown")
            url = job.get("url", "-")
            description = job.get("description", "-")
            posted_date = job.get("date", "-")
            tags = job.get("tags", [])
            is_remote = "remote" in (location or "").lower() or "remote" in [
                t.lower() for t in tags]
            source = "remoteok"

            print(f"Title: {title}")
            print(f"Company: {company}")
            print(f"Location: {location}")
            print(f"URL: {url}")
            print(
                f"Description: {description[:200]}{'...' if len(description) > 200 else ''}")
            print(f"Posted: {posted_date}")
            print(f"Tags: {', '.join(tags)}")
            print(f"Source: {source}")
            print(f"Is Remote: {is_remote}")
            print("-"*40)


if __name__ == "__main__":
    scraper = RemoteOKScraper()
    scraper.fetch_jobs()
