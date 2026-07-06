When writing or reviewing a mathematical derivation --- an algebraic
manipulation, a proof, a statistical argument --- hold it to a stricter
completeness bar than ordinary prose reasoning.

## Writing: don't skip steps

Write out every intermediate step: every distribution, cancellation,
substitution, application of a named identity or assumption, and change of
notation. Don't combine two or more operations into a single displayed line.
A reader should be able to get from one line to the next by checking a single
mechanical operation, never by re-deriving an omitted one.

This is stricter than ordinary prose, where combining a few closely related
points in one sentence is fine --- a derivation's whole value is that each
line is independently checkable, so skipping a step defeats the purpose even
when the reader could reconstruct it themselves.

## Reviewing: name the gap, don't just flag it

[`fact-check-prose.md`](fact-check-prose.md)'s document-internal-reasoning
check already covers whether each *stated* step is valid (verifying it
follows from the last, checking dimensions/units, checking edge cases). This
fragment is about a different failure mode: a step that isn't stated at
all --- the derivation jumps from one line to a non-adjacent one.

When a derivation skips a step:

1. **Point to the exact gap** --- the last line before the jump and the
   first line after it, not just "this derivation skips steps" in general.
2. **Name the missing operation** --- what specific move closes the gap
   (which distribution, cancellation, substitution, identity, or
   assumption). Don't leave it to the author to guess what you think is
   missing.
3. **Draft the missing line(s)** where feasible, so the author can drop them
   in directly rather than re-deriving the gap themselves --- the same
   spirit as proposing a concrete fix rather than only naming a problem
   (see [`challenge-unnecessary-complexity.md`](../workflow/challenge-unnecessary-complexity.md)'s
   "propose the fix, don't just name the issue" pattern).

A derivation with a plausible-looking but unstated jump is exactly the kind
of gap a reader skims past --- the same reason
[`challenge-ambiguous-terminology.md`](../workflow/challenge-ambiguous-terminology.md)
warns against accepting a plausible reading at face value instead of
verifying it.
