Don't reinvent the wheel (DRW).
Before implementing a new function or feature, check that it hasn't
already been done — either in one of our own repos, or in a trustworthy
external source we could depend on instead.
Prefer reusing, depending on, forking, or contributing to an existing
implementation over building a new one from scratch.

This is both a development principle (run the check before writing) and
a review principle (flag hand-rolled equivalents in a diff — see "In
review" below).

## Where to look

- **Our own repos**: the lab packages (e.g. `{bcs}`, `{ettbc}`), the
  shared reusable workflows and actions in `d-morrison/gha`, and this
  `ai-config` corpus's skills and fragments.
  Packages can depend on each other, so reuse across our repos is fine.
- **Trustworthy external sources**: base R; the
  [r-lib](https://github.com/r-lib) and
  [tidyverse](https://github.com/tidyverse) organizations; a focused,
  well-maintained CRAN package; [rOpenSci](https://github.com/ropensci);
  CRAN Task Views for topic surveys; and the analogous ecosystems
  elsewhere (PyPI, npm, the GitHub Actions marketplace).

The [`prefer-upstream`](../../skills/prefer-upstream/SKILL.md) skill is
the search procedure (where to look per ecosystem, and the
build-vs-use decision criteria);
[`prefer-packaged-functions`](../coding/prefer-packaged-functions.md)
is the R-function special case of this principle.

## Prefer forking or contributing over re-building

When an existing external source is close but not exact — it does most
of the job but is missing the piece we need — prefer extending it over
re-building the functionality from scratch:

- **Contribute upstream** when the missing piece is general-purpose:
  a PR adding it, or an issue with a reprex, per
  [`upstream-issues`](../workflow/upstream-issues.md) — read the
  upstream repo's contribution policy first, and never post to an
  external repo autonomously.
- **Fork** when we need the change now, or the change is too
  lab-specific for upstream to want.
  Still offer the general parts upstream where they fit, so the fork
  can eventually retire instead of becoming a permanently diverged
  maintenance burden.
- **Borrowing code** (copying rather than depending) goes through the
  [`scout-peers`](../../skills/scout-peers/SKILL.md) license gate:
  verify the license first, record attribution in `CREDITS.md`.

Re-building from scratch is the last resort, for when nothing close
enough exists or every existing option is unfit.

## When rolling our own is right

This is a default, not an absolute rule.
Build custom when the problem is genuinely project-specific, the
existing option is unmaintained or license-incompatible, its API is
wrong for the need, or the dependency is far heavier than the job
(a heavy package for a one-liner).
When you do build custom, note in the PR (or a code comment) that you
checked and nothing fit, so the next reader doesn't re-run the search
— and so the reviewer's DRW check below has its answer up front.

## In review

For each new function or feature a diff adds, ask whether that
functionality already exists in our own repos or a trustworthy
dependency.
A hand-rolled equivalent of something a maintained package (or our own
code) already provides is a review finding, the same weight as any
other standing review check: name the existing implementation, and
propose depending on, forking, or contributing to it instead.
Accept the custom version when one of the escape hatches above
genuinely applies — and ask for the "checked, nothing fit" note when
it's missing.
