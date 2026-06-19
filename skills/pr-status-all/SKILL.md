---
name: pr-status-all
description: Print a table summarizing the true status of every open PR in the repo — for each one, read the LATEST review comment (not a cached verdict) and parse it for remaining findings, alongside CI state and whether the branch is behind main. Use when asked "summarize all open PRs", "status table of my PRs", "what's the state of every PR", "give me a PR dashboard", or any whole-queue status overview. For a single PR use `pr-status`; to actually drive PRs to clean use `iterate-all`.
user-invocable: true
allowed-tools:
  - Bash
---

# pr-status-all

Produce a **one-row-per-PR status table** for all open PRs. This is the
whole-queue version of [`pr-status`](../pr-status/SKILL.md): apply the same
"read the **latest** review and parse it for findings" discipline to every
open PR, then lay the results out as a table. It is **read-only** — it reports
status, it does not push, merge, or run review loops (use
[`iterate-all`](../iterate-all/SKILL.md) for that, or
[`sync-pr-branch`](../sync-pr-branch/SKILL.md) to update a branch).

## When this fires

- "summarize all open PRs", "status table / dashboard of my PRs",
  "what's the state of every open PR", "which PRs are ready to merge".
- Whenever you'd otherwise report on more than one PR at once.

## CI green ≠ review clean

`gh pr checks <N>` going green is about **CI state**, not the review verdict. A
PR can have every check passing and still carry unaddressed review findings.
Report CI state and review verdict as **separate columns** — never collapse
them into one "OK".

## Procedure

1. **List the open PRs:**

   ```bash
   gh pr list --state open --json number,title,headRefName,isDraft \
     --jq '.[] | "\(.number)\t\(.headRefName)\t\(.isDraft)\t\(.title)"'
   ```

2. **For each PR, gather four independent signals:**

   - **Latest review verdict** — read the *most recent* review comment and
     parse it for findings (see next section). Do **not** trust an earlier
     cached verdict; a newer review may have landed.
   - **CI state** — `gh pr checks <N>` (note any failing/pending checks by
     name; don't just say "red").
   - **Unresolved threads** — count open inline review threads via the GraphQL
     snippet in [`pr-status`](../pr-status/SKILL.md) (*Check thread-resolution
     state*; the resolve mutation lives in `ard` step 4b). >0 means the PR
     isn't fully clean even if the review body reads "approved."
   - **Behind main?** — `git fetch origin main -q && git rev-list --count
     <headRefName>..origin/main` (or compare via the API). >0 means main has
     moved ahead and the branch should be synced.

3. **Render the table** (see Output).

## Read the LATEST review (the subtle part)

```bash
gh pr view <N> --json comments \
  --jq '[.comments[] | select(.author.login | startswith("claude"))] | last | .body'
```

The reviewer bot login **varies by API/setup**: `gh pr view` reports `claude`;
the REST API reports `claude[bot]`; some setups post as `github-actions[bot]`.
`startswith("claude")` covers the common cases — if a PR's reviewer posts under
a different login the `--jq` returns `null`, which you must **not** silently
report as "clean": broaden the filter or flag that no review was found.

Scan the latest body for any "Findings", "Issues", "Remaining",
"Non-blocking", "Minor", "Could improve", "Consider", etc. section. The bar for
**clean**: "Looks good" / "no findings" / "approved" with **zero** follow-on
bullets under any heading. Anything else is **open** — count the items. A
posted rebuttal the reviewer is still disputing is **open**, not clean: a
rebuttal only counts once it convinced the reviewer (they dropped the item).

## Output

A Markdown table, one row per open PR, with these columns:

| PR | Title | Branch | CI | Review | Threads | Behind main |

- **PR** — make the number a bare clickable URL
  (`https://github.com/<owner>/<repo>/pull/<N>`), not plain text, so it's
  one-click in the terminal.
- **CI** — ✅ / ❌ (name the failing check) / ⏳ pending.
- **Review** — `clean`, `N open` (with the headline finding), `none found`
  (filter didn't match / no review yet), or `in-flight` if a review run is
  still going.
- **Threads** — `resolved` (none open) or `N open` (unresolved inline review
  threads).
- **Behind main** — `up to date` or `N commits` (offer `sync-pr-branch`).

Below the table, list each PR's open findings briefly (or "none"), and call out
anything needing action: branches behind main, failing CI, drafts, or reviews
that returned `null`. Do **not** label a PR "ready to merge" unless it is
**fully clean** — its review is genuinely clean *and* all CI workflows are
green *and* it's not behind main *and* every inline review thread is resolved
(the only open conversation being the final all-clear and your reply). Never
hedge with "ready except for one nit."

## Notes

- Skip draft PRs from the "ready" assessment but still show them (mark as
  draft).
- If there are many PRs, gather the per-PR signals in parallel where possible
  to keep it fast.
