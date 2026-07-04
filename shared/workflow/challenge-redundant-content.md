When reviewing code or prose --- including mathematical content (derivations,
proofs, restated formulas) --- check for redundant content that could be
consolidated, and question it rather than silently accepting duplication.
Redundancy is doubly costly: more to read, and more to keep in sync when one
copy changes and the other doesn't.

**The litmus test: only flag content as redundant when consolidating it would
lose nothing.** If removing one copy would drop a case, an edge condition, a
generality, or a distinct meaning, it is not redundant --- it's merely similar.
Flagging similar-but-distinct content as a duplicate recommends a merge that
loses something; that's a worse outcome than leaving the duplication alone.
Question the content, don't assume either way: check what each copy actually
covers before deciding whether one subsumes the other.

## What this looks like in each domain

- **Prose.** The same claim or explanation restated in two places --- a README
  section and a doc page saying the same thing in different words, two
  paragraphs in the same document making the same point --- that could become
  one statement plus a cross-reference to it.
- **Math.** A general formula and a separately derived special case that the
  general formula already covers; the same derivation carried out twice in
  different notation with no added insight; a theorem re-proved in place
  instead of cited. Consolidating here means stating the general result once
  and deriving the special case from it (or citing it), not deleting the
  special case's meaning if it actually adds a constraint the general form
  doesn't capture.
- **Code.** Duplicated logic across functions, files, or configuration that
  could be extracted into one shared unit without narrowing what either call
  site needs. Two functions that look alike but branch on genuinely different
  conditions are not this case --- extracting a shared unit there would need a
  parameter or flag for the branch, and that's a judgment call, not an
  automatic win.

## Applies at the scale of what's in front of you

This is a review-time check on the document or diff already being read, not a
mandate to sweep an entire corpus for duplication --- that's a separate,
larger job with its own tooling. When the redundancy found here turns out to
span more than the current diff (the same fact duplicated across many files,
the same procedure copied into several unrelated places), say so and route it
to `find-overlap` (or `consolidate-skills`/`consolidate-memory` for
skills/memories), rather than trying to fix everything found along the way in
the current review.
