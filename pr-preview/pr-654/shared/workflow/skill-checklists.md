Use checklists in skills deliberately, not by default.

Add a checklist only when all three are true:

1. **Repeatable:** the same failure mode recurs across sessions.
2. **High-cost miss:** missing the step causes real churn (extra review rounds,
   broken CI, duplicate work, incorrect "clean" claims).
3. **Observable:** each item can be confirmed mechanically ("did we post the
   claim comment", "did we resolve every inline thread"), not by vague judgment.

When those conditions hold, checklist-ize the risky boundary:

- Keep it short (about 4-8 items) and ordered by execution.
- Write each item as an action + evidence pair, not a slogan.
- Place it where the miss happens (pre-push, pre-merge, end-of-round), not as a
  generic preamble.
- Reuse one canonical checklist for the family when possible; aliases should
  point to that canonical location rather than copy it.

Skip checklist-izing skills that are mostly design judgment, exploratory
research, or one-off improvisation. For those, rigid boxes add noise and slow
good decisions without reducing real failure risk.

