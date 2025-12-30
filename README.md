# Job Scraper – Internshala Jobs

A Python-based web scraper that collects job postings from the public Internshala jobs page and exports them to a structured Excel file.  
This project was built as part of a Generative AI task to practice web scraping, HTML parsing, and data export workflows.

## Features

- Scrapes multiple pages from the Internshala jobs listing:
  - `https://internshala.com/jobs/`
  - `https://internshala.com/jobs/page-2/`
  - `https://internshala.com/jobs/page-3/`
- Uses `requests` to download HTML and `BeautifulSoup` to parse job cards.
- Handles simple pagination with a configurable `MAX_PAGES` variable.
- Extracts key job details into a tabular format:
  - `JobTitle`
  - `Location`
  - `ExperienceRequired` (best-effort, based on visible text)
  - `SkillsRequired` (left blank where not available on the card)
  - `Salary`
  - `JobURL`
  - `JobDescriptionSummary`
- Saves all collected jobs into an Excel file: `Internshala_Jobs.xlsx`.

## Tech Stack

- **Language**: Python 3  
- **Libraries**:
  - `requests` – HTTP requests for fetching the pages
  - `beautifulsoup4` – HTML parsing
  - `pandas` – tabular data handling
  - `openpyxl` – Excel file support (used internally by `pandas.to_excel`)

## Project Structure

```
.
├── job_scraper.py        # Main script: scraping, parsing, pagination, Excel export
├── Internshala_Jobs.xlsx # Output Excel file with scraped job data
├── venv/                 # Python virtual environment (ignored by git)
└── README.md             # Project documentation
```

## How It Works

1. **Fetch pages**  
   The script starts at `https://internshala.com/jobs/` and fetches additional pages like `/page-2/`, `/page-3/` up to `MAX_PAGES` using the `fetch_page` function.

2. **Parse job cards**  
   Each page is parsed with `BeautifulSoup` in `parse_jobs_from_html`, which searches for job card containers and extracts:
   - Title and job URL from the main link.
   - Location, experience (if visible), and salary from text blocks.
   - A short description summary from the first suitable paragraph on the card.

3. **Normalize and export**  
   All job dictionaries are combined into a `pandas.DataFrame`, columns are ordered as required, and the result is written to `Internshala_Jobs.xlsx`.