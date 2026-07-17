When writing code, **avoid nested function calls and nested function
definitions where feasible**:

- Prefer named intermediate variables (or a pipe, e.g. `|>` / `%>%` in R) over
  deeply nested calls like `f(g(h(x)))`. Naming each step makes the data flow
  read top-to-bottom and leaves intermediate values inspectable in a debugger.
- Prefer standalone, top-level function definitions over functions defined
  inside other functions. Nested definitions hide reusable logic, complicate
  unit testing, and obscure scope.

This is a readability/maintainability default, not an absolute rule --- keep the
nesting when flattening it would be more convoluted (a trivial one-argument
wrapper, or a closure that genuinely needs the enclosing scope).

## Lambdas in map()/apply-family calls

The nested-definition rule applies to `purrr::map*()` / `pmap*()` /
`lapply()`-family call sites too: don't wrap a named function in an anonymous
function (lambda) just to fix constant arguments. Pass the mapped elements
positionally and the constants through the mapping function's `...`:

```r
# Preferred --- hr/power match schoenfeld_events()'s leading parameters
# positionally; the constant fractions ride along via map2's `...`
purrr::map2_dbl(
  df$hr, df$power, schoenfeld_events,
  p1 = frac_op, p2 = frac_nonop
)

# Avoid --- a lambda that only fixes constant arguments
purrr::map2_dbl(df$hr, df$power, function(h, p) {
  schoenfeld_events(hr = h, power = p, p1 = frac_op, p2 = frac_nonop)
})
```

purrr's own documentation (since 1.0) mildly recommends the opposite ---
shorthand lambdas over `...`-passing --- for readability. This preference
deliberately overrides that: when the mapped elements line up with the
callee's leading parameters, use `...` and skip the wrapper. Don't relitigate
this in review rounds; cite this fragment instead.

When a wrapper genuinely is necessary --- the mapped element isn't the
callee's leading argument, is used more than once in the body, or the body is
a real expression rather than a single call --- define a **named wrapper
function in its own file** (see
[`one-function-per-file`](one-function-per-file.md)) rather than a lambda.
The one exception is a demonstrated performance reason to define the wrapper
nested inside the calling function (e.g. it must close over a large
enclosing-scope object that would otherwise be passed repeatedly); that is
the same closure escape hatch as the nested-definition rule above.

Apply this when writing code and when reviewing it: a map-site lambda that
only fixes constants is a review finding, the same weight as the other
nesting findings. (Encoded from review feedback on `ucdavis/rampp#137`,
where two power-table builders wrapped `schoenfeld_events()` and
`total_n_for_power_unequal()` in lambdas that `...`-passing replaced.)
