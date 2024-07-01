import json
import sys

with open('bandit_report.json') as f:
    report = json.load(f)

for result in report['results']:
    if result['issue_severity'] == 'HIGH':
        print(f"High severity issue found: {result['issue_text']}")
        sys.exit(1)

print("No high severity issues found.")
