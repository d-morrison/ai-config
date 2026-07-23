# UMS — Update Memories and Skills

Actively review recent session context and update all relevant memory files and skill definitions to capture what was learned. Unlike `record-learnings` (which records individual facts in place as they arise), UMS is a reflective checkpoint: survey what accumulated, categorize it, and persist it all in one committed pass.

## When this fires

- **As soon as a learning worth saving shows up** — a corrected mistake, a new preference, a tool quirk, a workflow gap. This is the primary trigger: run UMS right then, interleaved with the main work, instead of batching learnings for a wrap-up step at the end. Don’t wait for the task to finish or for `/clear` to accumulate a backlog — and don’t gate it on approval or on a PR merging: capture the learning the moment it appears, even while the PR that taught it is still open and unreviewed.
- User says “ums”, “update memories and skills”, “record what we learned”
- **At the start of `/clear`** — a backstop, not the primary trigger: catch anything accumulated since the last proactive pass before context is lost
- After a workflow reveals a gap (e.g., a skill was followed but missed a step, or a preference wasn’t encoded)
- When the user says “did you update memories?” (the answer should be “let me do that now”)

## Procedure

**Scan recent context.** Review the conversation for:

- Mistakes made and corrected (skill gaps)
- New preferences expressed by the user
- Tool quirks discovered
- Workflow steps that were missing or unclear in existing skills
- Debugging insights
- Codebase conventions discovered

**Categorize each learning.** For each item, decide:

- Is it a **skill update**? (workflow step missing, procedure unclear)
- Is it a **memory note**? (tool quirk, preference, debugging insight)
- Is it **both**? (general guidance → update skill AND preferences)
- Is it already recorded? (check before writing — avoid duplicates)
- Is it **cross-project or project-specific**? (`memories/preferences.md`’s “Memory and skill storage” rule: cross-project lessons commit to `d-morrison/ai-config`; a convention/gotcha tied to one repo we own commits to *that* repo’s own agent docs instead — see the checklist item below for where. This changes step 4’s target, not just the content.)

**Apply updates.** For each item:

- Read the target file first (skill or memory) to understand current state
- Make the edit — concise bullet points, not prose
- If updating a skill: the change should be specific enough that following the skill next time would avoid the mistake

**Commit and push — via a branch + PR, not direct to `main`, in whichever repo step 2 routed the item to.**

**Cross-project items** (skills, cross-project memory notes): both live in the ai-config repo. Discover its path with `git -C ~/.claude/skills/ums rev-parse --show-toplevel` — point `-C` at a **skill subdir** (any one), not the `~/.claude/skills` parent. `bootstrap.sh` may symlink skills *per-child* into a real `~/.claude/skills` directory (cloud/web sessions pre-populate it), so the parent itself isn’t a symlink into the repo and `git -C` there fails with “not a git repository”; a child like `…/skills/ums` follows the symlink into the repo. (Both beat the older `dirname "$(readlink …)"`, which resolves only one symlink hop.) Never leave ANY changes (skills, memories, etc.) as local-only uncommitted edits. Run **one** of the two paths below — not both:

**Stage only the files you actually edited — NEVER `git add -A`.** The working tree often holds unrelated in-flight edits (the user’s own UMS commits, another skill being drafted); `git add -A` sweeps those into your commit and onto your PR, where they bloat the review and extend the cycle. List the specific paths instead. Then **`git status` to confirm only your intended files are staged** — if something unexpected is there, the working tree had in-flight work; unstage it rather than bundling it. (Avoid `git add -p` here: it needs a terminal and hangs in non-interactive sessions.)

*Already on the open PR’s branch* (e.g. mid-ARDI): commit + push to it.

``` bash
cd "$(git -C ~/.claude/skills/ums rev-parse --show-toplevel)"
git add skills/<name>/SKILL.md memories/<file>.md   # the files you touched
git commit -m "ums: <brief summary>"   # COMMIT
git push origin HEAD                   # PUSH
```

*No PR yet:* branch off main first — a direct-to-main push is denied by auto-mode and bypasses review.

``` bash
cd "$(git -C ~/.claude/skills/ums rev-parse --show-toplevel)"
git fetch origin main && git checkout -b ums-<topic> origin/main   # FETCH + CREATE_BRANCH
git add skills/<name>/SKILL.md memories/<file>.md   # the files you touched
git commit -m "ums: <brief summary>"   # COMMIT
git push -u origin HEAD && gh pr create --fill   # PUSH + CREATE_PR — then request d-morrison as reviewer
```

