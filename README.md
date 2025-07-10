**JOB MARKET TRACKER AND RESUME OPTIMIZER**

- Scrapes remote tech jobs from remoteok.com
- Analyzes the most in demand skills by frequency
- Filter jobs by location, company, title, and posting date
- Visualize skill trends
- Stores all data in SQLite database
- Resume matching coming soon!


<img width="600" height="350" alt="image" src="https://github.com/user-attachments/assets/f23e5671-9347-4ba4-b873-5d4d3c627872" />



-------------------------
  **TECH STACK**

- **Python 3.11.9**
- **Streamlit** for the interactive UI
- **SQLite** for persistent job storage
- **Pandas + Altair** for data analysis and visualization
- **RemoteOK API** for job listings

-------------------------
  **SETUP**
  1. Clone the repo:
      - git clone https://github.com/calhodges11/job-tools.git
      - cd job-tools
  2. Install requirements:
      - pip install -r requirements.txt
  3. Scrape job listings:
      - python job_scraper.py
  4. Launch the dashboard:
      - streamlit run main.py
       
----------------------------
**Planned Features**
- Scheduled scraping (via cron or schedule)
- Location filter via dropdown menu
- Clickable job URLs in dashboard
- Upload your resume and get a match score (WIP)
- Compare skill trends over time

---------------------------
**Author**
Calloway Hodges
github.com/calhodges11 | https://www.linkedin.com/in/calloway-hodges/
