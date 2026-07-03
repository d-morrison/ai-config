When reviewing code that implements an algorithm, computation, math, or
statistics, check whether it's *right* --- not just styled well. Use domain
knowledge and, where checkable, an external source (the referenced paper, a
package's own docs, a spec) --- the same evidentiary bar
[`fact-check-prose.md`](../writing/fact-check-prose.md) applies. This is the
code counterpart to that fragment: it fact-checks claims and reasoning
written in prose; this one fact-checks the logic embedded in code itself.

## What to check

- **Strategic correctness (the chosen approach).** Is this the right
  algorithm or design for the problem? A correct-looking implementation of
  the wrong strategy still produces wrong or needlessly costly results ---
  a data structure with the wrong complexity for the expected scale, a
  statistical method whose assumptions don't hold for this data (e.g.
  treating clustered or correlated observations as independent), a
  concurrency strategy prone to races. Ask whether a standard, better-known
  approach exists for this problem that the diff doesn't use --- the review
  counterpart to [`prefer-packaged-functions.md`](prefer-packaged-functions.md),
  but at the level of the overall approach rather than a single function call.
- **Tactical correctness (the implementation).** Given the chosen strategy,
  does the code actually execute it correctly? Off-by-one errors, wrong
  comparison operators, sign errors, a formula transcribed incorrectly from
  a paper or spec, mismatched units or dimensions, incorrect edge-case or
  boundary handling, numerical instability (catastrophic cancellation,
  overflow/underflow).
- **Math and statistics embedded in code.** When code implements a formula,
  statistical test, or model, verify it against its source (a paper, a
  textbook, a package's reference implementation, a spec) with the same
  rigor `fact-check-prose.md` applies to a derivation --- don't assume a
  formula is right because the code compiles and runs. Re-derive or
  spot-check by hand, or construct a small worked example with a known
  answer and compare it against the code's output.

## What to report

For each issue found, state:

1. **Whether it's strategic or tactical.** The fix differs: a strategic
   mistake needs a different approach; a tactical mistake needs a
   correction within the existing approach. Don't file "the algorithm is
   wrong" when the algorithm is right and only a line of it is wrong, or
   vice versa.
2. **The specific line or function**, and what's wrong with it.
3. **The basis for the judgment** --- cite the source checked (a paper, a
   spec, a package's reference implementation, a hand-worked example) so
   the finding can be verified without re-deriving it.

Distinguish blocking correctness issues from optional "there's a better
approach" suggestions, and don't let a plausible-looking implementation pass
unchecked just because it runs without error.
