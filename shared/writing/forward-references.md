A **forward reference** is any mention that points a reader ahead to
content they haven't reached yet --- a phrase like "as discussed below",
"in the following section", "we'll cover this later", or "as we'll see" ---
where the thing being pointed at genuinely comes later in reading order.
Good technical prose avoids these: they force the reader to hold an
unresolved pointer, and they're a common enough weakness that they're worth
a dedicated check, distinct from
[`definition-crossrefs.md`](definition-crossrefs.md)'s narrower check of
formal Quarto crossref-div ordering (`{#def-...}`, `{#thm-...}`, etc.) for
term and result definitions specifically. This fragment covers the general
case: **any** plain-text forward-pointing phrase, about **any** kind of
content (a section, a figure, a table, an argument, not just a formal
definition), in any prose --- READMEs, docs, papers, PR descriptions.

## The detection heuristic

The cheapest, most reliable signal: **a cross-reference or named-content
mention paired with a directional word that means "later"** --- below,
later, following, subsequently, further down, next (as in "the next
section"), afterward. The author is self-declaring the direction, so a
grep for the word near a reference cue finds most real instances without
having to read the whole document first:

```bash
rg -niE '(@[a-z0-9_-]+|section|figure|table|chapter|the following|as (we|you)('"'"'ll| will) see)[^.]{0,60}\b(below|later|subsequently|further down)\b' <file>
rg -niE '\b(below|later|subsequently|further down)\b[^.]{0,60}(@[a-z0-9_-]+|section|figure|table|chapter)' <file>
```

Treat every hit as a **candidate**, not a confirmed finding --- see the false
positives below.

## Confirming a hit

For each candidate, check two things:

1. **Is it actually a reference, not an idiom?** "Values below zero", "the
   below-threshold group", "below average" use "below" as a plain adjective
   or comparator, not a pointer to later content. Read the sentence; don't
   flag these.
2. **Does the target really come later?** Find what the phrase points at
   (a heading, a crossref target, a named figure/table). If it already
   precedes the mention, the wording is simply wrong (should say "above")
   but there's no forward-reference problem to fix structurally.

Only a hit that is (a) a genuine reference and (b) genuinely pointing
ahead is a forward reference to fix.

## Fixing a confirmed forward reference

Two options, in order of preference:

1. **Reorder.** Move the referenced content (the section, paragraph, div,
   figure, or table) earlier so it precedes the mention, then update the
   directional word ("below" → "above", or drop it if a working crossref
   link already carries the point). This is the strong fix: the reader
   never has to hold an unresolved pointer.
2. **Reword**, when reordering would break the document's narrative logic
   (e.g., a result genuinely depends on setup that must come first). Turn
   the vague pointer into a precise, working link (a real crossref or
   anchor) instead of a bare "below" --- this doesn't remove the forward
   reference, but at least lets the reader jump to it rather than search.
   Use this only when reordering is genuinely worse, not as a default
   shortcut.

## The roadmap exception

A deliberate scene-setting overview near the start of a document or
section ("this paper first covers X, then Y, then Z") is a conventional,
expected forward reference, not an error --- the reader isn't meant to
resolve it immediately, just to know what's coming. Scope this check to
places where the reader needs the pointed-at content *to understand the
current sentence*, not to a roadmap paragraph that's explicitly previewing
structure.

## Relationship to other checks

- **[`definition-crossrefs.md`](definition-crossrefs.md)** --- the special
  case of this same problem for formal term/result definitions via Quarto
  crossref divs. That check works by comparing div position to first
  mention directly; this one works by grepping for self-declared
  directional language. Run both: a definition can be forward-referenced
  without ever using the word "below" (a bare `@def-x` crossref with no
  signpost at all), which only `definition-crossrefs.md`'s ordering check
  catches.
- **[`challenge-ambiguous-terminology.md`](../workflow/challenge-ambiguous-terminology.md)**
  --- catches unclear terms; this check assumes the term is clear and
  instead verifies the reader has already been given whatever it's
  pointing at.
- **[`semantic-line-breaks.md`](semantic-line-breaks.md)** --- a sibling
  prose-quality check; both are the kind of finding worth raising as a
  suggestion during review of a prose diff.
