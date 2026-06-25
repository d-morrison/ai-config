---
name: "ph"
description: "Codex wrapper for the ai-config Claude skill `ph`. Alias for `purge-hallucinations`. Audit a target (memory/instruction corpus, repo code & docs, or an explicit file / PR diff / pasted AI output) for fabricated references that don't resolve \u2014 missing files, undefined functions, non-existent action refs/versions, dead URLs, dangling `[[memory-links]]`, fake skill names/citations/flags \u2014 then interactively propose a fix for each. Use when asked to 'ph', 'purge hallucinations', 'check for hallucinations', or 'verify the references'. Use when Codex is asked to use `ph`, `/ph`, or the corresponding ai-config/Claude skill workflow."
---

# ph (Codex wrapper)

This is a generated Codex wrapper around the canonical ai-config Claude skill.

Source: [skills/ph/SKILL.md](../../skills/ph/SKILL.md)

Before acting, read the source skill completely and follow its workflow, adapting it to Codex.

The source lives at `skills/ph/SKILL.md` in the same ai-config checkout as this wrapper. If this wrapper was loaded through `${CODEX_HOME:-$HOME/.codex}/skills/ph`, resolve the symlink target for this wrapper directory first, then read `../../skills/ph/SKILL.md` relative to that real directory. Do not resolve that relative path from inside `${CODEX_HOME:-$HOME/.codex}/skills`, because it points back at the wrapper tree.

- Treat `user-invocable` and `allowed-tools` as Claude metadata, not Codex permissions.
- Use the tools available in this Codex session for equivalent operations.
- If the source mentions a Claude-only path such as `~/.claude/skills`, use this repository's `skills/` path while editing.
- Keep procedural changes in the canonical source skill unless the user specifically asks to change this wrapper.
