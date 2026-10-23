# CSV schema and demo SLA rules

Required columns: `ticket_id`, `customer`, `priority`, `status`, `age_hours`, `subject`.

Supported priority values (case insensitive): `P1`, `P2`, `P3`.
Supported status values: `Open`, `In Progress`, `Resolved`.
`age_hours` is a nonnegative number representing the ticket age as of the sample snapshot.

**Educational demo thresholds, not real company SLA policy:**
- P1: 4 hours
- P2: 24 hours
- P3: 72 hours

An unresolved ticket is marked **Overdue** if `age_hours > threshold`. Resolved tickets are never listed as active SLA breaches. A ticket exactly at the threshold is not marked overdue.
