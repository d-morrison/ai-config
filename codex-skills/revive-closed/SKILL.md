---
name: "revive-closed"
description: "Codex wrapper for the ai-config Claude skill `revive-closed`. Alias for `rescue-closed`. Search closed issues and closed-but-unmerged PRs for the ones worth returning to, then triage and reopen the keepers. Use when asked to 'revive closed issues', 'revive a closed PR', 'resurrect stale issues', 'salvage abandoned PRs', or 'revive-closed'. Use when Codex is asked to use `revive-closed`, `/revive-closed`, or the corresponding ai-config/Claude skill workflow."
---

# revive-closed (Codex wrapper)

This is a generated Codex wrapper around the canonical ai-config Claude skill.

Source: [skills/revive-closed/SKILL.md](../../skills/revive-closed/SKILL.md)

Before acting, read the source skill completely and follow its workflow, adapting it to Codex.

The source lives at `skills/revive-closed/SKILL.md` in the same ai-config checkout as this wrapper. If this wrapper was loaded through `${CODEX_HOME:-$HOME/.codex}/skills/revive-closed`, resolve the symlink target for this wrapper directory first, then read `../../skills/revive-closed/SKILL.md` relative to that real directory. Do not resolve that relative path from inside `${CODEX_HOME:-$HOME/.codex}/skills`, because it points back at the wrapper tree.

- Treat `user-invocable` and `allowed-tools` as Claude metadata, not Codex permissions.
- Use the tools available in this Codex session for equivalent operations.
- If the source mentions a Claude-only path such as `~/.claude/skills`, use this repository's `skills/` path while editing.
- Keep procedural changes in the canonical source skill unless the user specifically asks to change this wrapper.
