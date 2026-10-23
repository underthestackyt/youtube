---
name: ticket-triage
description: Analyze a support-ticket CSV, identify overdue unresolved tickets, and produce a consistent Markdown triage report. Use when asked to triage support tickets, summarize a ticket queue, identify SLA breaches, or produce a support operations report.
---

# Ticket triage

When the user asks to analyze a ticket CSV:

1. Read `references/SCHEMA.md` to understand columns and SLA rules.
2. Confirm the input exists and has the expected columns. Do not invent missing data.
3. Run the deterministic report generator from the project root:
   `python3 .github/skills/ticket-triage/scripts/triage.py data/tickets.csv reports/triage-report.md`
4. Read the generated report and explain the most important findings with ticket IDs.
5. If asked, suggest next steps, clearly distinguishing those suggestions from measured results.

Do not modify source CSV data. Do not claim tickets have been escalated or resolved. The script uses sample educational SLA rules; do not present them as a company's real policy.
