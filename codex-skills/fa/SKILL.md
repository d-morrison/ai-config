---
name: "fa"
description: "Codex wrapper for the ai-config Claude skill `fa`. Alias for `fetch-all`. Run `git fetch` from origin across every git repo under a directory, reporting per-repo status (OK / updated / failed / skipped). Read-only \u2014 never merges or pulls. Use when asked to 'fa', 'fetch all', 'fetch from origin on all repos', or 'fetch every repo'. Use when Codex is asked to use `fa`, `/fa`, or the corresponding ai-config/Claude skill workflow."
---

# fa (Codex wrapper)

This is a generated Codex wrapper around the canonical ai-config Claude skill.

Source: [skills/fa/SKILL.md](../../skills/fa/SKILL.md)

Before acting, read the source skill completely and follow its workflow, adapting it to Codex.

The source lives at `skills/fa/SKILL.md` in the same ai-config checkout as this wrapper. If this wrapper was loaded through `${CODEX_HOME:-$HOME/.codex}/skills/fa`, resolve the symlink target for this wrapper directory first, then read `../../skills/fa/SKILL.md` relative to that real directory. Do not resolve that relative path from inside `${CODEX_HOME:-$HOME/.codex}/skills`, because it points back at the wrapper tree.

- Treat `user-invocable` and `allowed-tools` as Claude metadata, not Codex permissions.
- Use the tools available in this Codex session for equivalent operations.
- If the source mentions a Claude-only path such as `~/.claude/skills`, use this repository's `skills/` path while editing.
- Keep procedural changes in the canonical source skill unless the user specifically asks to change this wrapper.
