## Writing: include every step in derivations

When writing a mathematical derivation or proof,
include every intermediate step —
do not skip steps, even when they seem obvious.
A derivation with a missing step forces every reader
to reconstruct it independently;
a derivation with an extra "obvious" step costs almost nothing.

Apply this to all derivation contexts:
algebraic manipulation, probability calculations,
statistical results, limit arguments,
and the links between model assumptions and conclusions.

## Review: flag missing steps and draft the fill-in

When reviewing a derivation or proof,
check not only that stated steps are correct
but also that no step is missing.
This is a distinct check from
[`fact-check-prose.md`](fact-check-prose.md),
which verifies whether stated steps follow from each other;
this one asks whether any step between two consecutive lines
has been left out entirely.

For each gap found:

1. **Name the exact transition.**
   Quote or reference the two consecutive lines
   between which a step is missing
   (e.g. "between equations (3) and (4)").
2. **Name the missing operation.**
   State what algebraic, probabilistic, or logical move
   closes the gap
   (e.g. "apply the chain rule",
   "expand the expectation by linearity",
   "substitute the definition of the likelihood").
3. **Draft the missing line where feasible.**
   Write out the intermediate expression
   so the author can insert it verbatim or with minor edits,
   rather than re-deriving it from scratch.

Treat a missing step as a genuine finding,
not a nit:
a reviewer who reconstructs a gap silently
does the reader's work for them
without fixing the document for the next reader.
