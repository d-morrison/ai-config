---
name: "cw"
description: "Codex wrapper for the ai-config Claude skill `cw`. Alias for `clean-worktrees`. Sweep dead git worktrees in the current repo \u2014 prune admin stubs, then remove linked worktrees whose branch merged (or is gone) and whose tree is clean, never touching the main/current worktree, a dirty tree, or one with a live session. Use when asked to 'cw', 'clean worktrees', 'prune worktrees', or 'clean dead worktrees'. Use when Codex is asked to use `cw`, `/cw`, or the corresponding ai-config/Claude skill workflow."
---

# cw (Codex wrapper)

This is a generated Codex wrapper around the canonical ai-config Claude skill.

Source: [skills/cw/SKILL.md](../../skills/cw/SKILL.md)

Before acting, read the source skill completely and follow its workflow, adapting it to Codex.

The source lives at `skills/cw/SKILL.md` in the same ai-config checkout as this wrapper. If this wrapper was loaded through `${CODEX_HOME:-$HOME/.codex}/skills/cw`, resolve the symlink target for this wrapper directory first, then read `../../skills/cw/SKILL.md` relative to that real directory. Do not resolve that relative path from inside `${CODEX_HOME:-$HOME/.codex}/skills`, because it points back at the wrapper tree.

- Treat `user-invocable` and `allowed-tools` as Claude metadata, not Codex permissions.
- Use the tools available in this Codex session for equivalent operations.
- If the source mentions a Claude-only path such as `~/.claude/skills`, use this repository's `skills/` path while editing.
- Keep procedural changes in the canonical source skill unless the user specifically asks to change this wrapper.
