import json

def convert_to_markdown(report):
    md_lines = []
    md_lines.append("# Pytest Report\n")
    md_lines.append(f"**Total Tests:** {report['summary']['total']}")
    md_lines.append(f"**Passed:** {report['summary'].get('passed', 0)}")
    md_lines.append(f"**Failed:** {report['summary'].get('failed', 0)}")
    md_lines.append(f"**Skipped:** {report['summary'].get('skipped', 0)}\n")

    if report['summary']['failed'] > 0:
        md_lines.append("## Failed Tests:\n")
        for test in report['tests']:
            if test['outcome'] == 'failed':
                md_lines.append(f"### {test['nodeid']}\n")
                if 'call' in test and 'crash' in test['call']:
                    for failure in test['call']['crash']['traceback']:
                        md_lines.append(f"```\n{failure}\n```\n")
                elif 'setup' in test and 'crash' in test['setup']:
                    for failure in test['setup']['crash']['traceback']:
                        md_lines.append(f"```\n{failure}\n```\n")
                elif 'teardown' in test and 'crash' in test['teardown']:
                    for failure in test['teardown']['crash']['traceback']:
                        md_lines.append(f"```\n{failure}\n```\n")

    return "\n".join(md_lines)

with open("pytest_report.json", "r") as json_file:
    pytest_report = json.load(json_file)

markdown_report = convert_to_markdown(pytest_report)

with open("pytest_report.md", "w") as md_file:
    md_file.write(markdown_report)
