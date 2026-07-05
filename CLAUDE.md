# User-wide Claude Code instructions

<!--
Some sections below pull their body from a fragment in `shared/` via Claude
Code's `@path` import (e.g. `@shared/writing/plain-prose.md`). Those fragments
are the single source of truth for guidance shared with the UCD-SERG lab manual,
which transcludes the same files. Edit the fragment, not the inlined copy, and
keep fragments ASCII (write `---` for em-dashes) so the manual's character check
passes. See README.md, "Shared content".
-->

## Run UMS proactively, as learnings accumulate

Don't wait for `/clear` or the end of a task to run `ums` (Update Memories and Skills).
As soon as a learning worth saving shows up during a session — a corrected mistake, a new preference, a tool quirk, a workflow gap — run UMS right then, interleaved with the main work, rather than batching it for a wrap-up step at the end.

Still run UMS before `/clear` too, as a final catch-all for anything accumulated since the last proactive pass — but treat that as a backstop, not the trigger to wait for.

## Keep ai-config and repo checkouts fresh

In every session — at session start, and again periodically during long sessions — refresh the local state that goes stale as PRs merge elsewhere:

1. **The ai-config checkout.** Check that the local ai-config clone is on `main` — not a leftover work branch from an earlier session — and run `git pull --ff-only`.
   Only switch back to `main` when the working tree is clean; leave a dirty tree or another session's in-flight work alone and flag it instead.
   **If `pull --ff-only` fails with "diverged" rather than a dirty-tree error**, don't assume unpushed work is at risk — a fresh container can seed local `main` from a stale/orphaned snapshot (e.g. a pre-history-rewrite state) whose commits never landed on `origin/main` at all.
   Confirm the working tree is clean (`git status --short`) and spot-check a couple of the "unique" local commit messages against `git log origin/main` — if they don't appear there either (not even under a different hash), the divergent commits are orphaned, not real work, and it's safe to realign: `git checkout -B main origin/main`.
   Still flag it rather than force if the tree is dirty or the messages *do* look like genuine unpushed work.
   **If `main` isn't the currently checked-out branch** (the session is already working on a feature branch), skip the checkout dance entirely — `git branch -f main origin/main` realigns the ref in place without touching the working tree or switching away from the branch you're actively on.
2. **The `~/.claude` consumer copies.** On symlink-capable systems the children of `~/.claude` (`skills/`, `shared/`, `commands/`, `memories/`) are symlinks into the checkout, so the pull alone refreshes them; rerun `bootstrap.sh` only when the repo gained a new top-level dir.
   On Windows, Git Bash `ln -s` silently falls back to **real copies**, so a pull does NOT propagate there — copy-sync every file whose repo version changed into `~/.claude`.
   Before overwriting, check for edits made directly in `~/.claude` (a diff that adds prose the repo lacks) and upstream the genuine ones into the repo first; never clobber an un-upstreamed local edit.
   Don't rely on mtime to spot local edits — git operations reset mtimes on checkout, so it false-positives right after a `pull`, the case this check most needs to handle correctly.