**CAUTION:** if a compound `add && commit && push` is **denied**, *nothing* was committed — verify with `git status` / `git log` before any `git reset --hard`, or you’ll silently discard the still-uncommitted edits.

**After every push in UMS, verify PR state for the current branch in the intended base repo.** `gh pr list --head <owner>:<branch>` silently returns empty for an owner-qualified head — it only matches a bare branch name, even when a matching PR genuinely exists (verified directly: `gh pr list --head d-morrison:ums-pr635-lessons` returned `[]` against a real open PR on that exact branch, while `gh pr list --head ums-pr635-lessons` found it). Query the REST API instead, whose `head` filter does honor the owner-qualified form: `gh api --method GET "repos/<upstream-owner>/<repo>/pulls" -f "head=<head-owner>:<current-branch>" -f "state=open" --jq '.[] | {number, url, state}'` (for `dem-extra1/ai-config`, that is `gh api --method GET "repos/d-morrison/ai-config/pulls" -f "head=dem-extra1:<current-branch>" -f "state=open" ...`). If no open PR exists and upstream is accessible, open it immediately as cross-fork with non-interactive metadata and the reviewer request in the same command (bare `gh pr create` without `--fill`/`--title`/`--body` prompts interactively and can hang a headless session): `gh pr create --repo <upstream-owner>/<repo> --base main --head <head-owner>:<current-branch> --fill --reviewer d-morrison`. If upstream is not accessible in-session, push and explicitly hand off that upstream PR creation is still required.

**Project-specific items** (a convention or gotcha tied to one repo we own): commit to *that* repo’s own agent docs (`CLAUDE.md`, `.github/agents/*.md`, `.github/instructions/*.md`) via a branch + PR in that repo — not ai-config. Discover its path the same way, `cd`-ing into that repo’s own checkout instead of the ai-config one, then follow the same branch/commit/push/PR steps above. If that repo has no agent-doc infrastructure, fall back to its local Claude project memory (`~/.claude/projects/<project-path>/memory/`, write directly, no commit) — see the checklist item below.

**Operational checklist (run in order):**

**Preflight:** confirm branch + cleanliness (`git branch --show-current` / `git status --short`)

**Safe write form:** for any external post with markdown/backticks, use file-backed bodies (`--body-file` or `-F body=@<file>`), never inline double-quoted body strings

**Postcondition:** after push, verify open PR exists in the intended base repo for the head owner/branch (`gh api --method GET "repos/<upstream-owner>/<repo>/pulls" -f "head=<head-owner>:<branch>" -f "state=open" --jq '.[] | {number, url, state}'` — not `gh pr list --head <owner>:<branch>`, which silently returns empty for an owner-qualified head)

**Recovery signature:** if shell logs `command not found` during a comment/create command, first check whether `gh`/`glab` is actually installed (`which gh`); if it is unavailable in this session (expected in remote/web sessions), fall back to the MCP tool mapping in `tool-mappings.md` instead of retrying the CLI — if it *is* installed, the likely cause is backtick substitution mangling the body; re-run using a file-backed body and re-check posted content

**Report what was updated.** Provide a brief summary table:

| What | Where | Change |
|----|----|----|
| Poll for new reviews | `iterate/SKILL.md` | Added explicit polling procedure |
| glab has no –state flag | `/memories/tools.md` | New bullet |

## What to look for (checklist)

Did I follow a skill but miss a step? → Update the skill

Did the user correct my behavior? → Encode as preference + skill update

Did I discover a tool quirk? → `/memories/tools.md`

Did I learn a debugging pattern? → `/memories/debugging.md`

Did I create a *new* file under `/memories/`? → register it in `memories/MEMORY.md` as an index entry

Did I discover a repo convention for a repo **we own** that has checked-in agent docs? → put it IN that repo (its `CLAUDE.md`, `.github/agents/*.md`, or `.github/instructions/*.md`), via a PR, so the whole team and every `@claude` session there sees it. Do NOT keep repo-specific notes in ai-config (`memories/repo/` is retired). For a repo without agent-doc infrastructure, fall back to that repo’s local Claude project memory: `~/.claude/projects/<project-path>/memory/` (write directly; no commit).

