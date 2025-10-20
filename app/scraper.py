import requests

class RemoteOKScraper:
    API_URL = "https://remoteok.com/api"

    def fetch_jobs(self):
        headers = {
            "User-Agent": "Mozilla/5.0"
        }
        response = requests.get(self.API_URL, headers=headers)
        response.raise_for_status()
        jobs = response.json()
        print(f"Found {len(jobs)-1} jobs")  # First entry is metadata
        for job in jobs[1:]:
            print(job.get("position", "No title"))

if __name__ == "__main__":
    scraper = RemoteOKScraper()
    scraper.fetch_jobs()
