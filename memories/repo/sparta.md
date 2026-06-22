---
name: sparta-gotchas
description: "Operational gotchas and reviewer conventions for Lacaedemon/sparta (Godot tactical battle game)"
metadata:
  type: feedback
---

# Sparta — working notes

## Website docs scope in stacked PRs

When writing website/ documentation for a stacked PR, only document features whose code is actually present on that branch's ancestry (i.e. reachable via `git log` from that branch). Features that live in a *sibling* branch also targeting `main` are NOT in scope, even if conceptually related.

**Why:** In the terrain-speed PR (#185), website docs were written for the order-response delay feature (from `feat/order-response-delay`, a separate branch targeting `main`). The code was never in `feat/terrain-speed`'s ancestry, so the reviewer correctly flagged it as a "hallucinated feature."

**How to apply:** Before writing docs for a feature, `grep` for the relevant symbol/constant (e.g. `order_response_delay`) on the current branch. If it's absent, the feature isn't in scope — move the docs to the branch where the code lives.
