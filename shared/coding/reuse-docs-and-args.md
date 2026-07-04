When writing or reviewing a function that wraps or closely relates to another
function, prefer **reusing** that other function's documentation and argument
list over retyping them.

## Documentation reuse

In R, use [roxygen2's tag-reuse system](https://roxygen2.r-lib.org/reference/tags-reuse.html)
instead of copy-pasting a `@param` description or an explanatory section
between functions:

- **`@inheritParams other_fn`** — pull in `other_fn`'s `@param` documentation
  for any parameter this function shares with it, instead of retyping the
  description.
- **`@inheritDotParams other_fn`** — document a `...` argument by pointing at
  the function it's forwarded to (see "`...` passthrough" below), rather than
  writing out each forwarded parameter by hand.
- **`@inheritSection other_fn "Section Title"`** — reuse a full prose section
  (e.g. a shared "Details" block) instead of duplicating it.

Reused docs stay in sync automatically when the source function's docs
change; copy-pasted docs silently drift. In other languages, use the
equivalent inheritance mechanism instead of copying prose by hand — e.g.
Python Sphinx's `napoleon_use_param`/`:param:` inheritance or a shared
docstring template, JSDoc's `@inheritdoc`, or Doxygen's `@copydoc`.

## `...` passthrough

Favor passing `...` straight through to a subfunction over manually
re-declaring and re-relaying its arguments one by one. See
[Advanced R, "`...` (dot-dot-dot)"](https://adv-r.hadley.nz/functions.html?q=dot-dot#fun-dot-dot-dot):
a wrapper function that doesn't itself use an argument shouldn't name it in
its own signature just to hand it down — declare `...` and forward it
(`inner_fn(...)`), and document it with `@inheritDotParams` as above. This
keeps the wrapper's signature stable when the subfunction's arguments
change, and avoids the wrapper silently going stale (a new argument added to
the subfunction becomes unreachable through the wrapper until someone
remembers to add a matching pass-through parameter).

Apply the same idea in other languages with the analogous mechanism: `**kwargs`
forwarding in Python, spread/rest parameters (`...args`) in JavaScript/TypeScript,
or variadic forwarding in whatever the target language provides.

This is a default, not an absolute rule — name an argument explicitly (instead
of leaving it inside `...`) when the wrapper needs to inspect, validate, or
transform that specific value before forwarding it.

## In review

Flag both as review findings, the same weight as other idiomatic-code
findings: a `@param` description or prose section that's copy-pasted from
another function's docs instead of inherited, and a wrapper function that
manually re-declares and relays arguments it never touches itself instead of
using `...`/`**kwargs`/rest-parameter passthrough.
