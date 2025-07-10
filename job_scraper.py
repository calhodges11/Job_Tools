import requests
import pandas as pd
from datetime import datetime, timedelta
from database import init_db, insert_jobs, get_last_scrape_time

#================ SCRAPE JOB LISTINGS FROM SITE API ===================

REMOTEOK_API_URL = "https://remoteok.com/api"

#=== Get job data from remoteok.com API and parse the useful fields  ===
def fetch_remoteok_jobs():

    #Check if the API call is successful
    response = requests.get(REMOTEOK_API_URL, headers={"User-Agent": "Mozilla/5.0"})
    if response.status_code != 200:
        raise Exception("Failed to fetch data from RemoteOK")

    #Pull results into list of dictionaries and skip the first element since it is metadata
    jobs = response.json()[1:]
    records = []

    #Loop through jobs list and pull useful data into records
    for job in jobs:
        records.append({
            "id": job.get("id"),
            "company": job.get("company"),
            "position": job.get("position"),
            "location": job.get("location") or "Remote",
            "tags": job.get("tags"),
            "date_posted": job.get("date"),
            "url": job.get("url")
        })

    df = pd.DataFrame(records) # Convert records list into a pandas dataframe
    df["scraped_at"] = datetime.now() # add timestamp for the scrape to dataset
    df["date_posted"] = pd.to_datetime(df["date_posted"], errors="coerce") # convert dates for pd readability
    return df


if __name__ == "__main__":
    init_db()

    # Only scrape if last scrape was more than 3 hours ago
    last_scrape = get_last_scrape_time()
    now = datetime.now()

    if last_scrape and (now - last_scrape < timedelta(hours=3)):
        print(f"Last scrape was at {last_scrape}, less than 3 hours ago. Skipping.")
    else:

        df_jobs = fetch_remoteok_jobs() # retrieve dataframe from remoteok API
        numJobs = len(df_jobs)          # count number of entries pulled
        insert_jobs(df_jobs)            # save dataframe to SQLite database

        after_scrape = get_last_scrape_time()
        print(f"Scraped and saved {numJobs} jobs at {after_scrape}.")


