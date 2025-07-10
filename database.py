import sqlite3
import pandas as pd
import os

#=============== INITIALIZE DATABASE AND MANAGE DATA ===================

DB_NAME = "data/job_data.db"


os.makedirs("data", exist_ok=True)

#Create the database if it doesn't already exist
def init_db():
    #initialilze db connection
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        #Create table with id as primary key
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS jobs (
                id INTEGER PRIMARY KEY,
                company TEXT,
                position TEXT,
                location TEXT,
                tags TEXT,
                date_posted TEXT,
                url TEXT,
                scraped_at TEXT
            )
        """)

    conn.commit()
    conn.close()

#Insert dataframe of job listings into our table
def insert_jobs(df: pd.DataFrame):

    #open connection to the database and initialize the cursor
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    #loop through dataframe and insert entries, ignore any duplicate ids
    for _, row in df.iterrows():
        cursor.execute("""
            INSERT OR IGNORE INTO jobs (id, company, position, location, tags, date_posted, url, scraped_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            row["id"],
            row["company"],
            row["position"],
            row["location"],
            ",".join(row["tags"]) if isinstance(row["tags"], list) else row["tags"],
            row["date_posted"].isoformat() if pd.notnull(row["date_posted"]) else None,
            row["url"],
            row["scraped_at"].isoformat() if pd.notnull(row["scraped_at"]) else None
        ))
    conn.commit()
    conn.close()


#Get timestamp of most recent scrape
def get_last_scrape_time():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT MAX(scraped_at) FROM jobs") # MAX is the latest timestamp
    result = cursor.fetchone()[0]
    conn.close()
    return pd.to_datetime(result) if result else None




