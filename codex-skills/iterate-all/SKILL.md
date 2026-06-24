---
name: "iterate-all"
description: "Codex wrapper for the ai-config Claude skill `iterate-all`. Alias for `ardia`. Apply the review-until-clean loop to every open PR in the repo \u2014 drive each one to a clean review verdict in turn. Use when asked to 'iterate all', 'iterate all PRs', 'carry every open PR to clean', 'review-loop all my PRs', or to run the review-until-clean loop across the whole open-PR queue rather than a single PR. Use when Codex is asked to use `iterate-all`, `/iterate-all`, or the corresponding ai-config/Claude skill workflow."
---

# iterate-all (Codex wrapper)

This is a generated Codex wrapper around the canonical ai-config Claude skill.

Source: [skills/iterate-all/SKILL.md](../../skills/iterate-all/SKILL.md)

Before acting, read the source skill completely and follow its workflow, adapting it to Codex.

The source lives at `skills/iterate-all/SKILL.md` in the same ai-config checkout as this wrapper. If this wrapper was loaded through `${CODEX_HOME:-$HOME/.codex}/skills/iterate-all`, resolve the symlink target for this wrapper directory first, then read `../../skills/iterate-all/SKILL.md` relative to that real directory. Do not resolve that relative path from inside `${CODEX_HOME:-$HOME/.codex}/skills`, because it points back at the wrapper tree.

- Treat `user-invocable` and `allowed-tools` as Claude metadata, not Codex permissions.
- Use the tools available in this Codex session for equivalent operations.
- If the source mentions a Claude-only path such as `~/.claude/skills`, use this repository's `skills/` path while editing.
- Keep procedural changes in the canonical source skill unless the user specifically asks to change this wrapper.
