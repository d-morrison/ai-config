---
name: "adria"
description: "Codex wrapper for the ai-config Claude skill `adria`. Alias for `ardia` (common transposition typo). Apply ARDI to every open PR/MR in the repo \u2014 drive each to a clean review verdict. Use when asked to 'adria', 'drive all MRs to clean', or 'iterate all PRs'. Use when Codex is asked to use `adria`, `/adria`, or the corresponding ai-config/Claude skill workflow."
---

# adria (Codex wrapper)

This is a generated Codex wrapper around the canonical ai-config Claude skill.

Source: [skills/adria/SKILL.md](../../skills/adria/SKILL.md)

Before acting, read the source skill completely and follow its workflow, adapting it to Codex.

The source lives at `skills/adria/SKILL.md` in the same ai-config checkout as this wrapper. If this wrapper was loaded through `${CODEX_HOME:-$HOME/.codex}/skills/adria`, resolve the symlink target for this wrapper directory first, then read `../../skills/adria/SKILL.md` relative to that real directory. Do not resolve that relative path from inside `${CODEX_HOME:-$HOME/.codex}/skills`, because it points back at the wrapper tree.

- Treat `user-invocable` and `allowed-tools` as Claude metadata, not Codex permissions.
- Use the tools available in this Codex session for equivalent operations.
- If the source mentions a Claude-only path such as `~/.claude/skills`, use this repository's `skills/` path while editing.
- Keep procedural changes in the canonical source skill unless the user specifically asks to change this wrapper.
