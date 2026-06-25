---
name: "merge-main"
description: "Codex wrapper for the ai-config Claude skill `merge-main`. Alias for `sync-pr-branch`. Sync the current branch with both `main` and its own remote \u2014 fetch origin, merge origin/main and origin/<current-branch> into local, resolve conflicts, run the repo's pre-commit checks, and push. Use when invoked as `/merge-main`, or on \"merge main in\", \"update the branch\", \"the branch is behind main\", or whenever main has moved ahead of a PR branch you're working on. Use when Codex is asked to use `merge-main`, `/merge-main`, or the corresponding ai-config/Claude skill workflow."
---

# merge-main (Codex wrapper)

This is a generated Codex wrapper around the canonical ai-config Claude skill.

Source: [skills/merge-main/SKILL.md](../../skills/merge-main/SKILL.md)

Before acting, read the source skill completely and follow its workflow, adapting it to Codex.

The source lives at `skills/merge-main/SKILL.md` in the same ai-config checkout as this wrapper. If this wrapper was loaded through `${CODEX_HOME:-$HOME/.codex}/skills/merge-main`, resolve the symlink target for this wrapper directory first, then read `../../skills/merge-main/SKILL.md` relative to that real directory. Do not resolve that relative path from inside `${CODEX_HOME:-$HOME/.codex}/skills`, because it points back at the wrapper tree.

- Treat `user-invocable` and `allowed-tools` as Claude metadata, not Codex permissions.
- Use the tools available in this Codex session for equivalent operations.
- If the source mentions a Claude-only path such as `~/.claude/skills`, use this repository's `skills/` path while editing.
- Keep procedural changes in the canonical source skill unless the user specifically asks to change this wrapper.
