# LinkedIn Job Scraper

Scrapes LinkedIn job listings, matches them against your resume using Gemini AI,
and sends a plain-text email digest of new jobs.

## Features

- Scrapes job cards and full descriptions from LinkedIn's public guest API
- Extracts title, company, location, seniority, employment type, job function, industries, publication date, description
- Converts HTML descriptions to readable plain text
- Matches each job against your resume using Gemini 2.5 Flash
- Tracks seen jobs to send only new listings each run
- Sends a formatted plain-text email digest via Gmail SMTP

## Project structure
```
linkedin-scraper/
├── main.py # Entry point, CLI, orchestrator
├── ai_job_match.py # Gemini AI matching
├── pdf_reader.py # PDF reading
├── send_email.py # Email building, sending
├── export.py # CSV saving
├── constants.py # Constants
├── helpers.py # HTML-to-text, seen jobs tracking, filtering new jobs
├── yaml_files/
│ └── search.yaml # CSS selectors for job search cards
│ └── detail.yaml # CSS selectors for individual job pages
├── resume/
│ └── resume.pdf # Your resume (not committed to repo)
├── seen_jobs/
│ └── seen_jobs.json # Tracks already-sent job URLs
├── requirements.txt
├── README.md
└── .gitignore
```

## Environment variables (add in .env file locally)
| Variable       | Description                                                               |
| -------------- | ------------------------------------------------------------------------- |
| GEMINI_API_KEY | From aistudio.google.com                                                  |
| GMAIL_SENDER   | Your Gmail address used to send                                           |
| GMAIL_PASSWORD | 16-char app password                                                      |
| GMAIL_RECEIVER | Address to receive the digest                                             |

## Usage
### Basic run — emails new jobs (5 by default), custom location, no CSV
python main.py 'QA Engineer' --location 'Germany'

### With 2 job queries, custom location and custom job count
python main.py 'QA Engineer' 'Test Automation Engineer' --location 'Germany' --max-jobs 25

### Additionally write to a local CSV
python main.py 'QA Engineer' --location 'Germany' --output jobs.csv
