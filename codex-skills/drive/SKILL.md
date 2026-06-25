---
name: "drive"
description: "Codex wrapper for the ai-config Claude skill `drive`. Alias for `ardi` (\"drive to clean\"). ARD + Iterate on a single PR/MR until the review verdict is clean: read the latest review, Address/Rebut/Defer every finding, push, re-request review, repeat until zero findings. Use when asked to 'drive', 'drive this PR', 'drive to clean', or 'drive this PR to clean'. Use when Codex is asked to use `drive`, `/drive`, or the corresponding ai-config/Claude skill workflow."
---

# drive (Codex wrapper)

This is a generated Codex wrapper around the canonical ai-config Claude skill.

Source: [skills/drive/SKILL.md](../../skills/drive/SKILL.md)

Before acting, read the source skill completely and follow its workflow, adapting it to Codex.

The source lives at `skills/drive/SKILL.md` in the same ai-config checkout as this wrapper. If this wrapper was loaded through `${CODEX_HOME:-$HOME/.codex}/skills/drive`, resolve the symlink target for this wrapper directory first, then read `../../skills/drive/SKILL.md` relative to that real directory. Do not resolve that relative path from inside `${CODEX_HOME:-$HOME/.codex}/skills`, because it points back at the wrapper tree.

- Treat `user-invocable` and `allowed-tools` as Claude metadata, not Codex permissions.
- Use the tools available in this Codex session for equivalent operations.
- If the source mentions a Claude-only path such as `~/.claude/skills`, use this repository's `skills/` path while editing.
- Keep procedural changes in the canonical source skill unless the user specifically asks to change this wrapper.
