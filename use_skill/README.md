# GitHub Copilot Skills tutorial

A simple demo of using a skill in GitHub Copilot to analyze support tickets and generate a report.

## Setup

Open `use_skill` as your working folder in VS Code. The skill is in `.github/skills/ticket-triage/SKILL.md`, and the sample tickets are in `data/tickets.csv`.

## Try the skill

Open GitHub Copilot Chat in Agent mode and enter:

```text
Use the ticket-triage skill to analyze data/tickets.csv and generate
reports/triage-report.md. Tell me which tickets need attention first.
```

Review the generated report in `reports/triage-report.md`. The skill uses a Python 3 script, so make sure Python 3 is installed.
