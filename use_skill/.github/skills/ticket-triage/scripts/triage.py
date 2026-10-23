#!/usr/bin/env python3
"""Generate an offline ticket triage report from a CSV (Python standard library only)."""
import csv
import sys
from collections import Counter
from pathlib import Path

REQUIRED = {"ticket_id", "customer", "priority", "status", "age_hours", "subject"}
LIMITS = {"P1": 4, "P2": 24, "P3": 72}
VALID_STATUSES = {"open", "in progress", "resolved"}


def main():
    if len(sys.argv) != 3:
        raise SystemExit("Usage: python3 triage.py INPUT.csv OUTPUT.md")
    source, target = map(Path, sys.argv[1:])
    if not source.is_file():
        raise SystemExit(f"Input file not found: {source}")
    with source.open(newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        if not reader.fieldnames or not REQUIRED.issubset(set(reader.fieldnames)):
            raise SystemExit(f"CSV must contain columns: {', '.join(sorted(REQUIRED))}")
        tickets = list(reader)
    if not tickets:
        raise SystemExit("CSV is empty")
    ids = set()
    normalized = []
    for line, t in enumerate(tickets, start=2):
        ticket_id = t["ticket_id"].strip()
        p = t["priority"].strip().upper()
        status = t["status"].strip().lower()
        if not ticket_id or ticket_id in ids:
            raise SystemExit(f"Invalid or duplicate ticket ID at CSV line {line}")
        ids.add(ticket_id)
        if p not in LIMITS or status not in VALID_STATUSES:
            raise SystemExit(f"Unknown priority or status at CSV line {line}")
        try:
            age = float(t["age_hours"])
        except ValueError:
            raise SystemExit(f"Invalid age_hours at CSV line {line}")
        if not 0 <= age < float('inf'):
            raise SystemExit(f"age_hours must be finite and nonnegative at CSV line {line}")
        normalized.append({"id": ticket_id, "customer": t["customer"].strip(), "priority": p,
                           "status": status, "age": age, "subject": t["subject"].strip(),
                           "overdue": status != "resolved" and age > LIMITS[p]})
    overdue = sorted((t for t in normalized if t["overdue"]),
                     key=lambda t: (int(t["priority"][1:]), -(t["age"] - LIMITS[t["priority"]])))
    active = sum(t["status"] != "resolved" for t in normalized)
    by_priority = Counter(t["priority"] for t in normalized)
    lines = ["# Ticket Triage Report", "", "*Generated from the supplied sample CSV. SLA thresholds are for demonstration only.*", "",
             "## Summary", "", f"- Total tickets: **{len(normalized)}**",
             f"- Active tickets: **{active}**", f"- Resolved tickets: **{len(normalized) - active}**",
             f"- Overdue active tickets: **{len(overdue)}**",
             f"- Priority breakdown: P1 **{by_priority['P1']}**, P2 **{by_priority['P2']}**, P3 **{by_priority['P3']}**", "",
             "## Overdue tickets", "", "| ID | Priority | Status | Age (h) | SLA (h) | Customer | Subject |", "|---|---|---|---:|---:|---|---|"]
    for t in overdue:
        safe = lambda x: str(x).replace("|", "\\|").replace("\n", " ")
        lines.append(f"| {safe(t['id'])} | {t['priority']} | {t['status'].title()} | {t['age']:g} | {LIMITS[t['priority']]} | {safe(t['customer'])} | {safe(t['subject'])} |")
    if not overdue:
        lines.append("| None | — | — | — | — | — | — |")
    lines += ["", "## Suggested actions (not executed)", ""]
    if overdue:
        for t in overdue:
            action = "Escalate immediately and confirm incident owner" if t["priority"] == "P1" else "Review owner and plan next update"
            lines.append(f"- **{t['id']}** ({t['priority']}): {action}.")
    else:
        lines.append("- No overdue active tickets under the demo thresholds; continue regular monitoring.")
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Wrote {target} | tickets={len(normalized)} | overdue={len(overdue)}")

if __name__ == "__main__":
    main()
