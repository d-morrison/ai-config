# pr-status-all

Produce a **one-row-per-PR status table** for all open PRs. This is the whole-queue version of [`pr-status`](../../skills/pr-status/SKILL.llms.md): apply the same “read the **latest** review and parse it for findings” discipline to every open PR, then lay the results out as a table. It is **read-only** — it reports status, it does not push, merge, or run review loops (use [`ardia`](../../skills/ardia/SKILL.llms.md) for that, or [`sync-pr-branch`](../../skills/sync-pr-branch/SKILL.llms.md) to update a branch).

Because the per-PR signals are independent and read-only, gather them **concurrently** — one subagent per PR — then assemble the table. See *Why fan-out is safe here* for why this loop parallelizes and the write-loops don’t.

## When this fires

- “summarize all open PRs”, “status table / dashboard of my PRs”, “what’s the state of every open PR”, “which PRs are ready to merge”.
- Whenever you’d otherwise report on more than one PR at once.

## CI green ≠ review clean

`gh pr checks <N>` going green is about **CI state**, not the review verdict. A PR can have every check passing and still carry unaddressed review findings. Report CI state and review verdict as **separate columns** — never collapse them into one “OK”.

## Procedure

### 1. Enumerate the open PRs (orchestrator, one cheap call)

``` bash
gh pr list --state open --json number,title,headRefName,isDraft \
  --jq '.[] | "\(.number)\t\(.headRefName)\t\(.isDraft)\t\(.title)"'   # LIST_PRS
```

This is fast and sequential — a single call to get the work units.

### 2. Fan out — one subagent per PR (concurrent)

Spawn **one subagent per open PR, all in a single batch** (multiple `Agent` calls in one message) so they run at once. The fan-out is read-only, so it needs **no worktrees** — each subagent only reads PR signals, nothing mutates, and there is nothing to collide on.

Give each subagent its PR number and `headRefName`, and have it gather the **six independent signals** below and return one structured row. Carry the disciplines into the prompt — a subagent that doesn’t follow *Read the LATEST review* will silently misreport:

A subagent starts **fresh** — it sees only this prompt, not this skill file — so **inline the exact commands**; don’t point it at a section it can’t read. Fill in `<N>`, `<headRefName>`, `<owner>`, `<repo>` for each PR (resolve owner/repo once with `gh repo view --json owner,name --jq '"\(.owner.login)/\(.name)"'`):

