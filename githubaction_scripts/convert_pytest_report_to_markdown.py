import json

def convert_to_markdown(report):
    md_lines = []
    md_lines.append("# Pytest Report\n")
    md_lines.append(f"**Total Tests:** {report['summary']['total']}")
    md_lines.append(f"**Passed:** {report['summary']['passed']}")
    md_lines.append(f"**Failed:** {report['summary']['failed']}")
    md_lines.append(f"**Skipped:** {report['summary']['skipped']}\n")

    if report['summary']['failed'] > 0:
        md_lines.append("## Failed Tests:\n")
        for test in report['tests']:
            if test['outcome'] == 'failed':
                md_lines.append(f"### {test['nodeid']}\n")
                for failure in test['call']['crash']['traceback']:
                    md_lines.append(f"```\n{failure}\n```\n")

    return "\n".join(md_lines)

# Load the pytest JSON report
with open("pytest_report.json", "r") as json_file:
    pytest_report = json.load(json_file)

# Convert to Markdown
markdown_report = convert_to_markdown(pytest_report)

# Write the Markdown report to a file
with open("pytest_report.md", "w") as md_file:
    md_file.write(markdown_report)
