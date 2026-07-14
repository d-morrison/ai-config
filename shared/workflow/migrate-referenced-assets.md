When moving or removing content that references local files by relative path
--- images, data files, other assets a document embeds rather than links to
externally --- move or remove those referenced files too, not just the
document text. Grep the moved/removed files for asset-path patterns (image
extensions, `assets/`, `images/`, or whatever the project's own convention
is) and confirm each referenced file exists at the destination before
considering a migration or excision complete.

This is easy to miss because the failure mode is often silent or delayed:

- HTML rendering typically degrades gracefully --- a missing image becomes a
  broken-image icon or a rendered "image not found" placeholder, not a
  build failure. A migration can look completely clean in the common render
  target and still be missing files.
- A LaTeX-backed PDF render does **not** degrade gracefully: it hard-fails
  the whole document when it can't find a referenced image, often well after
  the rest of the render succeeded. If PDF (or another format sharing the
  same asset resolution) isn't part of the default CI render, this can stay
  undiscovered until someone builds that format specifically.
- Spell-check, link-check, and lint passes don't catch a missing local
  asset --- a relative image path isn't a spelling word or an external link,
  so none of the usual content-quality CI catches this gap.

When *removing* content instead of moving it, check the inverse case too:
does an asset referenced only by the removed content become orphaned? Decide
whether to delete it along with the text, or leave a note for a follow-up
cleanup pass --- don't leave it silently unreferenced with no record of why.

(d-morrison/wai#6, 2026-07-14: a chapter migration from one Quarto repo to
another moved 25 `.qmd` fragments referencing five meme images, but never
copied the `assets/images/` directory itself. HTML rendering silently
degraded to missing-image placeholders and every other CI check passed, so
the gap wasn't caught until the PDF render --- part of the same "render all
formats" publish job, just slower to reach --- hard-failed with a LaTeX
"file not found" error. Fixed as a follow-up, wai#13.)
