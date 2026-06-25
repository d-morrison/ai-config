---
name: "iterate"
description: "Codex wrapper for the ai-config Claude skill `iterate`. Alias for `ardi`. Drive a single pull request to a clean review verdict by looping request-review \u2192 address every finding \u2192 re-request-review until there are zero flagged items. Use when asked to 'iterate', 'iterate until clean', 'address the review comments', '@claude review again and fix what it finds', or after opening a PR you want carried all the way to mergeable. Handles the @claude bot reviewer; for human reviewers, follows the `ard` skill's step 1 (gh pr view --comments plus the inline-thread API). Use when Codex is asked to use `iterate`, `/iterate`, or the corresponding ai-config/Claude skill workflow."
---

# iterate (Codex wrapper)

This is a generated Codex wrapper around the canonical ai-config Claude skill.

Source: [skills/iterate/SKILL.md](../../skills/iterate/SKILL.md)

Before acting, read the source skill completely and follow its workflow, adapting it to Codex.

The source lives at `skills/iterate/SKILL.md` in the same ai-config checkout as this wrapper. If this wrapper was loaded through `${CODEX_HOME:-$HOME/.codex}/skills/iterate`, resolve the symlink target for this wrapper directory first, then read `../../skills/iterate/SKILL.md` relative to that real directory. Do not resolve that relative path from inside `${CODEX_HOME:-$HOME/.codex}/skills`, because it points back at the wrapper tree.

- Treat `user-invocable` and `allowed-tools` as Claude metadata, not Codex permissions.
- Use the tools available in this Codex session for equivalent operations.
- If the source mentions a Claude-only path such as `~/.claude/skills`, use this repository's `skills/` path while editing.
- Keep procedural changes in the canonical source skill unless the user specifically asks to change this wrapper.
