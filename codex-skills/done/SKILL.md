---
name: "done"
description: "Codex wrapper for the ai-config Claude skill `done`. Alias for `wrap-up`. End-of-session wrap-up: verify the true state of every PR/issue/branch/working tree (never assume), report a linked final summary that surfaces anything still open or dangling, then run a UMS review to persist what was learned. Use when invoked as `/done`, or on 'done', 'all done', 'are we done?', 'wrap up', or 'finish up'. Use when Codex is asked to use `done`, `/done`, or the corresponding ai-config/Claude skill workflow."
---

# done (Codex wrapper)

This is a generated Codex wrapper around the canonical ai-config Claude skill.

Source: [skills/done/SKILL.md](../../skills/done/SKILL.md)

Before acting, read the source skill completely and follow its workflow, adapting it to Codex.

The source lives at `skills/done/SKILL.md` in the same ai-config checkout as this wrapper. If this wrapper was loaded through `${CODEX_HOME:-$HOME/.codex}/skills/done`, resolve the symlink target for this wrapper directory first, then read `../../skills/done/SKILL.md` relative to that real directory. Do not resolve that relative path from inside `${CODEX_HOME:-$HOME/.codex}/skills`, because it points back at the wrapper tree.

- Treat `user-invocable` and `allowed-tools` as Claude metadata, not Codex permissions.
- Use the tools available in this Codex session for equivalent operations.
- If the source mentions a Claude-only path such as `~/.claude/skills`, use this repository's `skills/` path while editing.
- Keep procedural changes in the canonical source skill unless the user specifically asks to change this wrapper.
