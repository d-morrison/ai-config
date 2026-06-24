---
name: "ai-tells"
description: "Codex wrapper for the ai-config Claude skill `ai-tells`. Alias for `find-ai-tells`. Scan a text (file, PR/MR diff, or pasted prose) for telltale signs of AI/LLM authorship and report each with location, severity, and a de-slopped revision; also a standing self-check on my own drafts. Use when asked to 'ai-tells', 'find AI tells', 'de-slop this', 'does this sound like AI', or 'check if this was written by AI'. Use when Codex is asked to use `ai-tells`, `/ai-tells`, or the corresponding ai-config/Claude skill workflow."
---

# ai-tells (Codex wrapper)

This is a generated Codex wrapper around the canonical ai-config Claude skill.

Source: [skills/ai-tells/SKILL.md](../../skills/ai-tells/SKILL.md)

Before acting, read the source skill completely and follow its workflow, adapting it to Codex.

The source lives at `skills/ai-tells/SKILL.md` in the same ai-config checkout as this wrapper. If this wrapper was loaded through `${CODEX_HOME:-$HOME/.codex}/skills/ai-tells`, resolve the symlink target for this wrapper directory first, then read `../../skills/ai-tells/SKILL.md` relative to that real directory. Do not resolve that relative path from inside `${CODEX_HOME:-$HOME/.codex}/skills`, because it points back at the wrapper tree.

- Treat `user-invocable` and `allowed-tools` as Claude metadata, not Codex permissions.
- Use the tools available in this Codex session for equivalent operations.
- If the source mentions a Claude-only path such as `~/.claude/skills`, use this repository's `skills/` path while editing.
- Keep procedural changes in the canonical source skill unless the user specifically asks to change this wrapper.
