# MEMORY.md --- index of `memories/`

Index of the cross-project memory files in this directory. The `memorize` skill
records a memory in two steps: write the file, then register it here so the
corpus stays discoverable. Add a row below whenever you add a memory file.

This index covers only the general, cross-project memories kept in the
ai-config repo. Repo-specific memories live outside the repo, under
`~/.claude/projects/<project-path>/memory/`, each with its own `MEMORY.md`
index in that directory.

| File | Title | Covers |
|------|-------|--------|
| [`preferences.md`](preferences.md) | User preferences (cross-workspace) | Standing working rules: never-assume/always-verify, record learnings as you go, cite sources for tool-behavior claims, issue-first, and the ARDI / fully-clean definitions. |
| [`tools.md`](tools.md) | Local tools & CLIs | Tool and CLI behavior: `gh` pager and shared rate limits, REST-vs-GraphQL fallbacks, the `@claude` review bot's author name and re-trigger steps, sub-issue linking, and R / Quarto quirks in cloud / web sessions. |
| [`debugging.md`](debugging.md) | Debugging notes | Debugging practices: test CSS/JS web features in a real headless browser (not a DOM stub), the VS Code editor-vs-disk desync trap, and ARDI review-polling behavior. |
