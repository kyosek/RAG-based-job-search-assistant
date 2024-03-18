# Code below are taken from https://github.com/spinlud/py-linkedin-jobs-scraper?tab=readme-ov-file and modified

import logging
import pandas as pd
from linkedin_jobs_scraper import LinkedinScraper
from linkedin_jobs_scraper.events import Events, EventData, EventMetrics
from linkedin_jobs_scraper.query import Query, QueryOptions, QueryFilters
from linkedin_jobs_scraper.filters import (
    RelevanceFilters,
    TimeFilters,
    TypeFilters,
)

logging.basicConfig(level=logging.INFO)

JOB_TITLE = "Data Scientist"
LOCATION = ["London", "United Kingdom"]
job_postings = []


# Fired once for each successfully processed job
def on_data(data: EventData):

    print(
        "[ON_DATA]",
        data.title,
        data.company,
        data.company_link,
        data.date,
        data.link,
        data.insights,
        len(data.description),
    )
    job_postings.append([data.job_id, data.location, data.title, data.company, data.date, data.link,
                         data.description, ])

    df = pd.DataFrame(job_postings, columns=['Job_ID', 'Location', 'Title', 'Company', 'Date', 'Link', 'Description'])
    df.to_csv("data/jobs.csv")


# Fired once for each page (25 jobs)
def on_metrics(metrics: EventMetrics):
    print("[ON_METRICS]", str(metrics))


def on_error(error):
    print("[ON_ERROR]", error)


def on_end():
    print("[ON_END]")


def initialise_scraper():
    scraper = LinkedinScraper(
        chrome_executable_path=None,  # Custom Chrome executable path (e.g. /foo/bar/bin/chromedriver)
        chrome_binary_location=None,  # Custom path to Chrome/Chromium binary (e.g. /foo/bar/chrome-mac/Chromium.app/Contents/MacOS/Chromium)
        chrome_options=None,  # Custom Chrome options here
        headless=True,  # Overrides headless mode only if chrome_options is None
        max_workers=1,  # How many threads will be spawned to run queries concurrently (one Chrome driver for each thread)
        slow_mo=0.5,  # Slow down the scraper to avoid 'Too many requests 429' errors (in seconds)
        page_load_timeout=40,  # Page load timeout (in seconds)
    )

    # Add event listeners
    scraper.on(Events.DATA, on_data)
    scraper.on(Events.ERROR, on_error)
    scraper.on(Events.END, on_end)
    
    return scraper


def initialise_query(job_title: str, locations):
    queries = [
        Query(options=QueryOptions(limit=100)),  # Limit the number of jobs to scrape.
        Query(
            query=job_title,
            options=QueryOptions(
                locations=locations,
                apply_link=True,  # Try to extract apply link (easy applies are skipped). If set to True, scraping is slower because an additional page must be navigated. Default to False.
                skip_promoted_jobs=True,  # Skip promoted jobs. Default to False.
                page_offset=10,  # How many pages to skip
                limit=10,
                filters=QueryFilters(
                    # company_jobs_url="https://www.linkedin.com/jobs/search/?f_C=1441%2C17876832%2C791962%2C2374003%2C18950635%2C16140%2C10440912&geoId=92000000",  # Filter by companies.
                    relevance=RelevanceFilters.RECENT,
                    time=TimeFilters.MONTH,
                    type=[TypeFilters.FULL_TIME],
                    # on_site_or_remote=[OnSiteOrRemoteFilters.REMOTE],
                    # experience=[ExperienceLevelFilters.MID_SENIOR],
                ),
            ),
        ),
    ]
    return queries


def scrape_jobs(job_title: str, locations: list):
    scraper = initialise_scraper()
    queries = initialise_query(job_title, locations)

    scraper.run(queries)
    return scraper


if __name__ == "__main__":
    scraper = scrape_jobs(JOB_TITLE, LOCATION)
