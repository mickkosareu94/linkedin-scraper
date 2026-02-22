import re
import json
from pathlib import Path
from constants import SEEN_JOBS_FILE


# Convert HTML content to plain text by replacing tags with appropriate formatting (more readable for job descriptions).
def html_to_text(html: str) -> str:
    if not html:
        return ''
    replacements = [
        (r'<li[^>]*>',   '\n• '),    # list item  → bullet
        (r'</li>',       ''),
        (r'<br\s*/?>',   '\n'),      # line break → newline
        (r"<p[^>]*>",    '\n'),      # paragraph  → newline
        (r"</p>",        '\n'),
        (r"<h\d[^>]*>",  '\n'),      # headings   → newline
        (r'<[^>]+>',     ''),        # strip all remaining tags
        (r'&nbsp;',      ' '),
        (r'&amp;',       '&'),
        (r'&lt;',        '<'),
        (r'&gt;',        '>'),
        (r'\n{3,}',      '\n\n'),    # collapse excess blank lines
    ]
    for pattern, replacement in replacements:
        html = re.sub(pattern, replacement, html, flags=re.IGNORECASE)
    return html.strip()


def load_seen_jobs() -> set:
    if Path(SEEN_JOBS_FILE).exists():
        return set(json.loads(Path(SEEN_JOBS_FILE).read_text()))
    return set()


def save_seen_jobs(seen_jobs: set) -> None:
    Path(SEEN_JOBS_FILE).write_text(json.dumps(list(seen_jobs)))


def filter_new(jobs: list[dict]) -> list[dict]:
    seen_jobs = load_seen_jobs()
    new_jobs = [job for job in jobs if job.get('url') not in seen_jobs]
    seen_jobs.update(job['url'] for job in new_jobs)
    save_seen_jobs(seen_jobs)
    return new_jobs