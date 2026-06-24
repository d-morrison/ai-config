---
name: "cdu"
description: "Codex wrapper for the ai-config Claude skill `cdu`. Alias for `check-dependency-updates`. Audit a repo for stale dependencies and surface available upgrades \u2014 pinned GitHub Actions tags/SHAs, renv.lock versions, pre-commit revs, Quarto/tool versions, submodules. Use when asked to 'cdu', 'check dependency updates', 'audit dependency freshness', 'are my dependencies stale', or 'should I bump the workflow SHAs'. Use when Codex is asked to use `cdu`, `/cdu`, or the corresponding ai-config/Claude skill workflow."
---

# cdu (Codex wrapper)

This is a generated Codex wrapper around the canonical ai-config Claude skill.

Source: [skills/cdu/SKILL.md](../../skills/cdu/SKILL.md)

Before acting, read the source skill completely and follow its workflow, adapting it to Codex.

The source lives at `skills/cdu/SKILL.md` in the same ai-config checkout as this wrapper. If this wrapper was loaded through `${CODEX_HOME:-$HOME/.codex}/skills/cdu`, resolve the symlink target for this wrapper directory first, then read `../../skills/cdu/SKILL.md` relative to that real directory. Do not resolve that relative path from inside `${CODEX_HOME:-$HOME/.codex}/skills`, because it points back at the wrapper tree.

- Treat `user-invocable` and `allowed-tools` as Claude metadata, not Codex permissions.
- Use the tools available in this Codex session for equivalent operations.
- If the source mentions a Claude-only path such as `~/.claude/skills`, use this repository's `skills/` path while editing.
- Keep procedural changes in the canonical source skill unless the user specifically asks to change this wrapper.
