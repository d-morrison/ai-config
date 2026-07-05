# /pr-on-claim — Open a draft PR immediately after claiming an issue

Operationalizes the strong form of the claim workflow: branch → empty commit → draft PR, before writing any code. An open PR is the strongest "in-flight" signal that work is happening on an issue.

## Usage

```
/pr-on-claim <issue#> [title-override]
```

**Arguments:**
- `<issue#>` (required): GitHub issue number to claim and open a PR for
- `[title-override]` (optional): Override the PR title (defaults to issue title)

## What it does

1. Fetch `origin/main` and check out a clean branch: `feat/<slug>` or `fix/<slug>` (inferred from issue title)
2. Create an empty commit with message: `"start: <issue title> (closes #<N>)"`
3. Push the branch with `-u origin`
4. Open a **draft PR** with:
   - Title: issue title (or override)
   - Body: `"Closes #<N>\n\nWIP — opened up front to claim the issue; implementing now."`
5. Post a claim comment on the issue: `"Working on this — paws off until I'm done."`

## Why draft?

A draft PR doesn't trigger `@claude` review bot, so no review round is spent on an empty or half-finished diff. When implementation is complete and checks pass, mark ready-for-review (`gh pr ready <N>`).

## Order

1. Claim the issue (this skill)
2. Implement code on the branch
3. Mark PR ready-for-review
4. Iterate ARDI until clean
5. Merge

## Related

- `@shared/workflow/pr-on-claim.md` — policy documentation
- `@shared/workflow/claim-pr.md` — claim-only (no PR)
- `/ardi` — review iteration loop
- `/gi` — grab issue (includes PR-on-claim)
- `/st` — start task (includes PR-on-claim)
