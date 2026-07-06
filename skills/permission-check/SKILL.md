---
name: permission-check
description: "Read-only self-diagnostic for 'why is Claude Code prompting me for this' (or 'why isn't it'). Walks the permission config layers in resolution order (managed policy, CLI args, project-local, project-shared, user) and reports which layer's rule actually wins for a given tool/action pattern. Never edits config — see update-config for that. Use when asked to 'permission check', 'why does this keep prompting', 'why is this auto-allowed', 'check my permissions', 'diagnose permission prompt', or 'what rule controls this tool call'."
user-invocable: true
allowed-tools:
  - Bash
  - Read
---

# permission-check — diagnose why Claude Code is (or isn't) prompting

A read-only diagnostic: given a tool/action pattern (e.g. `Bash(rm:*)`,
`Edit`, `WebFetch(domain:example.com)`), walk every settings layer that can
carry a `permissions` block, find every rule that matches the pattern, and
report which one actually wins — and why.

This never edits a settings file. For *changing* permission config (adding an
allow entry, moving a rule to a different layer), hand off to `update-config`.

## When this fires

- "permission check", "why does this keep prompting me", "why is this
  auto-allowed", "check my permissions", "diagnose this permission prompt"
- "what rule controls `<tool pattern>`", "why did that just prompt when it
  didn't last time"

## The resolution model

Two independent things determine the outcome, and both matter:

