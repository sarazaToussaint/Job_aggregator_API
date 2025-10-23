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
        # Filter jobs from last 15 days (timezone-aware)
        date_cutoff = datetime.now(UTC) - timedelta(days=15)
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
        print(f"Found {len(filtered_jobs)} jobs from last 15 days")
        for job in filtered_jobs:
            print(job.get("position", "No title"))


if __name__ == "__main__":
    scraper = RemoteOKScraper()
    scraper.fetch_jobs()
