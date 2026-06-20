---
name: always
description: "Alias for `remember` / `memorize`. Persist a standing rule or preference to memory, routed by relevance to project-specific or general scope. Use when the user gives an always-apply directive — 'always …', 'never …', 'from now on …', 'I prefer …' — or says '/always', 'remember that …', or 'note that …'."
user-invocable: true
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
---

# always (alias for `remember` / `memorize`)

`always`, `remember`, and `memorize` are synonyms — same behavior regardless of
which word the user uses. An "always …" (or "never …") directive is a standing
preference to persist, so it routes to the same canonical skill. Read and
follow it:

→ **`~/.claude/skills/memorize/SKILL.md`**
