import json
import os

# File where seen job IDs will be stored
SEEN_JOBS_FILE = "seen_jobs.json"

def load_seen_jobs():
    """Loads previously seen job IDs from the JSON file."""
    if not os.path.exists(SEEN_JOBS_FILE):
        return set()  # Return empty set if file doesn't exist

    with open(SEEN_JOBS_FILE, "r") as file:
        try:
            job_ids = json.load(file)  # Load list of IDs from file
            return set(job_ids)        # Convert list to set for fast lookup
        except json.JSONDecodeError:
            return set()  # Return empty set if file is corrupted

def save_seen_jobs(job_ids):
    """Saves current set of job IDs to the JSON file."""
    with open(SEEN_JOBS_FILE, "w") as file:
        json.dump(list(job_ids), file, indent=2)  # Save as formatted JSON
