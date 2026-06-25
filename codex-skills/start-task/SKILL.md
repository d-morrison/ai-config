---
name: "start-task"
description: "Codex wrapper for the ai-config Claude skill `start-task`. Alias for `st` (Start Task, issue-first). Before writing code or opening a PR, ensure a tracking issue exists (search; file one if none), then branch, implement, open a PR, and ARDI to clean. Use when asked to 'start a task', 'start a new task', or 'new task'. Use when Codex is asked to use `start-task`, `/start-task`, or the corresponding ai-config/Claude skill workflow."
---

# start-task (Codex wrapper)

This is a generated Codex wrapper around the canonical ai-config Claude skill.

Source: [skills/start-task/SKILL.md](../../skills/start-task/SKILL.md)

Before acting, read the source skill completely and follow its workflow, adapting it to Codex.

The source lives at `skills/start-task/SKILL.md` in the same ai-config checkout as this wrapper. If this wrapper was loaded through `${CODEX_HOME:-$HOME/.codex}/skills/start-task`, resolve the symlink target for this wrapper directory first, then read `../../skills/start-task/SKILL.md` relative to that real directory. Do not resolve that relative path from inside `${CODEX_HOME:-$HOME/.codex}/skills`, because it points back at the wrapper tree.

- Treat `user-invocable` and `allowed-tools` as Claude metadata, not Codex permissions.
- Use the tools available in this Codex session for equivalent operations.
- If the source mentions a Claude-only path such as `~/.claude/skills`, use this repository's `skills/` path while editing.
- Keep procedural changes in the canonical source skill unless the user specifically asks to change this wrapper.
