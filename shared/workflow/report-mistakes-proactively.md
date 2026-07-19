If you see something, say something.
When you notice a mistake — in code, prose, configuration, data, CI, or any
other medium — file a tracking issue for it immediately, even when it is out
of scope for your current task.
An observation that lives only in the conversation is lost when the session
ends; the issue is what makes it durable.

## The procedure

1. **Say something in chat.** Surface the mistake as a one-line `⚠️ FLAG`
   (per `CLAUDE.md`'s chat-output-tagging convention) so the user sees it
   now — but don't stop there; chat is not durable.
2. **Dupe-check the tracker.** Search the target repo's issues first (the
   same search step [`issue-first`](issue-first.md) runs); when an open
   issue already covers the mistake, comment there with the new evidence
   instead of filing a duplicate.
3. **File the issue immediately** — in the same work stride as noticing it,
   not batched for a wrap-up step, mirroring `CLAUDE.md`'s "run UMS
   proactively" timing rule.
   Write it to stand alone: what is wrong, where (file/line or URL), why
   it's wrong, and — for a bug — a reprex where feasible, per
   [`issue-first`](issue-first.md).
4. **Link it back.** Name the filed issue in the chat flag, and in a PR
   comment when the mistake surfaced while working a PR, so the record is
   discoverable from both sides.

## Where to file

- **The repo where the mistake lives, when it's one we administrate** (our
  own repos and orgs — the same set [`dont-reinvent-wheel`](../principles/dont-reinvent-wheel.md)
  lists as "our own repos", plus this corpus and `gha`).
- **Never autonomously in an external repo.** When the mistake belongs to
  an upstream or third-party repo, follow
  [`upstream-issues`](upstream-issues.md): draft the report, file it in one
  of our own repos via that fragment's own-repo fallback, and ask the user
  to transfer or escalate it.
  External repos' contribution policies bind us, and some ban autonomous AI
  submissions outright.
- **When the session can't reach the home repo** (not in the session's
  GitHub scope, no network path), file in the current working repo, state
  plainly which repo it really belongs to, and ask the user to transfer it
  — the same fallback the `config-ai` skill's step 3 uses.

## Scope discipline

Filing the issue is the deliverable — don't derail the current task into
fixing the mistake.
The exception is a trivial fix in a file the current work already touches
(a typo on a line you're editing anyway): fold that in rather than filing.
Severity doesn't gate the rule: a nit gets tracked too — severity affects
the issue's priority, not whether it's recorded.

## Relationship to existing rules

- [`issue-first`](issue-first.md) governs work you're about to **start**;
  this rule governs mistakes you merely **notice**, whether or not anyone
  will work them soon.
- [`upstream-issues`](upstream-issues.md) supplies the where-to-file ladder
  this rule's external-repo case defers to.
- The [`defer-issue`](../../skills/defer-issue/SKILL.md) skill fires only
  on the **user's** explicit deferral ("let's handle this later"); this
  rule is self-initiated — no prompt needed.
- [`ardi`](ardi.md)'s Defer step already tracks out-of-scope **review
  findings**; this rule generalizes the same habit to any mistake noticed
  in any task.