1. **Layer precedence** decides which layer's rule set is even in play.
   Highest to lowest:
   1. **Managed policy settings** (cannot be overridden by anything below) —
      `/Library/Application Support/ClaudeCode/managed-settings.json` (+
      `managed-settings.d/`) on macOS, `/etc/claude-code/managed-settings.json`
      (+ `managed-settings.d/`) on Linux/WSL,
      `C:\Program Files\ClaudeCode\managed-settings.json` (+
      `managed-settings.d\`) on Windows.
   2. **CLI arguments** for this invocation (`--allowedTools`,
      `--disallowedTools`, `--permission-mode`).
   3. **Project-local settings** — `.claude/settings.local.json` (gitignored,
      personal).
   4. **Project-shared settings** — `.claude/settings.json` (checked in).
   5. **User settings** — `~/.claude/settings.json`.
2. **Rule-type precedence**, evaluated across ALL layers at once: **deny,
   then ask, then allow** — the first match in that order wins, and pattern
   specificity does **not** change this order. A `deny` rule in a
   *lower*-precedence layer still blocks a more specific `allow` rule in a
   *higher*-precedence layer (e.g. a project-shared `deny` on `Bash(aws *)`
   still blocks a project-local `allow` on `Bash(aws s3 ls)`). Managed-policy
   `deny` rules can't be bypassed by any layer, CLI flag, or hook.

Within a single rule type, the most specific matching pattern wins.

**Hooks** (`PreToolUse`) run *before* the permission prompt but don't bypass
this chain: a hook exiting with code 2 blocks before rule evaluation runs;
deny/ask rules are still evaluated regardless of what a hook's own
`"allow"` decision says.

Source: [Claude Code permissions
docs](https://code.claude.com/docs/en/permissions.md) (rule evaluation order,
hook interaction) and [settings
docs](https://code.claude.com/docs/en/settings.md) (layer list and paths). If
either page has since changed its ordering or paths, that page wins over this
skill's restatement — re-fetch it rather than trust this file blindly on a
stale point.

## Procedure

### 1. Get the exact pattern to diagnose

Ask for (or infer from context) the specific tool-call pattern — the same
shape a rule would use: `Bash(git push:*)`, `Edit`, `WebFetch(domain:x.com)`.
A vague description ("git stuff") isn't enough to match rule syntax
precisely; ask the user to narrow it if it's ambiguous.

### 2. Read every layer, in precedence order

```bash
# 1. Managed policy (host-global — see privacy gate below before reading)
# macOS:   /Library/Application Support/ClaudeCode/managed-settings.json
# Linux:   /etc/claude-code/managed-settings.json
# Windows: C:\Program Files\ClaudeCode\managed-settings.json
# (each may also have a managed-settings.d/ directory of fragments)

# 2. CLI args for this session — not a file; note if the invocation used
#    --allowedTools / --disallowedTools / --permission-mode

# 3. Project-local (gitignored, personal)
cat .claude/settings.local.json 2>/dev/null

# 4. Project-shared (checked in)
cat .claude/settings.json 2>/dev/null

# 5. User
cat ~/.claude/settings.json 2>/dev/null
```

**Privacy gate on layer 1 and layer 5.** The managed-policy file is
host-global, outside this project and outside the user's own home-relative
config — reading it can surface content unrelated to this session (org-wide
policy meant for a different audience). Only read it after telling the user
you're about to, and skip it if they'd rather not. The user-settings file
(`~/.claude/settings.json`) is personal but not host-global; read it without
asking, same as the project layers.

### 3. Extract every matching rule

For each layer that exists, pull its `permissions.allow` / `permissions.ask`
/ `permissions.deny` arrays and check each entry against the target pattern —
an exact match, a wildcard match (`Bash(git *)` matches
`Bash(git push:*)`), or a bare tool name (`Edit` matches any `Edit` call).
Record every hit with its layer and rule type; don't stop at the first one
found; the analysis needs the *full* set to apply the resolution model.

### 4. Apply the resolution model and report

1. Any `deny` hit, from any layer → **blocked**. Report that layer + rule as
   the reason, and note that no `allow` anywhere can override it.
2. Else any `ask` hit → **prompts** (with the layer + rule).
3. Else any `allow` hit → **auto-allowed** (with the layer + rule).
4. Else no hit anywhere → **prompts**, by Claude Code's own default (no rule
   means ask).

If a step finds more than one matching rule of the *winning* type (e.g. two
`allow` rules across different layers both match), name the most specific
one as the actual reason and note the others as also-matching but
non-deciding.

Report format:

```
Pattern: Bash(git push:*)

| Layer            | Rule type | Rule                | Matches? |
|------------------|-----------|----------------------|----------|
| Managed policy    | —         | (not present)        | —        |
| CLI args          | —         | (none passed)         | —        |
| Project-local     | allow     | Bash(git push:*)      | yes      |
| Project-shared    | —         | (no match)            | —        |
| User              | ask       | Bash(git *)           | yes (specificity loses to project-local) |

Verdict: auto-allowed — project-local's `Bash(git push:*)` allow rule wins
(no deny anywhere blocks it).
```

### 5. If nothing explains the observed behavior

If the reported verdict doesn't match what the user actually saw happen
(e.g. it should auto-allow per the rules but still prompted), say so plainly
rather than forcing a fit — flag the mismatch and suggest checking for a
hook (`PreToolUse`) that may be intercepting the call before rule evaluation,
or a session using `--permission-mode plan`/`bypassPermissions` that changes
the baseline. Don't guess at a hook's behavior; read `hooks` config in the
same settings files if one is suspected.

## Relationship to other skills

- **`update-config`** — the mutating counterpart. Once this skill identifies
  *which* layer and rule should change, hand off there to actually edit it;
  this skill never writes.
- **`fewer-permission-prompts`** — scans transcripts for *repeated* prompts
  and proposes an allowlist; this skill diagnoses a single pattern's current
  resolution on demand. Run `fewer-permission-prompts` when the question is
  "what should I allowlist", and `permission-check` when it's "why did/didn't
  this one thing prompt."

## Anti-patterns

- ❌ Editing a settings file to "fix" the prompt — that's `update-config`'s
  job; this skill only diagnoses.
- ❌ Reading the managed-policy file without telling the user first — it's
  host-global, not project- or user-scoped.
- ❌ Stopping at the first matching rule found instead of collecting all
  matches across every layer before applying the deny/ask/allow resolution
  order.
- ❌ Asserting a stale precedence rule from memory instead of checking the
  cited docs when the diagnosis doesn't match observed behavior.
