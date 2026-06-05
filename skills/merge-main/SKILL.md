---
name: merge-main
description: Alias for `sync-pr-branch`. Bring a PR branch up to date with main by merging origin/main into it, resolving conflicts, running the repo's pre-commit checks, and pushing. Use when invoked as `/merge-main`, or on "merge main in", "update the branch", "the branch is behind main", or whenever main has moved ahead of a PR branch you're working on.
user-invocable: true
allowed-tools:
  - Bash
  - Read
  - Edit
  - Write
---

# merge-main

This is a **synonym for [`sync-pr-branch`](../sync-pr-branch/SKILL.md)** — the
two are interchangeable. There is no separate behavior here.

**Do this:** read `~/.claude/skills/sync-pr-branch/SKILL.md` and follow its
instructions exactly, against the current PR branch (or the branch the user
named). Everything that skill says — merge `origin/main`, resolve conflicts,
run the repo's pre-commit checks (render / lint / spell), then push — applies
unchanged.

Keep the logic only in `sync-pr-branch`; this file is just the `/merge-main`
entry point so the two names stay in sync.
