import sys
import os

# Ensure current directory is in the Python path (helps with relative imports)
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

from dotenv import load_dotenv

# Internal modules
from job_tracker.job_search import search_jobs
from job_tracker.utils import load_seen_jobs, save_seen_jobs
from notifier.email_notifier import send_email_notification

# Load environment variables from .env file
load_dotenv()

# Settings for email notifications
USE_EMAIL = os.getenv("USE_EMAIL", "true").lower() == "true"
TO_EMAIL = os.getenv("TO_EMAIL", "user@example.com")

def main():
    # Fetch jobs using filters from env
    jobs = search_jobs()
    print(f"[DEBUG] Total jobs pulled: {len(jobs)}")

    # Load set of previously seen jobs
    seen = load_seen_jobs()
    new_jobs = []

    for job in jobs:
        # Identify each job uniquely
        title = job.get("job_title", "Unknown Title")
        company = job.get("employer_name", "Unknown Company")
        location = job.get("job_city", "Unknown Location")
        job_id = (
            job.get("job_id")
            or job.get("job_apply_link")
            or f"{title}_{company}_{location}_{job.get('job_posted_at_datetime_utc', '')}"
        )

        print(f"{title} at {company} in {location}")

        # Skip jobs already seen
        if job_id not in seen:
            new_jobs.append(job)
            seen.add(job_id)

    # Save updated seen job list
    save_seen_jobs(seen)

    if not new_jobs:
        print("No new jobs found.")
        return

    print(f"{len(new_jobs)} new job(s) found!")

    # Send email summary if enabled
    if USE_EMAIL:
        subject = f"{len(new_jobs)} New Job Alert(s) 🚨"
        body_lines = []

        for job in new_jobs:
            title = job.get("job_title", "Unknown Title")
            company = job.get("employer_name", "Unknown Company")
            location = job.get("job_city", "Unknown Location")
            link = job.get("job_apply_link", "")

            line = f"🔹 {title} at {company} in {location}\nApply: {link}\n"
            body_lines.append(line)

        body = "\n".join(body_lines)
        send_email_notification(TO_EMAIL, subject, body)

# Run script if executed directly
if __name__ == "__main__":
    main()
