import requests
import json
import time
from dotenv import load_dotenv
import os

load_dotenv()
RAPIDAPI_TOKEN= os.getenv("RAPIDAPI_TOKEN")
PATH_TO_MOCK = os.getenv("PATH_TO_MOCK")

BASE_URL = "https://jsearch.p.rapidapi.com/search-v2"

headers = {
	"x-rapidapi-key": RAPIDAPI_TOKEN,
	"x-rapidapi-host": "jsearch.p.rapidapi.com"
}

QUERIES = [
    "Python developer",
    "Java developer",
    "Kotlin developer",
    "JavaScript backend developer",
    "JavaScript frontend developer",
    "Fullstack developer",
    "Frontend developer"
]

def fetch_all_jobs(queries=QUERIES, pages_per_query=5):
    all_jobs = []

    for query in queries:

        params = {
            "query": query,
            "num_pages": "5",
            "country":"de",
            "language":"de",
            "date_posted":"week"
        }

        response = requests.get(BASE_URL, headers=headers, params=params)
        response.raise_for_status()

        data = response.json().get("data", {})
        if not data:
            continue  

        jobs = data.get("jobs", [])
        all_jobs.extend(jobs)

        print(f"Data: '{data}'")  
        print(f"Query: '{query}' | Total: {len(all_jobs)}")
        time.sleep(0.5)

    return all_jobs

try:
    print("Starting fetch...")
    jobs = fetch_all_jobs()
    print(f"Fetched {len(jobs)} jobs")

    if not jobs:
        print("Jobs list is empty! Nothing to write.")
    else:
        with open(PATH_TO_MOCK, "w", encoding="utf-8") as f:
            json.dump(jobs, f, ensure_ascii=False, indent=2)
        print(f"Done! Saved {len(jobs)} jobs")

except OSError as e:
    print(f"Cannot open file: {e}")

except Exception as e:
    print(f"Something went wrong: {e}")
    