3. **The working repo's main checkout.** Fast-forward the `main` checkout of whatever repo the session is working on (`git fetch origin`, then `git pull --ff-only` when `main` is checked out) — it goes stale as the session's own PRs and other sessions' PRs merge.
4. **The `.ai-config` submodule pin, in any repo that vendors ai-config as a git submodule** (check `.gitmodules` for a `.ai-config` entry — not every repo has one; most consume ai-config only via the Plugin Marketplace, which doesn't need this). Compare the pinned commit against ai-config's current `origin/main`: `git rev-parse HEAD:.ai-config` for the pin's SHA, then `git -C <path-to-a-local-ai-config-clone> rev-list --count <pin>..origin/main` for how far behind it is.
   A pin more than a few weeks or dozens of commits stale is worth refreshing: file a tracking issue, bump it (`git submodule update --init --remote .ai-config` from the parent repo handles both init and fetch in one step; or, if already checked out, `git fetch origin` inside the submodule before `git checkout origin/main`), then `git add .ai-config` in the parent repo to record the new gitlink, verify the parent repo's own checks still pass, and open a PR.
   Before assuming this is risk-free, check whether the parent repo's CI actually reads the submodule's checked-out content (vs. treating it as inert until a dev runs `git submodule update --init` locally) — a pin bump is a pure pointer change with no functional surface only when nothing reads it. (First done on `Lacaedemon/sparta` [PR #651](https://github.com/Lacaedemon/sparta/pull/651): the pin was 325 commits (~9 days) stale, unreferenced by CI, and not checked out by default.)
   **When the current checkout isn't `main` itself** (a feature branch or a worktree), `HEAD:.ai-config` only reflects that branch's own pin — it can look badly stale purely because the branch was cut before a bump PR merged into `main`, not because the project's actual pin needs refreshing. Also check `origin/main:.ai-config` (the pin as recorded on the base branch) against ai-config's `origin/main`; if that one is already fresh, no bump PR is needed — the branch's own pin resolves itself on its next merge/rebase. On Windows Git Bash, that comparison command hits an MSYS gotcha — see `memories/tools.md`. (Re-discovered on `Lacaedemon/sparta`'s `claude/infallible-lewin-5841e9` branch, 2026-07-04: the branch's own pin read 344 commits stale while `main`'s was only 19 commits behind.)

## Timestamp recaps in local time

When printing a status recap or summary, include a timestamp in the user's local time zone (Pacific Time, `America/Los_Angeles` — get it from `TZ=America/Los_Angeles date "+%Y-%m-%d %H:%M %Z"`; the explicit `TZ` enforces PT on a machine set to any other zone).
This makes "as of when" unambiguous when the user reads the recap later.

**Check the `%Z` in the output.** On Windows Git Bash the `TZ` override silently falls back to GMT (any IANA zone name does), so the command above prints GMT, not PT.
If the suffix isn't PDT/PST, fall back to plain `date` when the machine's system zone is already Pacific.
Otherwise use PowerShell: `[System.TimeZoneInfo]::ConvertTimeBySystemTimeZoneId([DateTime]::UtcNow, 'Pacific Standard Time')`.
Note the output format differs from the bash command — it's a raw `DateTime` with no timezone-abbreviation field, so format it yourself if you need the `PDT`/`PST` suffix or a compact form.

## Bare queue-command keywords

I maintain a family of slash skills for managing the task queue and amending requests: `/also`, `/first`, `/next`, `/before`, `/last`, `/and`, `/remember`, and `/always`.
When I write one of these keywords **without the leading slash** as a directive — e.g. "also fix the test", "remember that ...", "always link PRs in tables", "and bold it", "next, run the spellcheck", "first, revert that" — interpret it using the corresponding skill's semantics rather than as ordinary prose. (`/remember` and `/always` both route to the `memorize` skill.)
When the word is genuinely just part of a sentence (ambiguous), fall back to the plain reading.

## Link PRs in tables

When listing PRs in a table (or anywhere they could be clickable), make each PR number a markdown link to the PR URL — `[#237](https://github.com/<owner>/<repo>/pull/237)`.
The plain text form forces the user to copy/paste; the linked form lets them open the PR in one click.

## Tag chat output by category so long recaps stay scannable

Recaps get long across many parallel tracks, so tag categories of output with a stable marker and let the eye jump straight to what needs the user's attention.
Terminal markdown can't force text color, so the emoji plus the `===` frame plus the bold label *is* the signal.
Readers skim past a question or a flag buried mid-paragraph; a marked, set-apart block is harder to miss.

Reserve a **`===` box** for the output a user is waiting on — something they must respond to (a question, an offer, a blocker) or the headline answer they asked for — and use a lighter **emoji-prefix** (bold label, no box) for informational categories they can skim.
Boxing everything defeats the purpose, so keep the box meaningful.

Boxed (a `===` line above and below the labeled block):

- ❓ **QUESTION** — need the user's input. For a real either/or, prefer the AskUserQuestion picker over a boxed question. When a question is posed inline in chat prose rather than through a box, still set it apart — its own paragraph (blank line before and after, since a bare newline collapses back into the surrounding paragraph), in bold.
- 💡 **OFFER** — optional work I can do if they want it.
- 🛑 **BLOCKER** — stopped; need their call.
- ✅ **ANSWER** — the headline answer to a question they asked (put nuance below the box).

Prefixed, no box (informational, frequent):

- 📊 **UPDATE** — status or progress.
- ⚠️ **FLAG** — non-blocking heads-up or risk.
- ✔️ **DONE** — a completed action.
- 🟢 **ALL CLEAR** — nothing needs the user right now; work continues in the background. The recap's standing sign-off.

Keep the markers stable so they become muscle memory.
The set-apart ❓ **QUESTION** format also gives the `prompt-me` / `prompt-me-all` skills a reliable signal to key off when they sweep the transcript for unanswered questions later.
The user may tune the emoji set; the full taxonomy and rationale live in `memories/preferences.md`.

## Title Claude sessions with the PR/issue number

Name each Claude Code session (the title shown in the web/app session sidebar) `#NNN brief description` — the number of the PR or issue the session is working, then a short description.
Don't prefix it with "PR" or "Issue"; just the bare `#NNN`.
So `#316 session title convention`, not `PR #316 session title convention` or `PR session title convention`.

## Re-check for latest review findings before reporting PR status

**Before** reporting status on a PR (especially "clean" / "ready to merge"), re-read the **most recent** review comment on the PR.
Don't trust an earlier "verdict" you've cached — a new review may have been posted since (by the @claude bot, by a human, or by a re-trigger), and that newer review may contain findings the old one missed.

Specifically: when scanning checks (`gh pr checks`) shows green or "no failures", that's about CI state, **not** review verdict.
Always pull the latest claude comment (`gh pr view N --json comments --jq '[.comments[] | select(.author.login == "claude")] | last | .body'`) and parse it for any "Findings", "Issues", "Remaining" sections before declaring a PR ready.

**Also check formal GitHub reviews, not just issue-style comments — a human's `CHANGES_REQUESTED` can be invisible to a comments-only scan.** A review submitted via GitHub's review UI (as opposed to a plain PR comment) shows up in `gh pr view N --json reviews`, and its top-level `body` is frequently **empty** — the actual finding lives entirely in a per-line inline comment, which only appears via `gh api repos/<owner>/<repo>/pulls/N/comments` (a different endpoint from issue comments). Checking `--json comments` alone can miss the review's existence entirely. Before declaring a PR ready, also run:
```
gh pr view N --json reviews --jq '.reviews[] | select(.state == "CHANGES_REQUESTED") | "\(.author.login) \(.submittedAt)"'
gh api repos/<owner>/<repo>/pulls/N/comments --jq '.[] | "\(.path):\(.line // .original_line // "?") \(.user.login) \(.body)"'
```
A `CHANGES_REQUESTED` state is blocking regardless of whether an automated re-review later says "Ready for merge" — that bot verdict doesn't clear a human's own review state, which only the human (or an explicit dismissal) can resolve.

(A specific case of the standing **never assume; always verify** rule in `memories/preferences.md` — confirm the verdict with a fresh query, don't recall it.)

## Post in-chat feedback to the PR

When the user gives feedback, corrections, or guidance in the CLI or chat while working a PR, paraphrase it and post it as a PR comment:

```
gh pr comment <N> --body "..."
```

One to three sentences is enough.
Don't quote verbatim — paraphrase so it reads naturally in the PR thread.
Skip trivial acknowledgments or conversational exchanges with nothing to act on.

This makes context visible to future @claude sessions, other reviewers, and contributors who only see the PR thread.

## Claim a GitHub PR/issue before working on it

<!-- Shared with the lab manual; edit shared/workflow/claim-pr.md, not here. -->
@shared/workflow/claim-pr.md

The `claim-pr` skill operationalizes this (the exact claim wording, when it applies, and the closing/unclaim comment).

## Open a PR immediately after claiming an issue

@shared/workflow/pr-on-claim.md

The strong form of the claim: after claiming an issue you're about to work, open the PR right away — before implementing — from an empty commit, kept as a draft until the implementation lands.
An open PR is the visible in-flight signal other sessions check, so opening it up front stops parallel duplicates.
The `gi`, `gii`, `gip`, and `st` skills operationalize this.

## Use the existing PR branch, not the harness-specified branch

The Claude Code on the web harness injects a "Git Development Branch Requirements" section that assigns a session-unique branch name (e.g. `claude/abc123`) as the default for each repo.
**That branch is a fallback for brand-new work with no existing PR.**

When a task involves an existing PR or branch, work on that PR's branch instead:

1. Find the branch name: call `mcp__github__pull_request_read` (`method: get`) or (in CLI sessions) `gh pr view <N> --json headRefName -q .headRefName`.
2. Check it out or create a worktree from `origin/<branch>`.
3. Push back to that branch and update the existing PR --- do not open a new one.

Use the harness-specified branch only when starting work with no existing PR and no existing branch to continue.

**Exception --- the session can only push to its own branch.** Some web/remote sessions are scoped so the agent proxy allows pushing *only* to the harness-assigned branch; a push to any other branch (the existing PR's branch included) is rejected with `HTTP 403`.
When that happens you cannot follow step 3.
Don't retry the 403 --- it's a policy denial, not a transient error.

**Prefer stacking the fix, not superseding the PR.** When the work is an incremental fix to an existing, still-open PR (a review finding, a small addition) rather than a full rebuild, push the fix to the assigned branch and open it as a PR **stacked on** the original --- `base` set to the original PR's own branch, per the [`stack-prs`](skills/stack-prs/SKILL.md) skill --- rather than superseding it. Comment on the original PR pointing to the stacked one, and note the dependency ("stacked on this branch — either merge #N into this branch first, or merge this PR and #N will retarget to `main`"). This keeps the diff to just the incremental change instead of re-litigating the whole original PR's content, and it composes correctly regardless of how the maintainer merges it: they can merge the stacked PR straight into the original's branch (folding the fix in before the original PR itself merges) or merge the original first and let the stacked PR retarget to `main` per that skill's step 4.
Reserve the supersede path (below) for when stacking doesn't fit --- the original branch/PR is abandoned, or the fix amounts to a full rebuild rather than an incremental addition.
(Corrected on ai-config#493 → #498, 2026-07-05: first reflex was to supersede per the fallback below; the user redirected to stacking, and the maintainer then merged the stacked PR directly into #493's branch, folding the fix in before #493 itself merged --- exactly the outcome stacking was meant to produce.)

**Supersede fallback, when stacking doesn't apply:** push the fix to the assigned branch, open a **new** PR off `main` that supersedes the original (say "Supersedes #N" in the body and rebuild as a single clean commit so no sensitive history leaks through), comment on the original PR pointing to the replacement, and close the original once the new PR merges.

**Rebuilding the single clean commit: diff against `main`, don't cherry-pick from the write-protected branch.** `main` usually doesn't yet contain the original PR's changes, so cherry-picking just your incremental fix commit conflicts --- it was written against the PR branch's state, not `main`'s.
Instead, diff the whole file set and apply it fresh:
```bash
git diff origin/main <old-branch> -- <changed-files> > /tmp/rebuild.diff
git checkout -B <assigned-branch> origin/main
git apply /tmp/rebuild.diff
git add <changed-files> && git commit -m "..." && git push -u origin <assigned-branch>
```
(Seen on ai-config#372 → #380: the assigned branch could push, `sync-freshness-rule` could not.)

**Check whether the branch's own PR merged before adding more commits to it.** If a PR on this branch merged via **squash** (common in repos that enforce it), the branch's old commits are no longer ancestors of `main`'s new tip — `git merge-base --is-ancestor <old-commit> origin/main` returns false.
Committing follow-up work on top of that stale branch and pushing looks fine locally, but the resulting PR's diff shows the *entire prior PR's changes again* against `main`, confusing reviewers and re-litigating already-merged content.
Before adding commits to a branch you didn't just create, fetch `origin/main` and check ancestry first.
If the branch's own PR already merged, don't build on top of it — start clean: `git checkout -b <branch> origin/main`, then `git cherry-pick` only the genuinely new commit(s).
If you've already pushed a bloated diff, the same fix applies retroactively: rebuild the branch from `origin/main` plus a cherry-pick of the new work, then `git push --force-with-lease`. (Seen on gha#161 → gha#162 and ai-config#344 → ai-config#354, both squash-merged.)

**The harness-assigned branch name itself can already exist locally, pointing at unrelated stale content from an earlier session in the same container.** A fresh container doesn't guarantee a fresh local branch state --- `git checkout -b <harness-branch> origin/<existing-PR-branch>` can fail with "a branch named `<harness-branch>` already exists" if a prior session in this container created one under that same name and left it pointing at old work. Don't assume it's safe to reuse or that it reflects the actual PR: check `git merge-base --is-ancestor <local-tip> origin/main` first --- if the local tip is already an ancestor of `main` (i.e. it was old, already-merged content, not in-flight work), it's safe to discard by force-checking out the real PR branch under that same name with `git checkout -B <harness-branch> origin/<existing-PR-branch>` (uppercase `-B` resets the branch in place instead of erroring). (ai-config#481: the assigned branch name `claude/resolve-pr-481-conflicts-dz9v4w` already existed locally, pointing at a commit that turned out to be an ancestor of `main` from an earlier session --- switched to the actual PR branch instead, per this section's own primary rule.)

## Skills that call gh/glab: fall back to tool-mappings.md in remote sessions

Many skills under `skills/` name concrete `gh`/`glab` CLI commands (e.g. `gh pr comment`, `gh issue create`).
In a remote/web session where `gh`/`glab` isn't on `PATH`, substitute the equivalent GitHub MCP tool from [`tool-mappings.md`](tool-mappings.md) instead of failing or improvising.
That registry is the single source of truth for the gh/glab-to-MCP mapping in this repo --- don't inline a separate translation table into individual skills; point to `tool-mappings.md` and let it stay the one place to update. (GitLab operations have no MCP equivalent listed there; `glab` stays CLI-only.)

## File an issue before starting a new task

<!-- Shared with the lab manual; edit shared/workflow/issue-first.md, not here. -->
@shared/workflow/issue-first.md

The `st` (Start Task) skill operationalizes this; `gi` (Grab Issue) is the path when the issue already exists.

## Tracking issues in upstream repos

<!-- Shared with the lab manual; edit shared/workflow/upstream-issues.md, not here. -->
@shared/workflow/upstream-issues.md

The `sup` / `send-upstream` skill operationalizes steps 1--2 (the PR path, including fork-if-needed, and the issue path) and the link-back.
Step 3 (own-repo fallback) is not covered by `sup`; use `gh issue create` in the current repo and ask the user to transfer it.

## Wrap up a merged PR with UMS

When a PR/MR you were working on **merges**, run the `post-merge` skill: verify the merge actually landed, tidy the local branch (checkout `main`, pull, `git branch -d`), confirm any deferred items have follow-up issues, then run **UMS** to capture what the PR's review lifecycle taught — recurring review findings, corrections, and guidance given along the way.
A merge is the natural checkpoint to bank lessons before the context is lost.

"merge it" / "merge this" / "merge the PR" as bare directives (no slash) trigger the `merge-it` skill: when the PR isn't merged yet, it merges the ready PR (squash by default) **then** chains straight into `post-merge` (tidy + UMS); when the PR is already merged it goes directly to `post-merge`.
Either way the post-merge wrap-up — including the UMS follow-up PR — runs **automatically, without asking**.
If the phrase is clearly part of ordinary prose rather than a standalone directive, treat it as such.

## What "fully clean" means

<!-- Shared with the lab manual; edit shared/workflow/fully-clean.md, not here. -->
@shared/workflow/fully-clean.md

Escalate a deadlock via the `request-pr-review` skill (human reviewer `d-morrison`, or `gh pr edit <N> --add-reviewer d-morrison`), and surface the open item to me.

## Always run ARDI on PRs you touch

<!-- Shared with the lab manual; edit shared/workflow/ardi.md, not here. -->
@shared/workflow/ardi.md

The `ardi` / `iterate` skill family runs this loop. (See *What "fully clean" means* above; the mechanics for each step are in the sections around here.)

## Do the review yourself when the @claude workflow doesn't produce a verdict

When a PR you're managing has its `@claude` review workflow fail to produce a usable verdict — whether because it was **skipped for quota** or because it **ran to completion but never stated a verdict** (a "stub review") — don't stall the ARDI loop waiting for it — **do the review yourself and post it** as a PR comment.
Apply the same review standards the bot would (the SERG lab manual and d-morrison's modular/idiomatic priorities), then keep iterating to fully-clean on your own findings.
Neither failure mode is an approval — an unreviewed PR stays unreviewed regardless of why the bot didn't weigh in.

**Quota-skipped:** surfaces as a bot comment — either `Claude review skipped — API quota exhausted` (the review workflow) or `You've hit your org's monthly spend limit` (the `@claude` agent workflow).
Both mean no bot will respond on this run; re-running the workflow only helps once the quota actually resets.

**Stub review:** the review job reports success (`is_error: false`, real cost/turns logged) but the posted comment never states a `### Verdict` — the run genuinely executed but got cut short before reaching a conclusion (e.g. by escalating permission denials on tool calls it needed). This looks superficially fine (green check, a comment exists) so it's easy to mistake for a real review — read the comment body for an actual verdict section before trusting it. Re-running the same workflow can reproduce the same stub pattern repeatedly rather than self-resolving; if a retry doesn't help within a round or two, treat it as this failure mode and self-review rather than continuing to re-trigger. (Hit repeatedly on gha#193/gha#198, where `claude-review` produced escalating permission-denial-driven stub reviews across many runs before the actual fix — a same-prompt retry composite, gha#201 — landed.)

**Post the self-review before doing anything else — don't stall the PR waiting for the bot. Then, before writing the check off as permanently broken, try one manual re-run of the failed job — even after the workflow's own built-in same-run retry (e.g. gha#185's stub-retry) also stubbed.** Two stubs back to back is a stronger signal than one, but it's still not conclusive: a separately-triggered re-run (`rerun_failed_jobs` via the GitHub Actions API/MCP tool, not just re-reading the same run) is an independent LLM invocation, and the failure modes behind stubs (permission-denial spirals, timing) don't always repeat. If the check is a **required** one, spend the one manual re-run before reporting the workflow as broken for that PR. (`ucdavis/epi204`#361: attempt 1 and its automatic same-run retry both stubbed; self-reviewed and posted a verdict; a manual `rerun_failed_jobs` on that same workflow run then produced a genuine review — and it wasn't a rubber stamp, it caught a real one-sentence-per-line violation the self-review's own added text had introduced.)

Either way: don't wait on the bot indefinitely — do the review yourself and keep driving to fully-clean.

## Watch and ARDI every PR you touch — don't ask first

When you open (or are handed) a PR/MR in **any** repo, subscribe to its activity and run the ARDI loop to clean **automatically** — never ask "should I watch this?" or "should I iterate it?" first.
That answer is a standing yes across all PRs and all repos.
Subscribe with the `subscribe_pr_activity` tool (provided by the GitHub MCP server in remote/web sessions) or babysit locally, drive every review round to fully-clean, and re-arm a periodic check-in since webhooks don't deliver CI-success or merge-conflict transitions.

This webhook-driven loop never formally invokes the `ardi` skill, so read `skills/ardi/SKILL.md` step 6 for the re-request-review mechanics before pushing a fix: after a push, the push itself already triggers the review — don't also post "@claude review again" in the same round.
On workflows with `concurrency: cancel-in-progress`, the two triggers race and cancel each other, leaving the latest commit's review canceled and `require-review` red for no code reason.
Only post the mention when a round pushed no code (all Rebut/Defer). (Hit on ai-config#406: posting the mention right after a push canceled the review and cost three extra polling rounds to recover.)

Surface to me only when an item is ambiguous, architecturally significant, or deadlocked (the escalation rule above still applies), or when the PR is clean.
Stop watching only when the PR merges or closes, or I tell you to back off.

## Address every in-scope review comment, even non-blockers

<!-- Shared with the lab manual; edit shared/workflow/address-every-comment.md, not here. -->
@shared/workflow/address-every-comment.md

If you and the reviewer reach an impasse on a single item (your rebuttal didn't convince them and their re-raise didn't convince you), escalate that item to a **human reviewer** — request `d-morrison` via the `request-pr-review` skill (or `gh pr edit <N> --add-reviewer d-morrison`) and `@`-mention them with the impasse — for the final call rather than looping.

## Keep PR branches synced with main

<!-- Shared with the lab manual; edit shared/workflow/sync-with-main.md, not here. -->
@shared/workflow/sync-with-main.md

(Another instance of **never assume; always verify** — `git fetch` to check main's actual position instead of assuming the branch is current.
The `sync-pr-branch` / `merge-main` skill runs this.)

## Prioritize internal infrastructure work slightly over feature work

<!-- Shared with the lab manual; edit shared/workflow/pr-prioritization.md, not here. -->
@shared/workflow/pr-prioritization.md

A tie-breaker for `ardia`'s PR-ordering step and `gi`'s (and `gii`/`gip`'s) issue-priority table when candidates are otherwise close in priority.
The fragment also sets the default direction for the age factor: among several open PRs, take the **older** one first unless you have more specific instructions.

## Use subagents when helpful

When available, use subagents for helpful sidecar work: independent investigation, verification, or disjoint implementation slices. Keep immediate blocking critical-path edits local so progress does not wait unnecessarily.

## Non-destructive repo and memory actions

The user gives general permission to proceed with non-destructive actions such as setting up PRs, reading GitHub repository data through the API, running non-destructive Git and Perl commands, and editing shared `CLAUDE.md` memory. This includes pushing branches and opening PRs against the ai-config repo. Default to action without confirmation for reasonable non-destructive steps; ask only for destructive, ambiguous high-impact, or genuinely blocking choices. Destructive operations still require explicit instruction.

## Auto-orchestration: always look for Workflow opportunities

The heavy, parallelizable skills (`ardia`, `ardiaei`, `gia`, `gip`, `grade-work`, `opposition-research`, `find-overlap`) decide on their own whether a task warrants multi-agent orchestration via the `Workflow` tool --- so I don't have to type `ultracode` every time.
The `Workflow` tool stays opt-in-gated for bare prompts; an invoked skill is itself the sanctioned opt-in.
Launch a workflow directly when an opt-in signal is already present (`ultracode`, a `+Nk` budget, or "use a workflow"), otherwise propose one with a one-line cost estimate and wait.
The PR/issue-iteration skills stay serial where pushes collide on shared review runners (see the fragment's shared-runner exception).

More generally --- not just inside the named heavy skills --- always look for opportunities to automate work via the `Workflow` tool.
When a task turns out to be workflow-shaped (decomposable, verification-bearing, and at a scale that earns it --- see the fragment's criteria), say so and propose a workflow even if no skill mandated one.
The same opt-in gate still applies: propose with a cost estimate and wait unless an opt-in signal is already present.

<!-- Shared with the lab manual; edit shared/workflow/when-to-orchestrate.md, not here. -->
@shared/workflow/when-to-orchestrate.md

## Check for merge conflicts on every merge in an ultracode session

@shared/workflow/ultracode-merge-conflicts.md

## Coding style: avoid nesting; follow the lab manual

Follow the SERG lab manual (https://ucd-serg.github.io/lab-manual/) for coding and collaboration conventions.

<!-- Shared with the lab manual; edit shared/coding/avoid-nesting.md, not here. -->
@shared/coding/avoid-nesting.md

## Coding: prefer existing packaged functions over rolling your own

<!-- Shared with the lab manual; edit shared/coding/prefer-packaged-functions.md, not here. -->
@shared/coding/prefer-packaged-functions.md

## Coding: prefer per-operation grouping over persistent grouping (dplyr)

<!-- Shared with the lab manual; edit shared/coding/per-operation-grouping.md, not here. -->
@shared/coding/per-operation-grouping.md

## Coding: avoid hard-coding data with an external source of truth

<!-- Shared with the lab manual; edit shared/coding/avoid-hardcoding-external-data.md, not here. -->
@shared/coding/avoid-hardcoding-external-data.md

## Coding: write tidy code; prefer tidyverse over base R/rlang for it

<!-- Not yet shared with the lab manual; edit shared/coding/tidy-code.md, not here. -->
@shared/coding/tidy-code.md

Apply this both when writing code and when reviewing it — flag base R or
`{rlang}` verbosity in review the same way `per-operation-grouping` flags a
persistent `group_by()` that `.by` would replace.

## Coding: reuse function documentation and argument lists

<!-- Not yet shared with the lab manual; edit shared/coding/reuse-docs-and-args.md, not here. -->
@shared/coding/reuse-docs-and-args.md

## Writing style: plain, direct prose

<!-- Shared with the lab manual; edit shared/writing/plain-prose.md, not here. -->
@shared/writing/plain-prose.md

The `use-preferred-style` skill (alias `style`) spells out the procedure, the PSW chapter links, and a filler/jargon swap table; the `find-ai-tells` skill (alias `ai-tells`) is the scan-after detector counterpart.

## Writing style: semantic line breaks in prose

<!-- Shared with the lab manual; edit shared/writing/semantic-line-breaks.md, not here. -->
@shared/writing/semantic-line-breaks.md

## Quarto: link packages on first mention

**Link packages up front.** Package names in `.qmd` prose take the
`[{pkg}](url)` link form on first mention in a section (e.g.
`[{dplyr}](https://dplyr.tidyverse.org/)`). Add those links as you write the
section — the review bots flag every unlinked package name, one round at a time.

## Quarto: div syntax for figure/table labels and captions

In Quarto `.qmd` files, label and caption figures and tables with **div syntax**, not chunk-option syntax.
Wrap the code chunk in a `::: {#fig-...}` / `::: {#tbl-...}` fenced div and put the caption as the last line before the closing `:::`:

```
::: {#fig-stage-at-dx}

```{r}
#| label: stage-at-dx-fig
#| code-fold: true

plot_stage_at_dx(pt_data)
```

Stage at diagnosis by screening frequency
:::
```

Don't use the chunk options `#| label: fig-...` / `#| fig-cap: "..."` for the cross-reference id and caption.
The div id (`#fig-`/`#tbl-`) carries the cross-reference; the chunk `label` stays a plain code label.
This keeps figures consistent with tables, which already use div syntax.

## Challenge ambiguous phrasing and terminology in review

<!-- Shared with the lab manual; edit shared/workflow/challenge-ambiguous-terminology.md, not here. -->
@shared/workflow/challenge-ambiguous-terminology.md

The `ard`/`ardi` skill family and `use-preferred-style`/`find-ai-tells` operationalize this in their respective review contexts.

## Challenge redundant content in review

<!-- Shared with the lab manual; edit shared/workflow/challenge-redundant-content.md, not here. -->
@shared/workflow/challenge-redundant-content.md

The `ard`/`ardi` skill family and `code-review` apply this in PR/MR review; `find-overlap` (and its `consolidate-skills`/`consolidate-memory` actors) is the corpus-wide counterpart when redundancy spans more than the current diff.

## Writing style: scan for AI tells

The detector counterpart to the plain-prose guide above.

<!-- Shared with the lab manual; edit shared/writing/ai-tells.md, not here. -->
@shared/writing/ai-tells.md

The `find-ai-tells` skill (alias `ai-tells`) runs this same catalog on demand against any target text.

## Writing style: cite sources thoroughly

<!-- Shared with the lab manual; edit shared/writing/citations.md, not here. -->
@shared/writing/citations.md

## Fact-check prose and internal reasoning in review

<!-- Shared with the lab manual; edit shared/writing/fact-check-prose.md, not here. -->
@shared/writing/fact-check-prose.md

When running `code-review` or the `ard`/`ardi` loop on a diff that touches prose, apply this policy in addition to the normal review — those skills don't name it internally, but this CLAUDE.md directive governs regardless.

## Hyperlink technical terms and results; no forward references

@shared/writing/definition-crossrefs.md

Applies wherever `code-review`/`ard`/`ardi` already reviews a prose diff, alongside the fact-check and ambiguous-terminology checks above.

## Fact-check code logic and math in review

<!-- Not yet shared with the lab manual; edit shared/coding/fact-check-code-logic.md, not here. -->
@shared/coding/fact-check-code-logic.md

The code counterpart to the prose fact-check above --- catches strategic
mistakes (wrong algorithm or approach), tactical mistakes (wrong
implementation of a right approach), and math/statistics errors (wrong
formula or method, verified against a source), not just prose claims and
derivations.

## Challenge unnecessary complexity in review

<!-- Shared with the lab manual; edit shared/workflow/challenge-unnecessary-complexity.md, not here. -->
@shared/workflow/challenge-unnecessary-complexity.md

When running `code-review`, `ard`/`ardi`, or any prose review (`use-preferred-style`, `find-ai-tells`, `fact-check-prose`), apply this alongside the normal review — those skills don't name it internally, so this CLAUDE.md directive governs regardless. It's distinct from `simplify` (a dead-code-after-refactor sweep) and `tidy` (a separate on-demand audit).

## Useful prompt formats for coding agents

<!-- Vendored from UCD-SERG/lab-manual; edit there, not here. See README, "Shared content". -->
@shared/vendored/prompt-formats.md

## Review with Copilot before requesting human review

This is shared lab guidance on getting an automated review before asking a human reviewer.
When *I* iterate a PR, the ARDI loop above is the mechanism — it already addresses whatever the `@claude` or Copilot reviewer flags — so read this as the lab-member-facing statement of the same principle, not a second loop to run.

<!-- Vendored from UCD-SERG/lab-manual; edit there, not here. See README, "Shared content". -->
@shared/vendored/copilot-review-before-human.md

## Growth mindset: seek resources rather than accept limitations

<!-- Edit shared/workflow/growth-mindset.md, not here. -->
@shared/workflow/growth-mindset.md

## Encoding reusable feedback into ai-config

When the user gives feedback, corrections, or guidance that applies beyond the current session (a standing rule, style preference, workflow change, or behavioral note), decide on your own how to encode it --- don't ask.
Choose the right form (memory bullet in CLAUDE.md, update to a shared fragment in `shared/`, new or revised skill, etc.) and commit the change.
Only surface the choice if it's ambiguous or touches something architecturally significant.
