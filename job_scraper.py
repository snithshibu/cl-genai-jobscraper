import requests
from bs4 import BeautifulSoup
import pandas as pd
from urllib.parse import urljoin

BASE_URL = "https://internshala.com"
START_URL = "https://internshala.com/jobs/"
MAX_PAGES = 3  # scrape first 3 pages to keep it light; you can increase later


def fetch_page(url: str) -> str:
    """
    Fetch the HTML content of a page using requests.
    """
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/131.0.0.0 Safari/537.36"
        )
    }
    resp = requests.get(url, headers=headers, timeout=10)
    resp.raise_for_status()
    return resp.text


def parse_jobs_from_html(html: str):
    """
    Parse Internshala jobs HTML and extract job cards.

    This is based on the jobs listing pages on Internshala, which have
    repeated job blocks with title, company, location, stipend/salary, etc.
    """
    soup = BeautifulSoup(html, "html.parser")

    jobs_data = []

    # Main container for job listings; Internshala uses structured job cards.
    # Because their classes can be long/obfuscated, we search more generically.
    # We look for <div> elements that represent a single job card.
    job_cards = soup.find_all("div", attrs={"class": lambda c: c and "job" in c.lower()})
    # Note: this is a heuristic; if it picks too many, you can refine later.

    for card in job_cards:
        # Initialize all fields
        title = None
        location = None
        experience = None
        skills = None  # Not directly on card; can be filled from detail pages later
        salary = None
        job_url = None
        description_summary = None

        # Job Title & URL (often in an <a> tag inside the card)
        title_link = card.find("a", href=True)
        if title_link:
            title = title_link.get_text(strip=True)
            job_url = urljoin(BASE_URL, title_link["href"])

        # Location, salary, experience, and short description are spread across <div>/<span>/<p>.
        # We scan text of relevant elements.
        text_blocks = card.find_all(["div", "span", "p"], recursive=True)
        for block in text_blocks:
            t = block.get_text(" ", strip=True)

            if not t:
                continue

            lower_t = t.lower()

            # Location: Internshala often shows a city or 'Work from home' with a location icon
            if location is None and "location" in lower_t:
                # e.g. "Location(s): Delhi, Mumbai"
                if ":" in t:
                    location = t.split(":", 1)[1].strip()
                else:
                    location = t

            # Experience: if visible on the card (best effort)
            if experience is None and ("experience" in lower_t or "exp." in lower_t):
                if ":" in t:
                    experience = t.split(":", 1)[1].strip()
                else:
                    experience = t

            # Salary/Stipend: look for Rs, ₹, LPA, or 'Salary'
            if salary is None and (
                "salary" in lower_t
                or "stipend" in lower_t
                or "lpa" in lower_t
                or "₹" in t
            ):
                salary = t

            # Description summary: pick the first reasonable-length paragraph as summary
            if description_summary is None and len(t.split()) > 5 and "apply now" not in lower_t:
                description_summary = t

        jobs_data.append(
            {
                "JobTitle": title,
                "Location": location,
                "ExperienceRequired": experience,
                "SkillsRequired": skills,  # stays None unless you later parse detail pages
                "Salary": salary,
                "JobURL": job_url,
                "JobDescriptionSummary": description_summary,
            }
        )

    return jobs_data


def scrape_internshala_jobs(start_url: str, max_pages: int = 1):
    """
    Scrape multiple pages of Internshala jobs listing using simple pagination.
    Many Internshala category pages use URLs like /jobs/page-2/, /jobs/page-3/, etc.
    """
    all_jobs = []

    for page in range(1, max_pages + 1):
        if page == 1:
            url = start_url
        else:
            # For subsequent pages, Internshala often uses /jobs/page-2/, /jobs/page-3/, etc.
            url = urljoin(start_url, f"page-{page}/")

        print(f"Fetching page {page}: {url}")
        try:
            html = fetch_page(url)
        except requests.exceptions.RequestException as e:
            print(f"Error fetching page {page}: {e}")
            break

        jobs = parse_jobs_from_html(html)
        print(f"Found {len(jobs)} job cards on page {page}")
        all_jobs.extend(jobs)

    return all_jobs


def save_to_excel(jobs, output_file: str):
    """
    Save the list of job dictionaries to an Excel file using pandas.
    """
    df = pd.DataFrame(jobs)

    # Ensure columns are in the order required by the PDF
    columns_order = [
        "JobTitle",
        "Location",
        "ExperienceRequired",
        "SkillsRequired",
        "Salary",
        "JobURL",
        "JobDescriptionSummary",
    ]
    df = df.reindex(columns=columns_order)

    df.to_excel(output_file, index=False)
    print(f"Saved {len(df)} jobs to {output_file}")


def main():
    try:
        jobs = scrape_internshala_jobs(START_URL, max_pages=MAX_PAGES)
        print(f"Total jobs collected: {len(jobs)}")

        if not jobs:
            print("No jobs collected. You may need to refine the selectors in parse_jobs_from_html.")
            return

        output_file = "Internshala_Jobs.xlsx"
        save_to_excel(jobs, output_file)

    except Exception as e:
        print(f"Unexpected error: {e}")


if __name__ == "__main__":
    main()
