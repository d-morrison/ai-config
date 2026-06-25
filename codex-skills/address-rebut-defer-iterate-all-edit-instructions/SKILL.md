---
name: "address-rebut-defer-iterate-all-edit-instructions"
description: "Codex wrapper for the ai-config Claude skill `address-rebut-defer-iterate-all-edit-instructions`. Alias for `ardiaei` (ARDIA + Edit Instructions). Drive every open PR/MR to a clean review verdict, then update memories and skills with what the loop taught. Use when asked to 'address rebut defer iterate all then edit instructions', 'clean all PRs and record what we learned', or 'drive everything to clean and update instructions'. Use when Codex is asked to use `address-rebut-defer-iterate-all-edit-instructions`, `/address-rebut-defer-iterate-all-edit-instructions`, or the corresponding ai-config/Claude skill workflow."
---

# address-rebut-defer-iterate-all-edit-instructions (Codex wrapper)

This is a generated Codex wrapper around the canonical ai-config Claude skill.

Source: [skills/address-rebut-defer-iterate-all-edit-instructions/SKILL.md](../../skills/address-rebut-defer-iterate-all-edit-instructions/SKILL.md)

Before acting, read the source skill completely and follow its workflow, adapting it to Codex.

The source lives at `skills/address-rebut-defer-iterate-all-edit-instructions/SKILL.md` in the same ai-config checkout as this wrapper. If this wrapper was loaded through `${CODEX_HOME:-$HOME/.codex}/skills/address-rebut-defer-iterate-all-edit-instructions`, resolve the symlink target for this wrapper directory first, then read `../../skills/address-rebut-defer-iterate-all-edit-instructions/SKILL.md` relative to that real directory. Do not resolve that relative path from inside `${CODEX_HOME:-$HOME/.codex}/skills`, because it points back at the wrapper tree.

- Treat `user-invocable` and `allowed-tools` as Claude metadata, not Codex permissions.
- Use the tools available in this Codex session for equivalent operations.
- If the source mentions a Claude-only path such as `~/.claude/skills`, use this repository's `skills/` path while editing.
- Keep procedural changes in the canonical source skill unless the user specifically asks to change this wrapper.
