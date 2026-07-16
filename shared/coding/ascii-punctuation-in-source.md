Never use em-dashes (`—`, U+2014) in source-code files. This covers `.R`,
`.py`, `.qmd`, and any other code file, including the comments, roxygen/
docstring prose, and string literals inside them. Use ASCII punctuation
instead: a comma, colon, or semicolon where the em-dash joined clauses, a
spaced double hyphen (`--`) when a dash is genuinely wanted, or a plain
hyphen (`-`) for a compound.

The same rule extends to the other non-ASCII punctuation that slips in from
the same source (copy-paste from rendered text, an editor's smart-quote
autocorrect): en-dashes (`–`), curly quotes (`“ ” ‘ ’` -> `" '`), and stray
symbols like the multiplication sign (`×` -> `x`, or a context-appropriate
escape when the glyph must survive in output; see the last paragraph).

**Why source files specifically, not all prose.** Repositories commonly gate
source on an ASCII-only check that a plain Markdown doc is exempt from:

- R CMD check's "checking code files for non-ASCII characters" flags any
  non-ASCII byte in `R/`; under `error_on = "note"` it fails the build. Note
  that a helper defined in `data-raw/` (excluded from the build) passes
  silently until the function moves into `R/`, at which point the same
  em-dash starts failing CI.
- Some repos run a dedicated non-standard-character workflow over `.qmd` and
  `.R` (e.g. the UCD-SERG lab manual's `check-non-standard-chars`), which
  rejects em-dashes, curly quotes, and en-dashes outright.

So this is a source-code hygiene rule, not a general writing-style
preference: ordinary `.md` docs and chat prose are not the target. When the
glyph must appear in rendered output, keep the source ASCII in a
context-appropriate way. In an R or Python string literal (a `cli` message,
a plot label), use the `\uXXXX` escape, which the language decodes to the
character. In `.qmd` prose, `\uXXXX` is not interpreted by Pandoc and renders
literally: use a math span (`$\times$`), an HTML entity (`&times;`), or reword
to avoid the glyph.

Apply it when writing code and when reviewing a diff: a raw em-dash in a
roxygen block or a `.qmd` is a review finding, the same weight as any other
CI-breaking issue, because it will fail the ASCII check before it merges.
