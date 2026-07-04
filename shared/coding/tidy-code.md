Write clean, tidy code, and hold code under review to the same bar. A change
should read as if it always belonged in the file: no leftover debug prints,
no dead branches, no needlessly long functions doing three things at once.

In R specifically, prefer concise **tidyverse** idioms over more verbose base
R or `{rlang}` paradigms when both do the job:

```r
# Preferred — tidyverse, concise and pipe-friendly
df |> dplyr::filter(x > 0) |> dplyr::pull(y)

# Avoid — base R subsetting/indexing for the same result
df[df$x > 0, "y"]
```

```r
# Preferred — purrr, concise
purrr::map_dbl(x, mean)

# Avoid — base R apply-family equivalent
vapply(x, mean, numeric(1))
```

```r
# Preferred — rlang's {{ }} embrace, when you do need tidy eval
my_fn <- function(data, col) data |> dplyr::summarise(mean(!!col))

# Avoid — spelling the same thing out with rlang::enquo()/rlang::eval_tidy()
my_fn <- function(data, col) {
  col <- rlang::enquo(col)
  dplyr::summarise(data, rlang::eval_tidy(rlang::quo(mean(!!col)), data))
}
```

This is a readability default, not an absolute rule: reach for base R when
the tidyverse equivalent pulls in a heavy dependency for a one-liner, when
performance in a hot loop matters, or when base R is already the idiom the
surrounding file uses throughout. `{rlang}`'s lower-level tidy-eval building
blocks (`enquo()`, `eval_tidy()`, `sym()`) are for package authors who need
that control; `{{ }}` and other tidyverse-facing shorthand covers nearly
everything else.

This complements [`prefer-packaged-functions`](prefer-packaged-functions.md)
(look for an existing package before hand-rolling) and
[`per-operation-grouping`](per-operation-grouping.md) (a specific dplyr
instance of the same conciseness preference) — this fragment is the general
statement: write tidy code, and in R lean tidyverse over base R/rlang for it.
