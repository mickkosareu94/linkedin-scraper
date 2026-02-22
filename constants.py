SEARCH_YAML = 'yaml_files/search.yaml'
DETAIL_YAML = 'yaml_files/detail.yaml'
SEEN_JOBS_FILE = 'seen_jobs/seen_jobs.json'
RESUME_PATH = 'resume/resume.pdf'

SEARCH_URL = 'https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search'
DETAIL_URL = 'https://www.linkedin.com/jobs-guest/jobs/api/jobPosting/{}'

HEADERS = {
    'User-Agent': (
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) '
        'AppleWebKit/537.36 (KHTML, like Gecko) '
        'Chrome/120.0.0.0 Safari/537.36'
    )
}

CSV_FIELDS = [
    'title',
    'company',
    'location',
    'seniority_level',
    'employment_type',
    'job_function',
    'industries',
    'publication_date',
    'description',
    'ai_description',
    'match_percentage',
    'match_description',
    'url',
]

LLM_PROMPT = '''
You are a recruiter assistant. Compare the resume below against each of the {count} job descriptions.
Return ONLY a JSON array of exactly {count} objects in the same order as the jobs, each with:
- 'ai_description': 2-3 sentences summarising the role, followed by a bullet list of the main technical skills required
- 'match_percentage': integer 0-100
- 'match_description': 2-3 sentences on what matches and what does not

Resume:
{resume}

Jobs:
{jobs}
'''

GEMINI_MODEL = 'gemini-2.5-flash'