from constants import CSV_FIELDS
import csv


def save_to_csv(jobs: list[dict], output: str):
    with open(output, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=CSV_FIELDS, extrasaction='ignore')
        writer.writeheader()
        writer.writerows(jobs)

    print(f'Saved {len(jobs)} jobs → {output}')