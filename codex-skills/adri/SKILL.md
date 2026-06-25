---
name: "adri"
description: "Codex wrapper for the ai-config Claude skill `adri`. Alias for `ardi` (common transposition typo). ARD + Iterate on a single PR/MR until the review verdict is clean. Use when asked to 'adri', 'drive this PR to clean', or 'iterate this MR'. Use when Codex is asked to use `adri`, `/adri`, or the corresponding ai-config/Claude skill workflow."
---

# adri (Codex wrapper)

This is a generated Codex wrapper around the canonical ai-config Claude skill.

Source: [skills/adri/SKILL.md](../../skills/adri/SKILL.md)

Before acting, read the source skill completely and follow its workflow, adapting it to Codex.

The source lives at `skills/adri/SKILL.md` in the same ai-config checkout as this wrapper. If this wrapper was loaded through `${CODEX_HOME:-$HOME/.codex}/skills/adri`, resolve the symlink target for this wrapper directory first, then read `../../skills/adri/SKILL.md` relative to that real directory. Do not resolve that relative path from inside `${CODEX_HOME:-$HOME/.codex}/skills`, because it points back at the wrapper tree.

- Treat `user-invocable` and `allowed-tools` as Claude metadata, not Codex permissions.
- Use the tools available in this Codex session for equivalent operations.
- If the source mentions a Claude-only path such as `~/.claude/skills`, use this repository's `skills/` path while editing.
- Keep procedural changes in the canonical source skill unless the user specifically asks to change this wrapper.
