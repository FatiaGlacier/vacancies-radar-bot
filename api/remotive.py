import requests

BASE_URL = "https://remotive.com/api/remote-jobs"

def get_jobs_number():
    response = requests.get(BASE_URL)
    response.raise_for_status

    data = response.json()
    return data["job-count"]
