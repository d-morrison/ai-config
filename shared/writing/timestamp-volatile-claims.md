When you state a factual claim about a **condition that can change over
time**, attach the time the claim was true --- "as of 2026-07-24", "as of
this writing", "(checked 2026-07)". This applies everywhere a reader may
revisit the text later: chat replies, PR/issue/commit prose, docs, READMEs,
code comments, and memory files.

A timestamp makes staleness self-evident. A later reader --- including future
you --- can see the claim's vintage and know to re-verify it, instead of
trusting a bare present-tense assertion that has silently gone stale. An
undated volatile claim reads as a standing, timeless fact, so it gets
repackaged into fresh present-tense assertions without anyone re-checking the
underlying condition.

## What counts as volatile

A claim is volatile if updating the world could falsify the sentence without
touching the sentence itself:

- Release / availability status --- "package X is on CRAN", "feature Y is
  supported", "the API doesn't expose Z".
- "Current", "latest", "now", "recently", "still" claims --- a version number,
  a default, a "the newest model is ...".
- Counts, prices, dates, and roster facts --- "there are N consumers", "it
  costs $M", "A maintains it", "the pin is K commits behind".
- Anything you verified by looking it up just now --- if you had to check it,
  its answer can change, so record when you checked.

Prefer an **absolute** date over a relative word: "as of July 2026", not
"currently" / "now" / "recently" --- the same reason the memory rule converts
relative dates to absolute ones. A relative word is itself a claim that goes
stale the moment the text is read later.

## What does not need a timestamp

Timeless facts whose truth value can't flip --- a mathematical identity, a
definition, a language's fixed semantics ("R uses 1-based indexing"), a
historical event's date. Don't clutter these with an "as of"; the target is
specifically claims that a future change could falsify.

## The failure mode it prevents

Repo docs stated "snapr is not on CRAN or P3M." That was true when written,
but undated, so it read as a standing fact --- and it was restated as a fresh
present-tense assertion ("snapr isn't on CRAN at all") without re-checking,
even though snapr had since been published to CRAN (0.1.0, 2026-05-22). A
timestamp on the original --- "not on CRAN as of <date>" --- would have marked
it as a fact with a vintage, worth re-verifying before repeating.

## Relationship to other rules

- [`fact-check-prose.md`](fact-check-prose.md) checks that a claim is *true*
  now. This rule is complementary: even a true claim needs a timestamp when
  its truth is time-dependent, so it stays checkable later instead of
  decaying into a confident falsehood.
- The `check-info-quality` skill is the **detector** that finds
  already-stale claims after the fact; this rule prevents them at authoring
  time by making each volatile claim's vintage explicit.
- `CLAUDE.md`'s "Timestamp recaps in local time" and the
  convert-relative-dates-to-absolute memory rule timestamp *when you acted or
  spoke*; this rule timestamps *when a volatile fact was true* --- a different
  quantity that happens to share the "prefer absolute dates" mechanics.

## In review

An undated volatile claim is a review finding, the same weight as an uncited
one: ask for a timestamp, or a rephrase to something timeless. Apply it to
your **own** PR descriptions, comments, and commit messages too, not just
when reviewing someone else's prose.
