When picking which PR to work on next — choosing among several open PRs to
review, iterate (ARDI), or pick up first in a queue — slightly prefer
**internal infrastructure PRs** over **feature PRs**, all else equal.

An infrastructure PR changes shared tooling other work depends on: CI
workflows, reusable actions, templates, lint/CI config, dev scripts, or
this `ai-config` corpus itself. A feature PR adds or changes user-facing
behavior in a product repo. Infrastructure work unblocks everything built on
top of it, so a small lead in priority pays off across every PR that follows.

This is a **tie-breaker**, not an override: explicit priority labels,
blocking relationships, age, and size still rank above it. Apply it only when
two candidates are otherwise close — don't reorder a queue around it when a
feature PR is clearly more urgent (a labeled `P0`, something blocking other
work, or something the user flagged directly).
