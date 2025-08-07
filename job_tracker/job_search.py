import requests
import os
from dotenv import load_dotenv

# Load environment variables from .env or GitHub Secrets
load_dotenv()

# JSearch API config
RAPIDAPI_KEY = os.getenv("RAPIDAPI_KEY")
JSEARCH_URL = "https://jsearch.p.rapidapi.com/search"

HEADERS = {
    "x-rapidapi-host": "jsearch.p.rapidapi.com",
    "x-rapidapi-key": RAPIDAPI_KEY
}

# Check if the job is entry level based on keywords
def is_entry_level(job):
    experience = job.get("job_experience_level", "").lower()
    description = job.get("job_description", "").lower()
    return (
        "entry" in experience
        or "entry-level" in description
        or "entry level" in description
        or "junior" in description
        or "new grad" in description
    )

# Main function to search jobs using JSearch API
def search_jobs(
    titles=None,
    location="",
    pages=2
):
    """
    titles: list of job titles to search
    location: city or region, empty string = nationwide
    pages: number of pages to fetch (10 results per page)
    """

    # If titles not passed in, get from env or use fallback list
    if titles is None:
        job_titles_env = os.getenv("JOB_SEARCH_TITLES", "")
        if job_titles_env:
            titles = [title.strip() for title in job_titles_env.split(",")]
        else:
            titles = [
                "Software Engineer", "Marketing Assistant", 
                "Business Analyst", "Product Manager"
            ]
    
    # Override location if specified in env
    location = os.getenv("JOB_SEARCH_LOCATION", location)
    
    # Override pages if specified in env
    pages = int(os.getenv("JOB_SEARCH_PAGES", pages))

    all_jobs = []

    for title in titles:
        print(f"Searching for: {title}")

        # Set up the query parameters
        querystring = {
            "query": f"{title}" if not location else f"{title} in {location}",
            "page": "1",
            "num_pages": str(pages),
            "country": "us",
            "date_posted": "all"
        }

        # Send request to the JSearch API
        response = requests.get(JSEARCH_URL, headers=HEADERS, params=querystring)

        # Handle failed API call
        if response.status_code != 200:
            print(f"[ERROR] Failed to fetch jobs for {title}: {response.status_code}")
            print(response.text)
            continue

        # Parse response
        data = response.json()
        jobs = data.get("data", [])
        print(f"Found {len(jobs)} total jobs for '{title}'.")

        # Filter jobs to entry-level only
        entry_jobs = [job for job in jobs if is_entry_level(job)]
        print(f"Filtered down to {len(entry_jobs)} entry-level jobs.")
        all_jobs.extend(entry_jobs)

    print(f"[INFO] Total jobs across all titles: {len(all_jobs)}")
    return all_jobs
