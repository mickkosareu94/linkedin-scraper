import time
import requests
import argparse
from selectorlib import Extractor
from constants import (
    HEADERS,
    SEARCH_URL,
    DETAIL_URL,
    SEARCH_YAML,
    DETAIL_YAML,
    RESUME_PATH,
)
from export import save_to_csv
from helpers import html_to_text
from pdf_reader import read_pdf
from ai_job_match import match_all_jobs
from helpers import filter_new
from send_email import send_email


search_extractor = Extractor.from_yaml_file(SEARCH_YAML)
detail_extractor = Extractor.from_yaml_file(DETAIL_YAML)


def scrape(url: str, params: dict = None) -> str:
    response = requests.get(url, headers=HEADERS, params=params, timeout=10)
    if response.status_code != 200:
        raise Exception(f'Failed to fetch page: {response.status_code}')
    return response.text


def extract_search(source: str) -> list[dict]:
    result = search_extractor.extract(source)
    return result.get('jobs') or []


def extract_detail(source: str) -> dict:
    result = detail_extractor.extract(source) or {}
    if result.get('description'):
        result['description'] = html_to_text(result['description'])
    return result or {}


def run(keyword: str, location: str, max_jobs: int) -> list[dict]:
    all_jobs = []
    start = 0

    # Loop until we have collected enough jobs or there are no more jobs to fetch
    while len(all_jobs) < max_jobs:
        params = {'keywords': keyword, 'location': location, 'start': start}
        print(f'  [search] start={start} | collected: {len(all_jobs)}')
        scraped_search = scrape(SEARCH_URL, params=params)
        jobs = extract_search(scraped_search)
        if not jobs:
            print('No more jobs found.')
            break
        all_jobs.extend(jobs)
        start += len(jobs)
        time.sleep(2)

    all_jobs = all_jobs[:max_jobs]  # Limit to max_jobs
    print(f'Collected {len(all_jobs)} jobs. Fetching details...')
    resume_text = read_pdf(RESUME_PATH) 

    for index, job in enumerate(all_jobs):
        job_id = (job.get('job_id') or '').split(':')[-1]
        print(f'  [detail] {index + 1}/{len(all_jobs)}: {job.get("title")}')
        try:
            scraped_detail = scrape(DETAIL_URL.format(job_id))
            job_detail = extract_detail(scraped_detail)
            job.update(job_detail)
        except requests.HTTPError as e:
            print(f'Failed to fetch job detail for ID {job_id}: {e}')
        job.pop('job_id', None)
        time.sleep(2)

    print(f'\n  [AI] Matching {len(all_jobs)} jobs against resume...')
    match_all_jobs(resume_text, all_jobs)

    return all_jobs


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='LinkedIn job scraper with AI matching'
    )
    parser.add_argument('keyword', type=str, help='Job title to search for')
    parser.add_argument('location', type=str, help='Location to search in')
    parser.add_argument(
        '--max-jobs', type=int, default=5, help='Max number of jobs (default: 5)'
    )
    parser.add_argument(
        '--output', type=str, default=None, help='Optional CSV output path'
    )
    args = parser.parse_args()

    jobs = run(args.keyword, args.location, args.max_jobs)
    new_jobs = filter_new(jobs)
    if args.output:  # only writes CSV when --output is passed
        save_to_csv(new_jobs, args.output)

    send_email(new_jobs)
