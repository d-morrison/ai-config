---
name: mma
description: Merge main into all open PR branches in the current repo. For every open PR, fetch, merge origin/main (and origin/<branch>) in, resolve conflicts, run the repo's pre-commit checks, and push — reusing sync-pr-branch's per-branch procedure, looped across the whole open-PR queue. Use on "merge main into all pr branches", "sync every open PR with main", "mma", or when several PRs have all drifted behind main at once (e.g. after a run of merges) and need resyncing in one pass.
user-invocable: true
allowed-tools:
  - Bash
  - Read
  - Edit
  - Write
  - Agent
---

# mma

Repo-wide fan-out of [`sync-pr-branch`](../sync-pr-branch/SKILL.md): instead
of resyncing one branch, resync **every currently-open PR** in the repo
against `main` (and each PR's own remote), so a burst of merges into `main`
doesn't leave the rest of the queue stale and conflict-prone.

This is not a duplicate of `sync-pr-branch` — it's an orchestration layer on
top of it. The per-branch mechanics (fetch, merge `origin/main`, merge
`origin/<branch>`, resolve conflicts, run checks, push) are unchanged; only
`sync-pr-branch` owns that logic. Keep it that way — if the per-branch steps
ever need to change, fix them in `sync-pr-branch` and this skill inherits the
fix for free.

## When this fires

- "merge main into all pr branches", "sync every open PR with main", "mma",
  "resync the whole queue with main".
- After a run of merges to `main` (e.g. finishing an `ardia`/`gia` sweep) —
  proactively, even without being asked, since every remaining open PR just
  fell further behind.

## The procedure

1. **List every open PR in the repo** (`mcp__github__list_pull_requests` /
   `gh pr list`). Note each PR's number and `headRefName`.

2. **Check whether main is actually ahead** before touching anything:
   ```bash
   git fetch origin main
   ```
   For a PR whose branch tip is already an ancestor of `origin/main`'s new
   position (rare, but possible right after a squash-merge cleanup), skip it
   — nothing to merge.

3. **Resync each PR branch, one at a time — do not parallelize the push
   step.** This is the
   [shared-runner exception](../../shared/workflow/when-to-orchestrate.md) in
   practice: several PRs is decomposable, but each push triggers that PR's
   own CI and `@claude` review bot on a runner the whole repo shares, and
   parallel pushes make per-PR status illegible and can race concurrency
   groups against each other (see `gha`'s own
   `claude-review-<PR>`/`cancel-in-progress` note for what that race looks
   like in practice). Work the queue serially, or cap concurrency low enough
   that no two pushes land in the same few seconds.

   For each PR branch, in its own worktree (never the shared main checkout —
   see the per-repo memory file for this repo's worktree conventions if it
   has one):
   ```bash
   git worktree add .claude/worktrees/pr-<N> origin/<branch>
   cd .claude/worktrees/pr-<N>
   ```
   Then run **exactly** the [`sync-pr-branch`](../sync-pr-branch/SKILL.md)
   procedure against that branch: fetch, merge `origin/main`, merge
   `origin/<branch>`, resolve any conflicts (see `resolve-conflicts` / `rc`),
   run the repo's pre-commit checks, push.

   **Only merge `origin/main` and the PR's own `origin/<branch>`** — never
   another open PR's branch. Cross-PR changes stay out of scope here, same
   as `sync-pr-branch`'s own note.

4. **A real conflict blocks that one PR, not the sweep.** If a merge needs
   real conflict resolution beyond a mechanical pick, resolve it inline when
   confident and small; when the resolution is ambiguous or
   architecturally significant, leave that PR's worktree in place (mid-merge
   is fine to pause on — don't force through it) and move to the next PR,
   then come back to it. Report which PRs needed real resolution versus
   which were a clean fast-forward-style merge with nothing to resolve.

5. **A push can 403 in a session scoped to only its own harness-assigned
   branch** (see `ai-config`'s own "Use the existing PR branch, not the
   harness-specified branch" note). When that happens, don't retry the plain
   push — it's a policy denial, not a transient failure. That same note's
   default fallback is to stack the merge as its own PR against the
   original branch, or ask the user directly — **not** to reach for
   `git push --force-with-lease` as a routine step. A force-push is
   destructive and needs the user's own live, per-instance authorization
   (see the top-level git-safety rules); don't bake it into this skill's
   default path even when a past session found the proxy permitted it —
   that was an environment-specific exception, not a standing grant.
   Surface the blocked PRs to the user rather than guessing at a workaround.

6. **Report a per-PR summary** at the end: which PRs were already up to
   date, which merged clean and pushed, which needed conflict resolution
   (and whether that's done or still open), and which are blocked on
   something outside this skill's scope (a push restriction, an ambiguous
   conflict needing the user's call).

## Notes

- Use the `Agent` tool to dispatch one background agent per PR when the
  queue is large (roughly 4+ branches) and each branch's resync is
  genuinely independent — but keep the **push** itself serial/capped per
  step 3's shared-runner reasoning; parallelize the fetch-and-merge
  groundwork, not the push.
- This skill only touches branches with an **open** PR. A stale local
  worktree left over from a merged PR isn't in scope — that's the
  `post-merge` skill's job.
- If every open PR is already current with `main`, say so and stop; nothing
  to do is a valid, common outcome right after this same skill last ran.
