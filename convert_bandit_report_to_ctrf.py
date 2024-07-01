import json

def convert_to_ctrf(bandit_json):
    ctrf_lines = []
    ctrf_lines.append("## Bandit Security Analysis Report")
    ctrf_lines.append("| Issue Severity | Issue Confidence | File | Line | Issue Text |")
    ctrf_lines.append("| --- | --- | --- | --- | --- |")

    for issue in bandit_json["results"]:
        ctrf_lines.append(
            f"| {issue['issue_severity']} | {issue['issue_confidence']} | {issue['filename']} | {issue['line_number']} | {issue['issue_text']} |"
        )

    if len(bandit_json["results"]) > 0:
        ctrf_lines.append("\n### Issues Summary")
        ctrf_lines.append(f"**Total Issues Found:** {len(bandit_json['results'])}")
    else:
        ctrf_lines.append("\n**No issues found.**")

    return "\n".join(ctrf_lines)

# Load the Bandit JSON report
with open("bandit_report.json", "r") as json_file:
    bandit_report = json.load(json_file)

# Convert to CTRF
ctrf_report = convert_to_ctrf(bandit_report)

# Write the CTRF report to a file
with open("bandit_report_crtf.json", "w") as ctrf_file:
    ctrf_file.write(ctrf_report)
