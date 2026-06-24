---
name: "merge-skills"
description: "Codex wrapper for the ai-config Claude skill `merge-skills`. Alias for `consolidate-skills`. Merge two or more genuinely-overlapping skills into one canonical skill plus thin alias stubs, preserving every existing invocation name. Use when asked to 'merge skills', 'merge overlapping skills', 'dedupe skills', or 'collapse duplicate skills'. Use when Codex is asked to use `merge-skills`, `/merge-skills`, or the corresponding ai-config/Claude skill workflow."
---

# merge-skills (Codex wrapper)

This is a generated Codex wrapper around the canonical ai-config Claude skill.

Source: [skills/merge-skills/SKILL.md](../../skills/merge-skills/SKILL.md)

Before acting, read the source skill completely and follow its workflow, adapting it to Codex.

The source lives at `skills/merge-skills/SKILL.md` in the same ai-config checkout as this wrapper. If this wrapper was loaded through `${CODEX_HOME:-$HOME/.codex}/skills/merge-skills`, resolve the symlink target for this wrapper directory first, then read `../../skills/merge-skills/SKILL.md` relative to that real directory. Do not resolve that relative path from inside `${CODEX_HOME:-$HOME/.codex}/skills`, because it points back at the wrapper tree.

- Treat `user-invocable` and `allowed-tools` as Claude metadata, not Codex permissions.
- Use the tools available in this Codex session for equivalent operations.
- If the source mentions a Claude-only path such as `~/.claude/skills`, use this repository's `skills/` path while editing.
- Keep procedural changes in the canonical source skill unless the user specifically asks to change this wrapper.
