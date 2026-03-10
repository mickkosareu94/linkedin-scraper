import json
import os
import time

from dotenv import load_dotenv
from google import genai
from google.genai import types

from constants import GEMINI_MODEL, LLM_PROMPT

load_dotenv()

client = genai.Client(api_key=os.getenv('GEMINI_API_KEY'))


def match_all_jobs(resume_text: str, jobs: list[dict]) -> None:
    jobs_block = '\n\n'.join(
        f'Job {index + 1} — {job.get("title")} at {job.get("company")}:\n{job.get("description", "")}'
        for index, job in enumerate(jobs)
    )

    for attempt in range(1, 4):  # try up to 3 times
        try:
            response = client.models.generate_content(
                model=GEMINI_MODEL,
                contents=LLM_PROMPT.format(
                    count=len(jobs), resume=resume_text, jobs=jobs_block
                ),
                config=types.GenerateContentConfig(
                    response_mime_type='application/json'
                ),
            )
            break  # success
        except Exception as e:
            print(f'  [AI] Attempt {attempt} failed: {e}')
            if attempt == 3:
                raise
            time.sleep(30 * attempt)  # wait 30s, then 60s before next attempt

    results = json.loads(response.text)

    for job, result in zip(jobs, results):
        job['ai_description'] = result.get('ai_description')
        job['match_percentage'] = result.get('match_percentage')
        job['match_description'] = result.get('match_description')
