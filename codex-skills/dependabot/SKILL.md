---
name: "dependabot"
description: "Codex wrapper for the ai-config Claude skill `dependabot`. Alias for `chores`. Triage and wrap up dependency-bump / `chore(...)` PRs from Dependabot/Renovate: classify by bump size, confirm CI is green, merge safe patch/minor bumps, and flag risky majors with a changelog summary. Use when asked to 'handle the dependabot PRs', 'process dependabot', 'merge the bump PRs', or 'dependency updates'. Use when Codex is asked to use `dependabot`, `/dependabot`, or the corresponding ai-config/Claude skill workflow."
---

# dependabot (Codex wrapper)

This is a generated Codex wrapper around the canonical ai-config Claude skill.

Source: [skills/dependabot/SKILL.md](../../skills/dependabot/SKILL.md)

Before acting, read the source skill completely and follow its workflow, adapting it to Codex.

The source lives at `skills/dependabot/SKILL.md` in the same ai-config checkout as this wrapper. If this wrapper was loaded through `${CODEX_HOME:-$HOME/.codex}/skills/dependabot`, resolve the symlink target for this wrapper directory first, then read `../../skills/dependabot/SKILL.md` relative to that real directory. Do not resolve that relative path from inside `${CODEX_HOME:-$HOME/.codex}/skills`, because it points back at the wrapper tree.

- Treat `user-invocable` and `allowed-tools` as Claude metadata, not Codex permissions.
- Use the tools available in this Codex session for equivalent operations.
- If the source mentions a Claude-only path such as `~/.claude/skills`, use this repository's `skills/` path while editing.
- Keep procedural changes in the canonical source skill unless the user specifically asks to change this wrapper.
