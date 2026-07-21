# push-memory

Persist a **general-purpose** memory to the `ai-config` repo **from a session whose working repo is something else** (a product repo, `gha`, a data-analysis repo). This is the cross-repo companion to `memorize`: same routing and voice rules, different delivery.

`memorize`’s commit/push step assumes `ai-config` is your primary checkout, symlinked into `~/.claude/` by `bootstrap.sh`, with direct push to `main`. That breaks when you’re elsewhere:

- A session scoped to another repo may not have `ai-config` checked out at all — the `~/.claude/memories` symlink can be absent or dangling.
- Remote/web sessions can often push only to their assigned branch, so a direct push to `ai-config`’s `main` is rejected (`HTTP 403`).
- The current git context is the *other* repo, so a naive commit tangles the memory into that repo’s branch and working tree.

So this skill locates (or sidesteps) an `ai-config` checkout and delivers the memory on its own branch + PR, never touching the repo you’re working in.

## When this fires

- “push this to ai-config”, “add this to ai-config’s memory / `CLAUDE.md`”, “remember this globally from here”, “record this in ai-config even though we’re in `<other repo>`”, “/push-memory”.
- Any time you have a standing rule or reference fact worth keeping, the lesson is general (not tied to the repo you’re in), and `ai-config` is **not** your working repo.

If `ai-config` **is** your working repo (you’re on its `main`, symlinked, with push access), use `memorize` — it’s the shorter path. This skill is for the cross-repo case.

## First: is it actually a general-purpose memory for ai-config?

Two things route elsewhere before you go further:

- **Project-specific fact** — a convention or gotcha tied to ONE repo (“this repo renders with renv via `R_LIBS_USER`”). That belongs in that repo’s local project memory (`~/.claude/projects/<project-path>/memory/`) or its own `CLAUDE.md`, **not** in shared `ai-config`. Route it there (see `memorize`); don’t push it here.
- **Automated every-time action** (“after each commit run X”). Memory can’t execute it — that’s a **hook** in `settings.json` (use `update-config`). Say so and route it there.

What stays: a **general standing rule** (“always link PRs in tables”) → `CLAUDE.md`, or a **general reference fact** (“`gh` opens a pager — pipe to `cat`”) → a topical file in `memories/` (e.g. `tools.md`, `debugging.md`). These are exactly `memorize`’s two “general” scopes.

## Procedure

1.  **Route + choose the target file** using `memorize`’s rules: standing rule → `CLAUDE.md`; reference fact → the fitting `memories/<topic>.md`. When you add a *new* file under `memories/`, also add a row for it to `memories/MEMORY.md` (the index). Don’t duplicate — if the point is already recorded, update it in place rather than stacking a second copy.

2.  **Get the current content of the target file(s)** so you append in the right place and match the file’s voice — and decide your delivery path now, since reading and writing both follow it. In a **web/remote session, or with no usable local `ai-config` checkout**, use the GitHub file API (**Path A**, step 4): read with `mcp__github__get_file_contents` (`owner: d-morrison`, `repo: ai-config`). With a **clean local checkout you can branch in**, use a local worktree (**Path B**, step 4): read the file there.

3.  **Write** a concise bullet (one line preferred), matching the file’s voice; include the *why* if it isn’t obvious. Never edit files in the repo you’re working in — only the `ai-config` target file(s).

4.  **Deliver on a dedicated branch + PR.** Never push straight to `ai-config`’s `main`, and never entangle the change with the current repo’s branch. Pick the path that fits the session:

    **Path A — GitHub file API (remote/web; no local `ai-config` checkout).** The robust default when you’re in a web session or lack a clean checkout — it touches no working tree.

    1.  Branch off `main`: `mcp__github__create_branch` (`owner: d-morrison`, `repo: ai-config`, `from_branch: main`, `branch: memory/<slug>`). In a web session pinned to its assigned branch, use that assigned branch name instead.
    2.  Read each target with `mcp__github__get_file_contents` (keep the returned `sha`), edit locally, then write the updated file(s) on the branch — `mcp__github__create_or_update_file` per file, or `mcp__github__push_files` for several files in one commit (needed when you also touch `memories/MEMORY.md`).
    3.  Open the PR: `mcp__github__create_pull_request` (`base: main`, `head: <branch>`), body `Closes #<issue>` if a tracking issue exists.

    **Path B — local `ai-config` checkout you can safely branch in.** Resolve the repo root via this skill’s own symlink (the skill lives in `ai-config`):

    ``` bash
    acfg="$(git -C ~/.claude/skills/push-memory rev-parse --show-toplevel 2>/dev/null)"
    # Fall back to a sibling clone if that isn't a checkout here:
    [ -n "$acfg" ] || for d in ~/ai-config ~/Documents/GitHub/ai-config ../ai-config; do
      [ -d "$d/.git" ] && acfg="$(git -C "$d" rev-parse --show-toplevel)" && break
    done
    echo "${acfg:-NONE — use Path A}"
    ```

    That toplevel is the **main** checkout — it may be on another session’s branch or hold uncommitted edits. Don’t branch in place if it’s occupied; add a worktree off `origin/main` instead so you never disturb it:

    ``` bash
    git -C "$acfg" fetch origin main
    wt="$(mktemp -d)"
    git -C "$acfg" worktree add "$wt" -b memory/<slug> origin/main
    # edit "$wt"/CLAUDE.md or "$wt"/memories/<file>.md, then:
    git -C "$wt" add CLAUDE.md              # or: memories/<file>.md  (+ memories/MEMORY.md when adding a new memories file)
    git -C "$wt" commit -m "memory: <one-line summary>"
    git -C "$wt" push -u origin memory/<slug>
    ```

    Stage only the memory file(s) — never `git add -A`. Open the PR with `gh pr create` (or `mcp__github__create_pull_request`), then remove the worktree: `git -C "$acfg" worktree remove "$wt"`.

5.  **Follow through on the PR.** Opening it triggers the standing watch-and-ARDI rule: subscribe to its activity and drive the review to clean. A one-line memory PR is usually clean on the first pass, but don’t drop it — carry it to ready like any other PR.

6.  **Confirm**: one sentence — what was stored, which file, and the PR link.

## Don’t

- Don’t push a **project-specific** fact here — it belongs in that repo’s local memory or its own `CLAUDE.md`, not shared `ai-config`.
- Don’t edit or commit anything in the repo you’re working in — only the `ai-config` target file(s).
- Don’t push straight to `ai-config`’s `main`, and don’t `git add -A` — stage only the file(s) you wrote.
- Don’t run a full session review or touch skill files (that’s `ums`).
- Don’t store secrets, tokens, or passwords.

## Relationship to other skills

- **`memorize`** (`remember` / `always`) — the same routing and voice rules for the normal case: `ai-config` is your working repo, symlinked, and you push to its current branch directly. Reach for `memorize` there; reach for `push-memory` when `ai-config` is not the repo you’re in.
- **`ums`** — reviews the whole session and may also update skill definitions. `push-memory` stores exactly one memory the user names; it never scans or edits skills.
- **`update-config`** — where an “every-time action” belongs (a hook), since a memory can’t execute.
- **`config-ai`** — the broader router across skills/agents/memory/hooks/`gha` capabilities; its Step 3 fallback ladder (issue on target repo, then issue on the current repo for transfer) covers the case one rung past this skill’s Path A/B — when the session has no API/branch access to `ai-config` at all, not just a different working repo.

Back to top
