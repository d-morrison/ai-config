---
name: "clear-all"
description: "Codex wrapper for the ai-config Claude skill `clear-all`. Alias for `gia` (Grab Issues + iterate-All). Clear the repo's entire work queue: open a PR for every open issue that lacks one, and drive every open PR to a clean review verdict with green CI. Use when asked to 'clear-all', 'clear all the work', 'clear everything', 'open PRs for all the issues and drive them clean', 'open a PR for every issue and make every PR green', or 'clear the whole queue'. Use when Codex is asked to use `clear-all`, `/clear-all`, or the corresponding ai-config/Claude skill workflow."
---

# clear-all (Codex wrapper)

This is a generated Codex wrapper around the canonical ai-config Claude skill.

Source: [skills/clear-all/SKILL.md](../../skills/clear-all/SKILL.md)

Before acting, read the source skill completely and follow its workflow, adapting it to Codex.

The source lives at `skills/clear-all/SKILL.md` in the same ai-config checkout as this wrapper. If this wrapper was loaded through `${CODEX_HOME:-$HOME/.codex}/skills/clear-all`, resolve the symlink target for this wrapper directory first, then read `../../skills/clear-all/SKILL.md` relative to that real directory. Do not resolve that relative path from inside `${CODEX_HOME:-$HOME/.codex}/skills`, because it points back at the wrapper tree.

- Treat `user-invocable` and `allowed-tools` as Claude metadata, not Codex permissions.
- Use the tools available in this Codex session for equivalent operations.
- If the source mentions a Claude-only path such as `~/.claude/skills`, use this repository's `skills/` path while editing.
- Keep procedural changes in the canonical source skill unless the user specifically asks to change this wrapper.
