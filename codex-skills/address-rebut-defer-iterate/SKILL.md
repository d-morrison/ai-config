---
name: "address-rebut-defer-iterate"
description: "Codex wrapper for the ai-config Claude skill `address-rebut-defer-iterate`. Alias for `ardi`. ARD + Iterate on a single PR/MR until the review verdict is clean. Use when asked to 'address rebut defer iterate', 'drive this PR to clean', or 'iterate this MR'. Use when Codex is asked to use `address-rebut-defer-iterate`, `/address-rebut-defer-iterate`, or the corresponding ai-config/Claude skill workflow."
---

# address-rebut-defer-iterate (Codex wrapper)

This is a generated Codex wrapper around the canonical ai-config Claude skill.

Source: [skills/address-rebut-defer-iterate/SKILL.md](../../skills/address-rebut-defer-iterate/SKILL.md)

Before acting, read the source skill completely and follow its workflow, adapting it to Codex.

The source lives at `skills/address-rebut-defer-iterate/SKILL.md` in the same ai-config checkout as this wrapper. If this wrapper was loaded through `${CODEX_HOME:-$HOME/.codex}/skills/address-rebut-defer-iterate`, resolve the symlink target for this wrapper directory first, then read `../../skills/address-rebut-defer-iterate/SKILL.md` relative to that real directory. Do not resolve that relative path from inside `${CODEX_HOME:-$HOME/.codex}/skills`, because it points back at the wrapper tree.

- Treat `user-invocable` and `allowed-tools` as Claude metadata, not Codex permissions.
- Use the tools available in this Codex session for equivalent operations.
- If the source mentions a Claude-only path such as `~/.claude/skills`, use this repository's `skills/` path while editing.
- Keep procedural changes in the canonical source skill unless the user specifically asks to change this wrapper.
