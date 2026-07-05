ai-config work is done (PR #501): `shared/writing/math-derivation-steps.md` added and wired into CLAUDE.md.

Two cross-repo follow-ups are blocked in this session (permission constraints on writing to other repos):

**gha** — add item 13 to Code review guidelines in CLAUDE.md. The new item should follow the pattern of items 8–12:

```
### 13. Include every derivation step; flag missing steps

When reviewing a diff that adds or modifies a mathematical derivation or
proof, check not only that stated steps are correct (item 8) but also that
no step is missing between two consecutive lines.
For each gap found: name the exact transition (the two lines between which
a step is absent), name the missing operation (e.g. "apply the chain rule",
"expand by linearity of expectation"), and draft the missing intermediate
line where feasible so the author can insert it rather than re-derive it.
Treat a missing step as a genuine finding, not a nit.
This is a global standing rule from the
`d-morrison/ai-config` corpus (`shared/writing/math-derivation-steps.md`).
```

**rme** — in the Math Notation section of CLAUDE.md, the existing bullet `- Include every intermediate step in derivations — do not skip steps` covers the writing-time rule. Add a cross-reference to the shared fragment for the review-time counterpart (or replace the bullet with a pointer to `shared/writing/math-derivation-steps.md`).

**epi204** — same update as rme once the CLAUDE.md for that repo is located (404 on first lookup).
