---
description: "Cancel superseded (older) pipelines on the same branch, freeing runners for the latest push. Use when asked to 'cancel old pipelines', 'cancel superseded', 'free up runners', or when you notice stale pipelines blocking newer ones."
---

# Cancel Superseded Pipelines

Cancel older pipelines on the same branch that have been superseded by a newer push,
freeing CI runners for the latest pipeline.

## When to use

- After pushing a fix commit when an older pipeline on the same branch is still running
- When runners are busy and newer pipelines are stuck in `pending`
- When asked to "cancel old pipelines", "free up runners", or "cancel superseded"
- Proactively during ARDI loops when multiple pushes happen in quick succession

## Procedure

1. **Identify the current branch and its latest pipeline:**

```bash
BRANCH=$(git branch --show-current)
# Get pipelines for this branch, newest first
glab api "projects/<PROJECT_ID>/pipelines?ref=$BRANCH&sort=desc&per_page=10" 2>&1 | \
  python3 -c "
import json, sys
pipelines = json.load(sys.stdin)
for p in pipelines:
    print(f'{p[\"id\"]:>6}  {p[\"status\"]:12s}  {p[\"ref\"]}')
" | cat
```

2. **Cancel all but the newest running/pending pipeline:**

Keep the **first** (newest) pipeline. Cancel any older ones that are `running` or `pending`:

```bash
glab api "projects/<PROJECT_ID>/pipelines?ref=$BRANCH&sort=desc&per_page=10" 2>&1 | \
  python3 -c "
import json, sys
pipelines = json.load(sys.stdin)
# Filter to cancelable states
active = [p for p in pipelines if p['status'] in ('running', 'pending', 'created')]
if len(active) <= 1:
    print('Nothing to cancel — only one active pipeline.')
    sys.exit(0)
# Keep the newest, cancel the rest
keep = active[0]
print(f'Keeping pipeline #{keep[\"id\"]} ({keep[\"status\"]})')
for p in active[1:]:
    print(f'Canceling pipeline #{p[\"id\"]} ({p[\"status\"]})')
    # Print the cancel command
    print(f'  -> glab api -X POST projects/<PROJECT_ID>/pipelines/{p[\"id\"]}/cancel')
" | cat
```

Then execute the cancel commands:

```bash
glab api -X POST "projects/<PROJECT_ID>/pipelines/<OLD_ID>/cancel" 2>&1 | \
  python3 -c "import json,sys; print(json.load(sys.stdin).get('status','done'))" | cat
```

3. **For multi-branch cleanup** (e.g., after pushing fixes to multiple MR branches):

```bash
for BRANCH in branch1 branch2; do
  echo "=== $BRANCH ==="
  glab api "projects/<PROJECT_ID>/pipelines?ref=$BRANCH&sort=desc&per_page=5" 2>&1 | \
    python3 -c "
import json, sys
pipelines = json.load(sys.stdin)
active = [p for p in pipelines if p['status'] in ('running', 'pending', 'created')]
if len(active) <= 1:
    print('  Nothing to cancel.')
else:
    for p in active[1:]:
        print(f'  Canceling #{p[\"id\"]}')
" | cat
done
```

## Notes

- **Project ID**: Look it up from the repo's `.gitlab-ci.yml` context or use
  `glab api "projects?search=<repo-name>" | python3 -c "..."` to find it.
- **Don't cancel across branches** — only cancel older pipelines on the *same* ref.
- **Don't cancel `success` or `failed`** pipelines — they're already done.
- The `claude-review` job runs early and fast; the `check-package` job is usually
  what's hogging the runner. Canceling a superseded pipeline frees the runner for
  the newer one.
- Always pipe `glab api` through `| cat` to avoid pager issues.
