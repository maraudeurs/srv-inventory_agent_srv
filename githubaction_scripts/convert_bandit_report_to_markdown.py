import json

def convert_to_markdown(bandit_json):
    md_lines = []
    md_lines.append("## Bandit Security Analysis Report")
    md_lines.append("| Issue Severity | Issue Confidence | File | Line | Issue Text |")
    md_lines.append("| --- | --- | --- | --- | --- |")

    for issue in bandit_json["results"]:
        md_lines.append(
            f"| {issue['issue_severity']} | {issue['issue_confidence']} | {issue['filename']} | {issue['line_number']} | {issue['issue_text']} |"
        )

    if len(bandit_json["results"]) > 0:
        md_lines.append("\n### Issues Summary")
        md_lines.append(f"**Total Issues Found:** {len(bandit_json['results'])}")
    else:
        md_lines.append("\n**No issues found.**")

    return "\n".join(md_lines)

# Load the Bandit JSON report
with open("bandit_report.json", "r") as json_file:
    bandit_report = json.load(json_file)

# Convert to Markdown
markdown_report = convert_to_markdown(bandit_report)

# Write the Markdown report to a file
with open("bandit_report.md", "w") as md_file:
    md_file.write(markdown_report)
