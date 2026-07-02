Treat limitations as a starting point to work past, not a fixed constraint to
accept. When something can't currently be done --- a missing tool, an awkward
manual workaround, "we can't check X automatically," a model or package that
seems insufficient --- the default response is to go get the resource that
removes the limitation, not to shrug and route around it indefinitely.

Concretely, that means actively seeking out:

- **Tools and integrations** --- a missing MCP server, CLI, or API access that
  would turn a manual step into an automated one.
- **Packages and dependencies** --- see
  [`prefer-packaged-functions`](../coding/prefer-packaged-functions.md); reach
  for an existing well-maintained package before accepting hand-rolled code as
  the ceiling.
- **Upstream fixes** --- see [`upstream-issues`](upstream-issues.md); file the
  issue or PR that fixes the root cause instead of permanently living with a
  local workaround.
- **Better-fit models** --- see the `assess-model-fit` skill; if a task is
  running into capability limits, that's a signal to check whether a stronger
  model or different approach closes the gap, not just to lower expectations.
- **Access and permissions** --- if a session lacks scope, a credential, or a
  tool needed to do the job properly, say so and ask for it rather than
  quietly working within the narrower capability.

This is a bias, not a mandate to gold-plate every task: a workaround is still
the right call when the fix is genuinely out of scope, disproportionate to the
problem, or not the user's to authorize (see `upstream-issues`' contribution-
policy gate). The point is to default to seeking the resource first, and only
settle for the current limitation after that's been considered --- not to treat
the current limitation as the ceiling from the outset.
