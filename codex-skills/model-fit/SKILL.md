---
name: "model-fit"
description: "Codex wrapper for the ai-config Claude skill `model-fit`. Alias for `assess-model-fit`. Shorthand trigger for assessing whether the current model is sufficient or needs escalation. Use when you want a quicker invocation of assess-model-fit. Use when Codex is asked to use `model-fit`, `/model-fit`, or the corresponding ai-config/Claude skill workflow."
---

# model-fit (Codex wrapper)

This is a generated Codex wrapper around the canonical ai-config Claude skill.

Source: [skills/model-fit/SKILL.md](../../skills/model-fit/SKILL.md)

Before acting, read the source skill completely and follow its workflow, adapting it to Codex.

The source lives at `skills/model-fit/SKILL.md` in the same ai-config checkout as this wrapper. If this wrapper was loaded through `${CODEX_HOME:-$HOME/.codex}/skills/model-fit`, resolve the symlink target for this wrapper directory first, then read `../../skills/model-fit/SKILL.md` relative to that real directory. Do not resolve that relative path from inside `${CODEX_HOME:-$HOME/.codex}/skills`, because it points back at the wrapper tree.

- Treat `user-invocable` and `allowed-tools` as Claude metadata, not Codex permissions.
- Use the tools available in this Codex session for equivalent operations.
- If the source mentions a Claude-only path such as `~/.claude/skills`, use this repository's `skills/` path while editing.
- Keep procedural changes in the canonical source skill unless the user specifically asks to change this wrapper.
