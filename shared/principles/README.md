# Big-picture principles

The central home for our big-picture development principles.
Each principle gets a short statement here plus links to the specific
rules and skills that operationalize it; a principle with enough depth
gets its own fragment file in this directory.

The specific rules stay authoritative for their own details.
This catalog is the index: it names each principle and shows how the
principles relate, so a new rule can be filed under the principle it
serves instead of floating free.

## The goals the principles serve

The catalog has three layers: these **goals** are the *why*, the
**principles** below are the *how*, and the specific rules and skills
each principle links to are the *what*.
We build code and prose that is:

- **Valid** — correct in logic, math, and claims — and **easy to
  externally validate**: tested, checkable by deterministic instruments
  (see [`algorithmatize-checks`](../workflow/algorithmatize-checks.md)),
  reproducible, and cited so a reader can verify without re-deriving.
- **Highly functional** — it does the whole job it exists for, not an
  approximation of it.
- **Efficient** — economical with compute, memory, and people's time
  (CI minutes, review rounds); performance tuning beyond that needs a
  demonstrated hot spot, not speculation.
- **Maintainable** — the next change is cheap: one home per fact, small
  units, no accumulated complexity debt.
- **Extensible** — new capability slots in without rework, because the
  units are composable and the abstractions are real ones.
- **Human- and AI-readable** — a reader (including future us) can
  follow it without archaeology: plain prose, idiomatic code.
  Equally legible to AI agents: conventions stated where agents load
  them (`CLAUDE.md`, shared fragments), greppable naming, and context
  that doesn't depend on out-of-band knowledge.
- **Reusable** — built once, usable across our repos; and conversely,
  built on what already exists rather than duplicated (DRW).

When a proposed rule or review finding doesn't clearly serve one of
these goals, question the rule rather than the code.

## KISS — keep it simple, stupid

Prefer the simplest construct that does the job, and treat added
complexity as a cost that needs justification.
The umbrella statement lives in `CLAUDE.md` ("KISS is the umbrella
principle"); when a case arises that no enumerated rule covers, apply
KISS directly.

Operationalized by:
[`challenge-unnecessary-complexity`](../workflow/challenge-unnecessary-complexity.md)
(the review side),
[`avoid-nesting`](../coding/avoid-nesting.md),
[`tidy-code`](../coding/tidy-code.md), and
[`per-operation-grouping`](../coding/per-operation-grouping.md).

## DRY — don't repeat yourself

Every fact and every piece of logic gets exactly one home; a second
copy is a sync bug waiting to happen, because updating one copy should
have updated the other and eventually won't.

Operationalized by:
[`challenge-redundant-content`](../workflow/challenge-redundant-content.md)
(the review side),
[`reuse-docs-and-args`](../coding/reuse-docs-and-args.md),
[`avoid-hardcoding-external-data`](../coding/avoid-hardcoding-external-data.md),
and the `find-overlap` / `consolidate-skills` / `consolidate-memory`
skills (the corpus-wide sweep).

## DRW — don't reinvent the wheel

Before implementing a new function or feature, check whether it has
already been done — in one of our own repos, or in a trustworthy
external source we could depend on, fork, or contribute to instead.

Full statement: [`dont-reinvent-wheel`](dont-reinvent-wheel.md).
Operationalized by:
[`prefer-packaged-functions`](../coding/prefer-packaged-functions.md)
(the R-function special case), the
[`prefer-upstream`](../../skills/prefer-upstream/SKILL.md) skill (the
search procedure), and the
[`scout-peers`](../../skills/scout-peers/SKILL.md) skill (license-gated
borrowing from peer repos).

## Modularity — small, single-purpose, composable units

Favor small, single-purpose functions and reusable units over long
monolithic blocks, so each piece can be found, tested, documented, and
reused on its own.

Operationalized by:
[`one-function-per-file`](../coding/one-function-per-file.md),
[`decompose-to-functions`](../coding/decompose-to-functions.md), and the
"highly modular and idiomatic" review priorities in
[`gha`'s `CLAUDE.md`](https://github.com/d-morrison/gha/blob/main/CLAUDE.md)
(favor small, single-purpose functions over long monolithic blocks;
flag duplicated logic, functions that do too much, and steps that
should be extracted and named).

## How the principles relate — and where they pull against each other

KISS is the umbrella for the complexity-cost family: most of the
specific coding rules are special cases of "the simplest construct that
does the job".

DRY and modularity overlap KISS but are **siblings, not subsets**.
Deduplicating or decomposing adds indirection — an extracted
abstraction, another file, another call hop — that a narrow KISS
reading resists, in exchange for one-home maintenance, testability,
and reuse.
When they conflict, judgment decides case by case: don't abstract
prematurely (a wrong abstraction costs more than a little duplication;
wait for a pattern to actually recur before extracting it), but once
the same fact or logic has two hand-maintained copies, DRY wins.

DRW is the outward-facing sibling: KISS, DRY, and modularity govern the
code we write; DRW asks first whether we should be writing it at all,
or reusing, forking, or contributing to something that already exists.

## Adding a principle

When a new big-picture principle emerges (from review feedback, a
correction, a recurring pattern), add it here: a short statement, links
to whatever operationalizes it, and — if it needs more than a
paragraph — its own fragment file in this directory, wired into
`CLAUDE.md` with an `@shared/principles/...` reference.
