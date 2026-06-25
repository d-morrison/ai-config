---
name: "find-duplicates"
description: "Codex wrapper for the ai-config Claude skill `find-duplicates`. Alias for `find-overlap`. Read-only detector of overlapping or redundant content across a corpus (skills, memories, docs, prose, any file set) \u2014 clusters comparable units, classifies them, and reports a disposition without editing anything. Use when asked to 'find duplicates', 'find redundant content', 'dedupe audit', or 'what's redundant here'. Use when Codex is asked to use `find-duplicates`, `/find-duplicates`, or the corresponding ai-config/Claude skill workflow."
---

# find-duplicates (Codex wrapper)

This is a generated Codex wrapper around the canonical ai-config Claude skill.

Source: [skills/find-duplicates/SKILL.md](../../skills/find-duplicates/SKILL.md)

Before acting, read the source skill completely and follow its workflow, adapting it to Codex.

The source lives at `skills/find-duplicates/SKILL.md` in the same ai-config checkout as this wrapper. If this wrapper was loaded through `${CODEX_HOME:-$HOME/.codex}/skills/find-duplicates`, resolve the symlink target for this wrapper directory first, then read `../../skills/find-duplicates/SKILL.md` relative to that real directory. Do not resolve that relative path from inside `${CODEX_HOME:-$HOME/.codex}/skills`, because it points back at the wrapper tree.

- Treat `user-invocable` and `allowed-tools` as Claude metadata, not Codex permissions.
- Use the tools available in this Codex session for equivalent operations.
- If the source mentions a Claude-only path such as `~/.claude/skills`, use this repository's `skills/` path while editing.
- Keep procedural changes in the canonical source skill unless the user specifically asks to change this wrapper.
