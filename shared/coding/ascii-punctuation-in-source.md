Never use em-dashes (U+2014) in tracked source files. This covers `.R`,
`.py`, `.qmd`, `.md`, and any other source file in the repository, including
the comments, roxygen/docstring prose, and string literals inside code
files, and the body of Markdown docs (README, NEWS, docs pages, this corpus's
own fragments). Use ASCII punctuation instead: a comma, colon, or semicolon
where the em-dash joined clauses, a spaced double hyphen (`--`) when a dash is
genuinely wanted, or a plain hyphen (`-`) for a compound.

The same rule extends to the other non-ASCII punctuation that slips in from
the same source (copy-paste from rendered text, an editor's smart-quote
autocorrect): en-dashes (U+2013), curly quotes (U+201C U+201D U+2018 U+2019,
which become `"` and `'`), and stray symbols like the multiplication sign
(U+00D7, which becomes `x`, or a context-appropriate escape when the glyph
must survive in output).

**Scope: every tracked source file, `.md` included.** Markdown files are
source too. They are version-controlled, diffed, and rendered, so the same
smart-quote/copy-paste corruption and whole-paragraph-reflow diffs apply.

This is a separate concern from [`find-ai-tells`](../writing/ai-tells.md)'s
em-dash-*overuse* signal, which is about frequency, not presence -- a single
em-dash there is explicitly called innocent. This rule bans em-dashes in
tracked source files regardless of frequency, for the ASCII-hygiene reasons
above.

Do not exempt a README, a `NEWS.md`, a docs page, or any other Markdown doc,
and do not exempt this corpus's own `shared/` fragments, `CLAUDE.md`s, or
skill files. Chat replies and other ephemeral, non-tracked text are outside
this rule's scope, but the same plain-ASCII habit there avoids
re-introducing the glyphs on the next copy-paste into a file.

**Why this holds even where CI does not gate it.** Some file types are gated
by a check that makes a stray em-dash a hard build failure, though the two
common ones reject different things:

- R CMD check's "checking code files for non-ASCII characters" flags
  non-ASCII bytes in code and string literals in `R/`, but not in comments
  -- "Writing R Extensions" explicitly says other characters "are accepted
  in comments" (verified against the current manual). Under `error_on =
  "note"` a flagged (non-comment) occurrence fails the build. Note that a
  helper defined in `data-raw/` (excluded from the build) passes silently
  until the function moves into `R/`, at which point the same em-dash in
  code starts failing CI.
- Some repos run a dedicated non-standard-character workflow -- e.g. the
  UCD-SERG lab manual's own check, or `d-morrison/gha`'s reusable
  `check-non-standard-chars` -- which rejects only a specific glyph set
  (em-dashes, curly quotes, en-dashes), not every non-ASCII code point, over
  the file types it scans.

Where no CI gate covers a file (commonly a Markdown doc in a repo whose check
only scans `.R`/`.qmd`), the rule is still required, not optional: keep the
file's punctuation and the specific stray symbols named above (the
multiplication sign, U+00D7) ASCII anyway.
This rule doesn't ban other non-ASCII characters in general, like an accented
name or a quoted foreign term -- only the named glyphs.
Treat adding or extending the repo's non-ASCII check to also scan `.md` as
the enforcement follow-up: a repo with no such check yet needs to add one, and
a repo whose check already scans `.R`/`.qmd` needs to extend it. Scanning
`.md` alone isn't enough for `d-morrison/gha`'s `check-non-standard-chars`
specifically -- its glyph set covers curly quotes and en/em-dashes but not
the multiplication sign (verified against its source: no U+00D7 entry in
`NON_STANDARD_CHARS`), so the follow-up there also needs to add that glyph.
When the glyph must appear in rendered output, keep the source ASCII in a
context-appropriate way.
In an R or Python string literal (a status message, a plot label), use the
`\uXXXX` escape, which the language decodes to the character.
In `.qmd`/`.md` prose, `\uXXXX` is not interpreted by Pandoc and renders
literally: use a math span (`$\times$`), an HTML entity (`&times;`), or
reword to avoid the glyph.

Apply it when writing and when reviewing a diff: a raw em-dash in a roxygen
block, a `.qmd`, or a `.md` doc is a review finding, regardless of whether
this particular file is one a CI check currently scans.
Give it the **same review weight** as a CI-breaking issue -- this is not a
claim that it always breaks CI, since not every file type is scanned.
