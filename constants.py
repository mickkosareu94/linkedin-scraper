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
You are a strict but fair technical recruiter. Compare the resume against each of the {count} job descriptions.
Be precise and conservative with scores — do not round up or give benefit of the doubt.

Scoring rules:

Step 1 — Assign a base score by domain and platform fit:
- Same domain, same platform (e.g. mobile QA vs mobile QA): base 85
- Same domain, different platform (e.g. mobile QA vs web QA): base 60
- Adjacent domain (e.g. manual QA vs automation QA, or QA vs QA tooling): base 50
- Completely different domain (e.g. electrical/hardware QA vs software QA): base 15, do not exceed 25 regardless of anything else

Step 2 — Adjust the base score by ±5-10 points per factor:
- Required tool/skill is directly present in resume: +5 to +10
- Required tool is similar but not the same (e.g. Cypress vs Playwright, Appium vs Espresso): -5 to -10, do not treat as a match
- Required tool/skill is completely missing from resume: -5 to -10
- Seniority level is significantly higher than resume: -10
- Strong overlap in testing methodology, processes, or domain knowledge: +5 to +10

Step 3 — Hard limits:
- Never exceed the base score by more than 15 points
- Never go below 5
- Only give 80+ if domain, platform, and the majority of required tools directly match the resume

Return ONLY a JSON array of exactly {count} objects in the same order as the jobs, each with:
- 'ai_description': 2-3 sentences summarising the role, followed by a bullet list of the main technical skills required
- 'match_percentage': integer 0-100 following the scoring rules above strictly
- 'match_description': 2-3 sentences explaining the score — name exact tools and skills, state clearly what matches and what does not, do not generalise

Resume:
{resume}

Jobs:
{jobs}
'''

GEMINI_MODEL = 'gemini-2.5-flash'