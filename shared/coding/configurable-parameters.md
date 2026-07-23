Make every parameter configurable.
A quantity a caller could reasonably want to vary --- a size, a count, a
layout, a timing, a threshold, a spawn geometry --- should enter through a
function parameter, a constructor/instance field, or a data file, with
today's value kept as the default. Never bury it as a bare literal inside
the implementation where only an edit to that function's own source can
change it.

## The exemption

**Empirically known physical constants** (gravity, unit conversions,
measured material properties) and **true mathematical constants** are
exempt --- values with an external provenance that no caller has any
business varying. The test: would a caller ever legitimately want a
different value for a different call, run, or configuration? If yes, it's a
parameter. If the value is fixed by the physical world or by mathematics
itself, it stays a literal.

## Distinct from avoid-hardcoding-external-data

This is a different axis from
[`avoid-hardcoding-external-data`](avoid-hardcoding-external-data.md), which
is about duplicated **ownership** of a fact that already has an external
source of truth (a version number, a package list). This rule is about
**variability**: a value can have no external owner at all --- it's a
constant this project chose --- and still be a parameter, because some
future caller will legitimately want a different value for their own
call site. The two checks compose: a value can fail either, both, or
neither.

## Why

A compile-time or hard-coded constant shared across every caller forces
every future change in scope to become a global, code-editing change ---
and when call sites have accumulated downstream state that assumes the old
value (timing, layout, positioning baked into other artifacts), that
edit can cascade into a large, unplanned retiming/rework sweep instead of
a single call-site argument change.
(Lacaedemon/sparta#945 changed a shared compile-time battlefield-size
constant and had to retime 19 existing clips that had baked in the old
size; Lacaedemon/sparta#960 tracks moving to per-demo configurability to
avoid repeating this.)

## In review

Flag a new hard-coded tunable in a diff as a standard review finding, the
same weight as the other `shared/coding` rules: name the value, confirm it
isn't one of the two exemptions above, and ask for it to become a
parameter/field/data value with the current value as its default.
