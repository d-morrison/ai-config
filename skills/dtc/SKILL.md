---
name: dtc
description: "Alias for `delegate-to-codex`. Delegate heavy read/draft/verify work to the `codex` CLI before spending Claude quota — build prompts, run codex read-only, orchestrate multi-item work via a background runner + DONE-marker poll, fall back to Claude only for what codex can't finish. Use when asked to 'dtc', 'delegate to codex', 'use codex', 'run this on codex', 'codex-first', 'do this with codex', or 'offload to codex'."
user-invocable: true
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
---

# dtc (alias for `delegate-to-codex`)

This is a short alias. Read and follow the canonical skill:

→ **[delegate-to-codex](../delegate-to-codex/SKILL.md)**
