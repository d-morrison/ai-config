# merge-it — merge a ready PR, then wrap up automatically

The active counterpart to `post-merge`. When I say “merge it”, I mean: do the merge now (the PR is ready), then run the whole post-merge wrap-up (verify → tidy → UMS) **on your own, without asking**. Asking “want me to run UMS?” after merging is the exact gap this skill closes — the answer is a standing yes (see `preferences.md`).

## When this fires

- “merge it”, “merge this”, “merge the PR”, “go ahead and merge” (as an explicit merge directive). Deliberately excludes vague approval like “ship it” / “lgtm” — merging is irreversible, so require an explicit merge verb.
- Distinct from `merge-main` / `sync-pr-branch` (those merge `main` *into* a branch to sync it — they do NOT merge the PR).
- If the PR is **already merged**, skip steps 2–3 and go straight to step 4 (`post-merge`).

## Procedure

### 1. Identify the PR and confirm it’s ready — never assume

- Resolve which PR is meant (the one from the current session; if ambiguous, ask which number).
- Confirm it is **fully clean** before merging (the ARDI terminal state — see `shared/workflow/fully-clean.md`): every CI workflow and check run — not just required ones — is green **and completed** (never still queued or in progress) AND the latest review is clean. Verify with a fresh query, not a cached verdict: `mcp__github__pull_request_read` (`get` for `mergeable_state`, `get_check_runs` for CI) — or `gh pr view <N>` / `gh pr checks <N>` in a local session. `get_check_runs`/`gh pr checks` only cover check runs (plus legacy statuses), not every raw Actions workflow run — see `fully-clean.md`’s `action_required`-with-zero-jobs gotcha if something looks off despite an all-clear checks view.
- Check `mergeStateStatus` in addition to `mergeable`. A PR can be `"MERGEABLE"` but `"BLOCKED"` when branch protection requires at least one approving review and only bot/comment reviews exist. Fix: request `d-morrison` as reviewer (`gh pr edit <N> --add-reviewer d-morrison` — `EDIT_PR`) and leave a note that the PR is clean and ready. Don’t attempt to force-merge.
- If any CI workflow or check run is red or still in progress/queued/pending, or the review still has open findings, **do not merge**. Report what’s blocking instead. (Only merge a not-clean PR if the user explicitly says to anyway.)

### 2. Merge

- Default to **squash** for a feature branch with many small iteration commits (and/or a merge-of-main commit) — it gives `main` one clean commit. Use a plain merge commit only if the user asks or the repo clearly prefers it; don’t stop to ask for a method on a routine feature PR.
- Give the squash an accurate **commit title and body** when the PR body has gone stale across the review loop — pass `commit_title` / `commit_message` rather than letting GitHub paste the outdated description. Keep `Closes #N` in the message so the linked issue auto-closes.
- If `gh pr merge` fails with `Head branch is out of date`, first read the PR’s actual base branch (`gh pr view <N> --json baseRefName -q .baseRefName` — do **not** assume `main`; stacked and release PRs target a different base), sync that base into the PR branch, and retry once. **Syncing the base creates a new head SHA, which invalidates the CI/review “fully clean” snapshot that authorized the original merge attempt** — re-run the ARDI “fully clean” check (`fully-clean.md`) against the new SHA before retrying the merge, don’t just retry the merge command itself; a repo that doesn’t make every workflow/review a required branch-protection check can otherwise merge an unreviewed/untested new head. If the merge still fails, don’t compare against `origin` blindly — for a cross-fork PR, `origin` is the *base* repo, not necessarily where the head branch lives, so `git ls-remote origin refs/heads/<branch>` can silently read a missing ref or an unrelated same-named branch in the base repo. Get the actual head repo and ref from the PR API first (`gh pr view <N> --json headRepositoryOwner,headRepository,headRefName`), then query *that* repo’s ref (`gh api repos/<head-owner>/<head-repo>/git/refs/heads/<head-ref> --jq .object.sha` — verified this endpoint works) and compare it against the PR API’s own `.head.sha` (`gh api repos/<owner>/<repo>/pulls/<N> --jq .head.sha`) — the PR object can lag the branch ref briefly, so the correct response is to **wait** until the two agree, not to keep retrying blindly. Only use `--admin` as a last resort when the user has **separately and explicitly** authorized the branch-protection bypass itself — ordinary merge authorization does **not** cover it (see `preferences.md`).

``` bash
# MERGE_PR — remote/web (GitHub MCP):
#   mcp__github__merge_pull_request  merge_method=squash  commit_title=…  commit_message=…
# local:
gh pr merge <N> --squash --subject "<title>" --body "<accurate summary; Closes #N>"
```

In remote/web sessions, load the merge tool’s schema with `ToolSearch` (`select:mcp__github__merge_pull_request`) before the first call to confirm the exact name and parameters — the `d-morrison/gha` CLAUDE.md mapping table (`tools.md`) is the canonical `gh`→MCP reference.

### 3. Verify the merge landed — never assume

Confirm `merged == true` (the merge tool’s result) and re-check the PR state and that the linked issue auto-closed. If the merge didn’t land (conflict, branch protection, not mergeable), **stop and report** — don’t tidy or run UMS.

### 4. Chain into `post-merge` — automatically

Run the `post-merge` skill (invoke it by name) for the rest: tidy the local branch (checkout `main`, pull, `git branch -d`, remove any worktree), confirm deferred items are tracked, and **run UMS** to bank what the PR’s review lifecycle taught. Do this without a separate prompt — opening the UMS follow-up branch + PR is a standing yes (`preferences.md`).

## Relationship to other skills

- **`post-merge`** — step 4 delegates to it. `post-merge` assumes the PR is already merged (verify → tidy → UMS); `merge-it` adds the actual merge in front of it for the “it’s clean, merge it” case.
- **`merge-main` / `sync-pr-branch`** — merge `main` INTO a PR branch to sync; unrelated to merging the PR itself. Don’t confuse the trigger words.
- **`ardi` / `iterate`** — the loop that gets a PR to fully-clean; `merge-it` is what you run once it’s there and the user says go.
- **`ums`** — the learnings step `post-merge` runs at the end.
- **`wrap-up` / `merged`** — session-level bookend; `merge-it` is per-PR.

## Anti-patterns

- ❌ Asking “want me to run UMS / wrap up?” after merging — it’s automatic.
- ❌ Reporting the merge as done and moving on (including to other things the user said while the merge was in flight) without actually running step 4 — a busy, multi-threaded conversation makes this easy to drop, but the chain isn’t optional follow-up; it’s part of the merge action itself. See `mwc`’s own anti-pattern entry for the concrete case this happened in.
- ❌ Merging a PR that isn’t fully clean (red or still-in-progress CI, or open findings) without the user explicitly saying so.
- ❌ Letting the squash commit inherit a stale PR description — pass an accurate title/body when the body no longer matches the final diff.
- ❌ Confusing “merge it” (merge the PR) with “merge main” (sync the branch).
- ❌ `git branch -D` (force) in the tidy without checking why `-d` refused.

Back to top