Did the user express a new preference? → `/memories/preferences.md`

Did a workflow emerge that could be a new skill? → run `spot-skill-opportunities` to judge whether it’s genuinely recurring, then `skill-builder` to create it

Did a heavy skill’s fan-out step need a dedicated read-only worker persona (like `dependency-auditor` / `hallucination-detector` / `community-demand-scout`), rather than just a new skill? → run `agent-builder` to scaffold `.claude/agents/<name>.md`

Are there existing skills that reference outdated info? → Fix them

Has `learn-staging.md` accumulated entries since the last `promote-memory` run? → fold in a `promote-memory` pass now.

Did I edit one step’s scope without updating sibling steps in the same file? → Search the file for all enumerations of the changed category and make them consistent.

Did I add a shared-procedure step to one skill but not to sibling skills? → Grep sibling skills for the same action and add the step there too.

Did I change how a skill describes its relationship/contrast to a sibling skill (e.g. “X is passive, Y is explicit”)? → Grep the sibling skill for its own mirrored description of that same relationship and update it too — a one-directional fix leaves the sibling’s docs contradicting the new behavior. (Caught by `@claude` review on ai-config#439: `ums/SKILL.md`’s passive-vs-active contrast with `record-learnings` was fixed, but `record-learnings/SKILL.md`’s own mirrored line describing `ums` as “the explicit … counterpart” was missed until review flagged it as a follow-on.)

## Relationship to record-learnings and staged capture

- `record-learnings` = records individual facts in place, in the moment they arise
- `ums` = a reflective, full-context sweep — survey what accumulated, categorize it, and persist it all in one committed pass

Both write to the same destinations. `ums` fires proactively, as soon as a learning worth saving shows up, rather than waiting to catch up later; the `/clear` trigger is only a backstop for anything that slipped through.

`spot-skill-opportunities` is the standing, continuous version of this skill’s “did a workflow emerge that could be a new skill?” checklist item — it runs the recognition judgment call live, in the moment, instead of only at this checkpoint. `agent-builder` is the sibling construction step for the other checklist item above — a recurring fan-out worker persona rather than a new user-invocable skill.

`learn`/`promote-memory` are a staged alternative for the uncertain case: `record-learnings` and this skill both write directly to committed memory the moment something looks worth remembering, which is right when you’re confident. When you’re not — a candidate whose generality or evidence isn’t solid yet — `learn` stages it instead, and a `promote-memory` pass (which a `ums` run can fold in, or run standalone) reviews staged candidates before they land in committed memory. Neither replaces the direct-write path; they add a review gate for the cases that need one.

## Anti-patterns

- ❌ Saying “I’ll remember that” without actually writing it down
- ❌ Updating memories but not pushing skill changes to origin
- ❌ Recording vague lessons (“be more careful”) instead of specific ones (“always poll for new review after pushing — check commit SHA matches”)
- ❌ Skipping the “check existing notes” step and creating duplicates
- ❌ Updating only preferences when a skill also needs the fix
- ❌ `git add -A` — it sweeps unrelated in-flight edits (the user’s work, other draft skills) into your commit/PR. Stage the specific files you touched.
- ❌ Creating `memories/repo/<repo>.md` for any repo — this pattern is retired. Put repo-specific lore in the repo’s own agent docs (`.github/agents/`, `CLAUDE.md`, `.github/instructions/`) via a PR, or in `~/.claude/projects/<project-path>/memory/` (local project memory, no commit) if the repo has no agent-doc infrastructure. See the checklist item above and `memories/preferences.md` for the full rule.
- ❌ Inserting a new bullet into any memory file with nested lists (including `tools.md`, `preferences.md`) without checking the surrounding indentation first. These files mix 0-indent top-level bullets with 2-/4-indent sub-bullets and multi-paragraph continuations; a new top-level bullet dropped in the middle of an existing parent’s sub-list re-parents whatever follows it in Markdown (a sibling sub-bullet silently becomes this new bullet’s child). Before committing an insertion, re-read the few lines immediately above and below the insertion point and confirm the indentation still matches what it did before — or place the new bullet after the complete enclosing list instead of inside it. (Caught by `@claude` review on ai-config#335: a new 0-indent bullet landed between two sibling sub-bullets of an existing parent, breaking the nesting.)

Back to top
