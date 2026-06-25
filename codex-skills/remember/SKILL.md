---
name: "remember"
description: "Codex wrapper for the ai-config Claude skill `remember`. Alias for `memorize`. Persist a fact or preference to memory, routed by relevance to project-specific or general scope. Use when the user says '/remember', 'remember that \u2026', 'from now on \u2026', 'always/never \u2026', or 'note that \u2026'. Use when Codex is asked to use `remember`, `/remember`, or the corresponding ai-config/Claude skill workflow."
---

# remember (Codex wrapper)

This is a generated Codex wrapper around the canonical ai-config Claude skill.

Source: [skills/remember/SKILL.md](../../skills/remember/SKILL.md)

Before acting, read the source skill completely and follow its workflow, adapting it to Codex.

The source lives at `skills/remember/SKILL.md` in the same ai-config checkout as this wrapper. If this wrapper was loaded through `${CODEX_HOME:-$HOME/.codex}/skills/remember`, resolve the symlink target for this wrapper directory first, then read `../../skills/remember/SKILL.md` relative to that real directory. Do not resolve that relative path from inside `${CODEX_HOME:-$HOME/.codex}/skills`, because it points back at the wrapper tree.

- Treat `user-invocable` and `allowed-tools` as Claude metadata, not Codex permissions.
- Use the tools available in this Codex session for equivalent operations.
- If the source mentions a Claude-only path such as `~/.claude/skills`, use this repository's `skills/` path while editing.
- Keep procedural changes in the canonical source skill unless the user specifically asks to change this wrapper.
