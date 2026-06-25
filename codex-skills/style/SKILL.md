---
name: "style"
description: "Codex wrapper for the ai-config Claude skill `style`. Alias for `use-preferred-style`. Write or revise prose in the user's preferred style \u2014 limit dependent clauses, cut filler and jargon, prefer short declarative sentences joined by coordinating conjunctions. Use when asked to '/style', 'use my style', 'apply my preferred style', or 'tighten this prose'. Use when Codex is asked to use `style`, `/style`, or the corresponding ai-config/Claude skill workflow."
---

# style (Codex wrapper)

This is a generated Codex wrapper around the canonical ai-config Claude skill.

Source: [skills/style/SKILL.md](../../skills/style/SKILL.md)

Before acting, read the source skill completely and follow its workflow, adapting it to Codex.

The source lives at `skills/style/SKILL.md` in the same ai-config checkout as this wrapper. If this wrapper was loaded through `${CODEX_HOME:-$HOME/.codex}/skills/style`, resolve the symlink target for this wrapper directory first, then read `../../skills/style/SKILL.md` relative to that real directory. Do not resolve that relative path from inside `${CODEX_HOME:-$HOME/.codex}/skills`, because it points back at the wrapper tree.

- Treat `user-invocable` and `allowed-tools` as Claude metadata, not Codex permissions.
- Use the tools available in this Codex session for equivalent operations.
- If the source mentions a Claude-only path such as `~/.claude/skills`, use this repository's `skills/` path while editing.
- Keep procedural changes in the canonical source skill unless the user specifically asks to change this wrapper.
