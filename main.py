import streamlit as st
import pandas as pd
import sqlite3
from datetime import datetime
import altair as alt

#============================================= STREAMLIT DASHBOARD =======================================

#=============================== Load Data ==============================================
# Load jobs from database into our dataframe
@st.cache_data
def load_jobs():
    conn = sqlite3.connect("data/job_data.db") # open connection to database
    df = pd.read_sql("SELECT * FROM jobs", conn) # create dataframe for streamlit use
    conn.close()

    df["date_posted"] = pd.to_datetime(df["date_posted"], errors="coerce") # create date_posted entry in our dataframe
    df["date_posted"] = pd.to_datetime(df["date_posted"], errors="coerce").dt.tz_localize(None) # remove timezone
    df["scraped_at"] = pd.to_datetime(df["scraped_at"], errors="coerce") # create entry for time of scrape
    return df

#Configure streamlit page
st.set_page_config(page_title="Job Market Tracker", layout="wide")
st.title("📊 Job Market Tracker")

df = load_jobs()

#Sidebar filters
st.sidebar.header("Filters")
keyword = st.sidebar.text_input("Search title or company")
location = st.sidebar.text_input("Location filter")

#Allow user to filter by date of job posting
min_post_date = df["date_posted"].min().date()
max_post_date = df["date_posted"].max().date()

selected_min_date = st.sidebar.date_input(
    "Show jobs posted after",
    value=min_post_date,
    min_value=min_post_date,
    max_value=max_post_date
)

#====================================== Filter Logic =============================

#Create copy of data to work with
filtered_df = df.copy()

#Keyword filter
if keyword:
    filtered_df = filtered_df[
        filtered_df["position"].str.contains(keyword, case=False, na=False) |
        filtered_df["company"].str.contains(keyword, case=False, na=False)
    ]

#Location filter
if location:
    filtered_df = filtered_df[filtered_df["location"].str.contains(location, case=False, na=False)]

#Date posted filter
filtered_df = filtered_df[filtered_df["date_posted"] >= pd.to_datetime(selected_min_date)]

#Show filtered data
st.write(f"Showing {len(filtered_df)} job(s):")
st.dataframe(filtered_df[["date_posted", "company", "position", "location", "tags", "url"]])



#====================================== High Demand Skills ===============================
st.header("📌 Most In-Demand Skills (by job tags)")

# Flatten tags list into a single pandas series where the index = tag name and value is occurences.
# If tags contains two skills separated by a comma in one tag,
# split it into a list then explode the list into separate tags
# then count the occurences of each tag and get the 20 most occurring
all_tags = (
    df["tags"] # pull tags from frame
    .dropna() # remove null tags
    .apply(lambda x: x if isinstance(x, list) else x.split(",")) # skip existing tags and split entries if comma
    .explode() # explode list entries
    .str.strip() # remove leading/trailing spaces
    .loc[lambda x: x != ""]  # remove blank tags
    .value_counts() # count the number of occurrences of each tag
    .head(20) # get the top 20 occurring tags
)

skills_df = all_tags.reset_index() # convert series into a dataframe
skills_df.columns = ["Skill", "Count"] # set column names

# Plot bar chart of new skills dataframe
chart = alt.Chart(skills_df).mark_bar().encode(
    x=alt.X("Count:Q", title="Job Count"),
    y=alt.Y("Skill:N", sort="-x", title="Skill"),
    tooltip=["Skill", "Count"]
).properties(height=400)

st.altair_chart(chart, use_container_width=True)