> Gather the status of PR **\#** (branch `<headRefName>`) in this repo and return a single structured row. Do not push, merge, or modify anything.
>
> 1.  **Latest review verdict, checked for currency against the head.** Read the *most recent* review comment **and** the timestamp of the latest commit, in one call, so a “clean” verdict posted before the last push can’t be mistaken for current:
>
>     ``` bash
>     gh pr view "<N>" --json comments,commits,headRefOid \
>       --jq '{review: ([.comments[] | select(.author.login | startswith("claude"))] | last), lastCommitDate: (.commits[-1].committedDate), headRefOid: .headRefOid}'
>     ```
>
>     **This fetches more than `READ_PR_COMMENTS` maps to** – [`tool-mappings.md`](../../tool-mappings.md)’s entry for that token is a comments-only MCP call, which returns neither `commits` nor `headRefOid`. In a remote/MCP session without `gh`, fetch those two fields with a separate call rather than assuming the token mapping covers this expanded query. The reviewer login varies by setup: `gh pr view` reports `claude`; the REST API reports `claude[bot]`. `startswith("claude")` matches both. If `.review` is `null`, the reviewer may post as `github-actions[bot]` or another login – **never report “clean”**; broaden the filter or say no review was found. **If `.review.createdAt` is earlier than `.lastCommitDate`, the review predates the latest push** – report `in-flight`, not the review body’s verdict, regardless of what it says (both are ISO 8601 UTC timestamps, so a plain string comparison works). **This timing comparison is best-effort, not proof** – a review run *started* against an older commit can finish and post *after* a newer push lands, making `createdAt` look current even though the reviewed content is stale (issue comments carry no structured `commit_id` to check directly, unlike formal reviews). When the review body names the commit it reviewed (the `@claude` bot commonly writes “commit `<sha>`”), cross-check that mentioned SHA’s prefix against `.headRefOid` (now part of the same call above) as a corroborating signal; treat a mismatch as `in-flight` even if the timing check alone would have said `clean`. **When no SHA can be extracted from the body, don’t fall back to trusting the timing check alone as proof of currency** – report `unverified` (not `clean`) instead, since `committedDate` is the commit’s local committer timestamp, not when GitHub received the push, and a commit authored earlier but pushed later can pass the timing check while still being newer than the review. Only once the review postdates the last commit **and** a named SHA matches – unconditionally; no SHA named means `unverified`, not `clean`, full stop – apply the bar for `clean`: “Looks good” / “no findings” / “approved” with zero follow-on bullets under any heading. A rebuttal the reviewer still disputes is **open**, not clean.
>
> 2.  **External (Copilot) reviewer verdict – read-only, don’t request one.** The comment above is the `@claude` bot only; a formal Copilot review is a separate object it won’t show. This step **only inspects an existing Copilot review** – it never POSTs a review request. Requesting a review is a mutation (triggers a review job, consumes quota, can collide with a concurrent `ardi` loop), which breaks this skill’s whole justification for fanning out subagents concurrently (*read-only, side-effect-free*). If no genuine verdict already exists at the current head, report that fact – don’t try to produce one; that’s `ardi`’s job.
>
>     ``` bash
>     set -o pipefail
>     head="$(gh pr view "<N>" --json headRefOid -q .headRefOid)"
>     review_id="$(gh api "repos/<owner>/<repo>/pulls/<N>/reviews" --paginate \
>       | jq -s --arg h "$head" \
>       '[.[][] | select(.user.login=="copilot-pull-request-reviewer[bot]" and .commit_id==$h)] | last | .id')"
>     if [ -n "$review_id" ] && [ "$review_id" != "null" ]; then
>       gh api "repos/<owner>/<repo>/pulls/<N>/reviews/$review_id" --jq '{state, body}'
>       gh api "repos/<owner>/<repo>/pulls/<N>/comments" --paginate \
>         | jq -s --arg rid "$review_id" \
>         '[.[][] | select(.pull_request_review_id == ($rid | tonumber))] | .[] | {line: (.line // .original_line), body}'
>     else
>       echo "no Copilot review exists at the current head"
>     fi
>     ```
>
>     Clean requires **three** things: an affirmative zero-new-findings overview (e.g. “generated no new comments” – never a literally empty body), zero matched inline comments, **and no “Comments suppressed due to low confidence” block in the body** – a “no new comments” overview can still carry real low-confidence findings collapsed into a `<details>` block that never becomes a formal inline comment (verified: PR \#660’s review 4767752501 read “generated no new comments” while carrying 3 suppressed findings). A stub-like non-answer (“ineligible”, “reached their quota limit”) is not a verdict either. **This step cannot determine *why* no Copilot verdict exists** – it can’t tell “Copilot was never asked” from “Copilot is unreachable” from “a self-review was posted instead.” Don’t guess; report the plain evidence-based fact (`no verdict at head`), and leave the availability/self-review judgment call to `ardi`, which actually drives the PR and can request reviews.
>
> 3.  **CI state** – `gh pr checks <N>` (`PR_CHECKS`); name any failing/pending check, don’t just say “red”.
>
> 4.  **Unresolved threads** – count open inline review threads (`READ_PR_REVIEW_COMMENTS`). Run exactly:
>
>     ``` bash
>     gh api graphql -f query='query {
>       repository(owner:"<owner>", name:"<repo>") {
>         pullRequest(number:<N>) {
>           reviewThreads(first:100) {
>             totalCount
>             nodes { isResolved }
>           }
>         }
>       }
>     }' --jq '.data.repository.pullRequest.reviewThreads as $rt |
>       ($rt.nodes | map(select(.isResolved | not)) | length) as $open |
>       if $rt.totalCount > ($rt.nodes | length)
>       then "\($open)+ open (cap)"
>       else if $open == 0 then "resolved" else "\($open) open" end
>       end'
>     ```
>
>     The command emits one of three normalized values: `resolved` (all threads resolved), `N open` (e.g. `3 open`) — that many unresolved threads, or `N+ open (cap)` — the 100-thread cap was hit, **cannot confirm clean** — treat as unresolved.
>
> 5.  **Behind main?** – fetch the head ref too (a fresh subagent has no local branch), then compare remote-tracking refs: `git fetch origin main <headRefName> -q && git rev-list --count origin/<headRefName>..origin/main`. \>0 means main has moved ahead.
>
> 6.  **Blocking human `CHANGES_REQUESTED`** (`READ_PR_REVIEWS` – abstract operation token; resolve to your model’s tool via [`tool-mappings.md`](../../tool-mappings.md)). A bot’s clean verdict does **not** clear a human’s formal review state – it’s a separate object, invisible to the Signal 1 comments query, and its top-level body is often empty (the finding lives in an inline comment):
>
>     ``` bash
>     gh pr view "<N>" --json reviews \
>       --jq '[.reviews[] | select(.author.login != null and (.state == "APPROVED" or .state == "CHANGES_REQUESTED" or .state == "DISMISSED"))] | group_by(.author.login) | map(sort_by(.submittedAt) | last) | [.[] | select(.state == "CHANGES_REQUESTED") | .author.login]'
>     ```
>
>     **`--json reviews` returns the full review history, not one entry per reviewer, and a reviewer’s *decisive* state persists across neutral comments** – GitHub only clears `CHANGES_REQUESTED` when that same reviewer later `APPROVED`s, or via an explicit dismissal; a neutral `COMMENTED` review in between does **not** clear it. Filter to only `APPROVED`/`CHANGES_REQUESTED`/`DISMISSED` states *before* reducing to each author’s latest review – reducing over all states first lets a later `COMMENTED` round hide an earlier `CHANGES_REQUESTED` (verified with a synthetic fixture: naive reduction incorrectly cleared it, state-filtered reduction correctly kept it blocking). **Keep `DISMISSED` in the filter** – dropping it would let an older `CHANGES_REQUESTED` outlive its own later dismissal, since the dismissal itself would never survive the reduction to compete as “latest” (verified with a second synthetic fixture: `CHANGES_REQUESTED` then `DISMISSED` incorrectly stayed blocking under an `APPROVED`/`CHANGES_REQUESTED`-only filter, correctly cleared once `DISMISSED` was included). The trailing `select(.state == "CHANGES_REQUESTED")` still keeps `DISMISSED` reviews themselves out of the final blocking list. Any non-empty result **blocks** regardless of what any bot says – only the human (or an explicit dismissal) resolves it. Return the reviewer login(s) from the array, not just a count.
>
> Return: PR number, CI (✅/❌-with-name/⏳), review (`clean` / `unverified` / `N open` with the headline finding / `none found` / `in-flight`), external (`clean` / `N open` / `no verdict at head`), human-blocked (`none` / `N pending` – name the reviewer if `N` \> 0), threads (`resolved` / `N open` / `N+ open (cap)`), behind-main (`up to date` / `N commits`).

### 3. Assemble (orchestrator)

Collect the rows the subagents return and **pair each with the `title`, `headRefName`, and `isDraft`** the orchestrator already has from step 1 (the subagent doesn’t re-fetch these), then render the table + per-PR findings list (see *Output*) — marking draft PRs from `isDraft`. The output is **identical** to the series version — only the way the signals are gathered changed.

### Graceful degradation to series

If subagent fan-out is unavailable (no `Agent` tool in the session), fall back to gathering the six signals **in series** – loop the exact same per-PR gather (items 1-6 above, including the currency check and the human `CHANGES_REQUESTED` check) over each PR from step 1. The output is the same; it’s just slower. Don’t substitute a simplified comments-only query here – that would silently drop the current-head and human-review guarantees the rest of this skill relies on.

## Output

A Markdown table, one row per open PR, with these columns:

PR \| Title \| Branch \| CI \| Review \| External \| Human \| Threads \| Behind main \|

- **PR** — make the number a markdown link, `[#<N>](https://github.com/<owner>/<repo>/pull/<N>)` (repo policy — never a bare `#N`), so it’s one-click and compact.
- **CI** — ✅ / ❌ (name the failing check) / ⏳ pending.
- **Review** – `clean`, `unverified` (postdates the last commit by timing alone but no SHA could corroborate it), `N open` (with the headline finding), `none found` (filter didn’t match / no review yet), or `in-flight` if a review run is still going **or** the latest review predates the latest commit (per subagent item 1’s currency check) – either way, the current head hasn’t been confirmed reviewed yet.
- **External** – `clean` (a genuine, non-stub Copilot verdict at the current head, per subagent item 2), `N open` (findings in that verdict), or `no verdict at head` (no Copilot review exists yet at the current commit). This step is read-only and doesn’t request a review, so it can’t tell “Copilot was never asked” from “unreachable” from “a self-review covers it” – report the plain fact, don’t guess at the reason.
- **Human** – `none` (no blocking human review) or `N pending` (name the reviewer login(s)) per subagent item 6. This overrides everything else – a `CHANGES_REQUESTED` review blocks regardless of any bot’s verdict.
- **Threads** — `resolved` (none open), `N open` (unresolved inline review threads), or `N+ open (cap)` (100-thread cap hit — cannot confirm clean).
- **Behind main** — `up to date` or `N commits` (offer `sync-pr-branch`).

Below the table, list each PR’s open findings briefly (or “none”), and call out anything needing action: branches behind main, failing CI, drafts, reviews that returned `null`, or a pending human review. Do **not** label a PR “ready to merge” unless it is **fully clean** – **Human is `none`** (a blocking human review overrides everything below) *and* at least one of Review or External is `clean` at the current head (the canonical rule needs one genuine external verdict, not both – a clean Claude verdict alone is sufficient, and so is a clean Copilot verdict alone; `unverified` does **not** count as clean) *and* neither one has open findings *and* all CI workflows are green *and* it’s not behind main *and* every inline review thread is resolved (the only open conversation being the final all-clear and your reply). If both Review and External come back `none found` / `no verdict at head` / `unverified`, this skill has no evidence of a genuine external verdict at all – report the PR as not confirmed clean and point at `ardi` to obtain one; don’t guess whether a self-review already covers it. Never hedge with “ready except for one nit.”

## Why fan-out is safe here (and the write-loops stay series)

This loop parallelizes because its units are **independent and side-effect-free** — each PR’s signals are read-only and don’t depend on any other PR. The whole-queue *write* loops are different, and deliberately stay (mostly) series:

- **`ardia` / `iterate-all`** — share one working directory, compete for CI runner capacity, and have human checkpoints. Parallelize only opt-in, with worktree isolation + bounded concurrency — not by default.
- **`gii` / `gia`** — intentionally sequential: a later issue’s base branch depends on whether the prior MR merged, and same-file issues conflict. **`gip`** is the opt-in exception — it fans out only the *provably independent* subset (no stacking dependency, no file overlap), each subagent in its own worktree, and sends everything else back through `gii`.

Rule of thumb: fan out a whole-queue loop only when its units are provably independent and don’t mutate shared state — like this one.

## Notes

- Skip draft PRs from the “ready” assessment but still show them (mark as draft).
- One unit of work per PR: in the parallel path that’s one subagent per PR; in the series fallback it’s one gather per PR. Either way, the *output* table and findings list are identical.

## Relationship to other skills

- **`pr-status`** — the single-PR version; this applies its latest-review-only / `null`-not-clean discipline across the whole open-PR queue. (pr-status : pr-status-all :: `ardi` : `ardia`.)
- **`ardia` / `iterate-all`** — the *write* counterpart: actually drive every open PR to clean. This skill only reports; see *Why fan-out is safe here* for why those loops stay series.
- **`sync-pr-branch`** — offered for any PR the table flags as behind main.

Back to top
