# Job Scraper – Fake Python Jobs

This project is a simple **Python web scraper** that collects job postings from the public demo site [Fake Python Jobs](https://realpython.github.io/fake-jobs/) and saves them into an Excel file using `pandas` and `openpyxl`.

The scraper is implemented in a Jupyter Notebook (`jobscraper.ipynb`) and is intended for learning the basics of web scraping: sending HTTP requests, parsing HTML with BeautifulSoup, structuring data with pandas, and exporting to `.xlsx`.

---

## Features

- Fetches the Fake Python Jobs listing page with `requests`.
- Parses HTML using `BeautifulSoup` to locate individual job cards.
- Extracts key fields:
  - Job Title  
  - Company  
  - Location  
  - Date Posted  
  - Apply Link
- Handles missing fields gracefully by filling `"N/A"`.
- Stores all jobs in a `pandas` DataFrame and exports to `job_postings.xlsx` via `openpyxl`.
