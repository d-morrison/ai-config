---
name: "always"
description: "Codex wrapper for the ai-config Claude skill `always`. Alias for `memorize` (synonym of `remember`). Persist a standing rule or preference to memory, routed by relevance to project-specific or general scope. Use when the user gives an always-apply directive \u2014 'always \u2026', 'never \u2026', 'from now on \u2026', 'I prefer \u2026' \u2014 or says '/always'. Use when Codex is asked to use `always`, `/always`, or the corresponding ai-config/Claude skill workflow."
---

# always (Codex wrapper)

This is a generated Codex wrapper around the canonical ai-config Claude skill.

Source: [skills/always/SKILL.md](../../skills/always/SKILL.md)

Before acting, read the source skill completely and follow its workflow, adapting it to Codex.

The source lives at `skills/always/SKILL.md` in the same ai-config checkout as this wrapper. If this wrapper was loaded through `${CODEX_HOME:-$HOME/.codex}/skills/always`, resolve the symlink target for this wrapper directory first, then read `../../skills/always/SKILL.md` relative to that real directory. Do not resolve that relative path from inside `${CODEX_HOME:-$HOME/.codex}/skills`, because it points back at the wrapper tree.

- Treat `user-invocable` and `allowed-tools` as Claude metadata, not Codex permissions.
- Use the tools available in this Codex session for equivalent operations.
- If the source mentions a Claude-only path such as `~/.claude/skills`, use this repository's `skills/` path while editing.
- Keep procedural changes in the canonical source skill unless the user specifically asks to change this wrapper.
