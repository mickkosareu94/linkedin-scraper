import smtplib
import ssl
import os
from email.mime.text import MIMEText
from dotenv import load_dotenv

load_dotenv()

sender = os.getenv('GMAIL_SENDER')
sender_password = os.getenv('GMAIL_PASSWORD')
receiver = os.getenv('GMAIL_RECEIVER')


def build_email_message(jobs: list[dict]) -> str:
    message_lines = [f'LinkedIn Jobs digest — {len(jobs)} new job(s)\n']

    for index, job in enumerate(jobs, 1):
        message_lines += [
            f'{"─" * 20}',
            f'{index}. {job.get("title") or "N/A"} — {job.get("company") or "N/A"} \n',
            f'   Location: {job.get("location") or ""}',
            f'   Seniority: {job.get("seniority_level") or ""}',
            f'   Type: {job.get("employment_type") or ""} \n',
            f'   Short job description: {job.get("ai_description") or ""} \n',
            f'   Match percentage: {job.get("match_percentage") or "N/A"}%',
            f'   Match summary: {job.get("match_description") or ""} \n',
            f'   Posted: {job.get("publication_date") or ""}',
            f'   URL: {job.get("url") or ""}',
            '',
        ]
    return '\n'.join(message_lines)


def send_email(jobs: list[dict]) -> None:
    if not jobs:
        print('No jobs to include in the email. Skipping email sending.')
        return

    message = MIMEText(build_email_message(jobs), 'plain')
    message['Subject'] = f'LinkedIn Jobs — {len(jobs)} new match(es)'
    message['From'] = f'LinkedIn Jobs Digest <{sender}>'
    message['To'] = receiver

    host = 'smtp.gmail.com'
    port = 465

    context = ssl.create_default_context()

    with smtplib.SMTP_SSL(host, port, context=context) as server:
        server.login(sender, sender_password)
        server.sendmail(sender, receiver, message.as_string())

    print(f'Email sent to {receiver} with {len(jobs)} job(s).')
