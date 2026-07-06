When reviewing prose that defines technical terms or named results via
formal cross-reference divs --- Quarto's theorem-like div syntax
(`::: {#def-...}`, `{#thm-...}`, `{#lem-...}`, `{#cor-...}`, `{#prp-...}`,
`{#cnj-...}`, `{#exm-...}`, `{#exr-...}`) or an equivalent
glossary/definition-list convention --- check two things for every mention:

- **Hyperlinked on first mention.** The first place a technical term or
  named result appears in running prose should link to the div that
  defines or states it --- a Quarto crossref (`@def-token-budget`,
  `@thm-cauchy-schwarz`) or an explicit markdown link to the div's anchor.
  A bare mention of a term the reader hasn't been given a definition for
  forces them to search instead of click.
- **No forward references.** The definition/theorem/lemma/etc. div itself
  must appear **before** its first mention in reading order --- earlier in
  the same document, not later. A crossref pointing at a div the reader
  hasn't reached yet is a forward reference.

Scope note: "same document" means the single rendered file this checklist
runs against. In a multi-file Quarto book, a term defined in a later
chapter and referenced from an earlier one is a forward reference from the
reader's perspective too, but checking reading order across chapter files
is out of scope here --- flag that case manually when reviewing a book-level
diff.

## What to check

- For each technical term or named result mentioned in the prose, find its
  defining div (if one exists) and confirm the first mention is a working
  crossref/link to it, not bare text.
- For each definition/theorem/etc. div, confirm it precedes --- in document
  reading order --- every place that references it, whether a prose mention
  or a crossref used elsewhere in the same document.
- A term or result mentioned but never defined anywhere in the document is
  a separate gap from ordering: flag it as missing a definition entirely,
  not just as a forward reference.

## What to report

For each violation, name the term or result, the mention's location, and
one of:

- **Missing crossref** --- the mention is bare text; add a link to the
  defining div.
- **Forward reference** --- the div is at `<location>`, after the mention
  at `<location>`; move the div earlier, or restructure so the definition
  precedes its use.
- **Undefined term** --- the term is mentioned but no div defines it
  anywhere in the document; add the missing definition.

## Relationship to other checks

- **[`forward-references.md`](forward-references.md)** --- the general case
  of this same problem: any plain-text forward-pointing phrase ("below",
  "later", "in the following section") about any kind of content, not just
  a formal definition/theorem div. That check's grep-for-directional-word
  heuristic won't catch a bare `@def-x` crossref with no signpost word at
  all --- this check's direct div-position comparison is what catches that
  case. Run both on a diff that touches definitions.
- **[`check-rendered-refs`](../../skills/check-rendered-refs/SKILL.md)**
  (`crr`) is a post-render check: does `@def-x` resolve at all, without
  leaking `?@def-x` or `**key?**` into the built HTML. This check runs
  earlier, on the source prose itself: even a crossref that will resolve
  cleanly can still target the wrong spot (no link at all) or point
  backward at content that hasn't appeared yet.
- **[`challenge-ambiguous-terminology.md`](../workflow/challenge-ambiguous-terminology.md)**
  catches terms whose *meaning* is unresolved; this check assumes the
  meaning is fine and instead verifies the *link and its ordering* --- a
  resolved term can still be unlinked or defined too late.
