---
name: "send-upstream"
description: "Codex wrapper for the ai-config Claude skill `send-upstream`. Alias for `sup`. File an issue or open a PR on an upstream repo (fork parent, dependency, external project). Use when asked to 'send upstream', 'file upstream issue', 'upstream PR', or 'contribute this fix back'. Use when Codex is asked to use `send-upstream`, `/send-upstream`, or the corresponding ai-config/Claude skill workflow."
---

# send-upstream (Codex wrapper)

This is a generated Codex wrapper around the canonical ai-config Claude skill.

Source: [skills/send-upstream/SKILL.md](../../skills/send-upstream/SKILL.md)

Before acting, read the source skill completely and follow its workflow, adapting it to Codex.

The source lives at `skills/send-upstream/SKILL.md` in the same ai-config checkout as this wrapper. If this wrapper was loaded through `${CODEX_HOME:-$HOME/.codex}/skills/send-upstream`, resolve the symlink target for this wrapper directory first, then read `../../skills/send-upstream/SKILL.md` relative to that real directory. Do not resolve that relative path from inside `${CODEX_HOME:-$HOME/.codex}/skills`, because it points back at the wrapper tree.

- Treat `user-invocable` and `allowed-tools` as Claude metadata, not Codex permissions.
- Use the tools available in this Codex session for equivalent operations.
- If the source mentions a Claude-only path such as `~/.claude/skills`, use this repository's `skills/` path while editing.
- Keep procedural changes in the canonical source skill unless the user specifically asks to change this wrapper.
