When an R function signature doesn't fit on one line, format the argument
list with **single-indent** style: nothing after `function(`, each argument
on its own line indented one level (+2 spaces), and `) {` on its own line
closing the signature.

```r
# Preferred --- single-indent
build_surv_power_table <- function(
  frac_op,
  frac_nonop,
  projected_total,
  hrs = c(2.0, 1.5)
) {
  ...
}

# Avoid --- hanging/aligned indent
build_surv_power_table <- function(frac_op, frac_nonop, projected_total,
                                   hrs = c(2.0, 1.5)) {
  ...
}
```

A signature that fits within the line limit on one line stays on one line;
this rule is only about how to break long ones.

Why single-indent over hanging indent:

- A rename of the function doesn't reflow every continuation line, so diffs
  stay confined to the argument that actually changed.
- Adding or removing an argument is a one-line diff, like a trailing-comma
  list.
- It matches the tidyverse style guide's current recommendation.

lintr's `indentation_linter` doesn't settle this choice: as of lintr 3.4.0
it rejects a third style — the old *double-indent* form (arguments at +4
with `) {` attached; r-lib/lintr#2830) — but accepts both single-indent and
hanging-aligned indent. Choosing single-indent over hanging-aligned is
therefore a review-level preference, not a CI-enforced one: flag
hanging-indent signatures in review the same way as other formatting
findings, and convert them when touching a file for other reasons.

(Encoded from review feedback on `ucdavis/rampp#137`, 2026-07-17; the
repo-wide conversion of pre-existing hanging signatures there is tracked in
`ucdavis/rampp#139`.)
