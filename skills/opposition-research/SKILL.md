---
name: opposition-research
description: Mine a competitor's community surfaces (issue trackers, forums, subreddits, reviews) for demanded features and map them to this repo. Use when asked to 'opposition research', 'oppo', 'mine competitor feedback', 'what do users want from <product>', or 'find demanded features from <competitor>'.
user-invocable: true
allowed-tools:
  - WebSearch
  - WebFetch
  - Agent
  - Bash
---

# opposition-research

Find what users of a competitor product are loudly asking for, then map those
demands to this repo. The output is a ranked list of feature gaps — from real
user discourse, not assumptions — plus a prompt to file tracking issues for
anything worth pursuing.

## When this fires

- "What do users want from \<product\>?"
- "Run opposition research on \<competitor\>."
- "What features do \<competitor\> users keep asking for?"
- "Mine \<competitor\> feedback."
- `/opposition-research`, `/oppo`

## Relationship to other skills

- **`scout-peers`** — mines a competitor's **source code and structure** (what
  they *built*). This skill mines their **user community** (what users *want
  next*). The two are complementary: scout-peers tells you what exists; this
  skill tells you what's missing.

## Procedure

### 1. Identify the competitor

Confirm the target product and any scope constraints with the user before
searching. If the prompt is ambiguous (e.g. "our main competitor" without
naming one), ask. Note which community surfaces to prioritize — by default,
cast wide.

### 2. Find the community surfaces

Search for each of these surface types for the named product:

- **Issue trackers** — GitHub/GitLab issue lists; filter for open feature
  requests, the most-commented, or those labeled `enhancement`/`feature`.
- **Feature-request forums** — UserVoice, Canny, Discourse, dedicated feedback
  boards. Sort by votes.
- **Subreddits and community forums** — search `<product> feature request` or
  `<product> wish list` on Reddit; look for the product's own subreddit.
- **Stack Overflow tags** — questions marked as feature gaps or workarounds hint
  at missing functionality.
- **Review sites** — G2, Capterra, Product Hunt; read the "cons" and "what would
  you improve" sections.
- **Release note trackers** — sometimes "planned" or "won't fix" labels on
  release notes reveal demand.

For each surface found, record the URL and a one-line description of what it
covers.

### 3. Fan out research agents (parallel)

Spawn one subagent per surface or surface-bucket. Run them all at once (one
`Agent` call per surface in a single message). Give each subagent the surface
URL and this reporting contract:

> Scrape or search this surface for the **most-requested features** of
> \<product\>. Rank by demand signal: vote count, number of +1 reactions, thread
> length, or recurrence across posts. Return a structured list:
>
> - **Feature** — one-line description.
> - **Demand signal** — vote count / thread count / recurrence (be specific).
> - **Notes** — any context: workaround mentioned, partial implementation noted,
>   version requested.
>
> Return at most 20 items. Focus on feature *requests*, not bug reports.

Collect all subagent results before proceeding.

### 4. Filter and de-duplicate

Merge all findings into one list. Then:

- Remove features the current repo already ships (check against the local
  codebase or README).
- Merge overlapping requests (different phrasings of the same feature).
- Note when a feature appears across multiple surfaces — cross-surface
  recurrence is a stronger signal than a single high-vote thread.

### 5. Map to this repo

For each surviving item, note:

- **In scope?** Does this fit the current repo's domain and goals?
- **Which area?** Which part of the repo (module, workflow, config, docs) would
  this touch?
- **Effort estimate** — Low / Med / High, rough.

Skip items clearly outside scope; note them briefly so the user can override.

### 6. Report and optionally file issues

Present the ranked list (most-demanded first, after cross-surface weighting).
For each item include: feature description, demand signal summary, in-scope
verdict, area, and effort.

Then ask the user which items to file as GitHub issues. Do **not** file issues
without confirmation. When the user greenlights items, file them with
`gh issue create`, linking back to the source surface(s) in the body.

## Output format

1. **Surfaces found** — short table: surface type · URL · coverage notes.
2. **Ranked feature gap list** — one row per deduplicated feature:
   | # | Feature | Demand signal | In scope? | Area | Effort |
3. **Cross-surface hits** — call out any feature that appeared on 3+ surfaces;
   these are the strongest signals.
4. **Out-of-scope items** (brief) — so the user can override the filtering.
5. **Next step prompt** — ask which items to file as tracking issues.

## Anti-patterns

- Don't conflate bug reports with feature requests; bugs belong in a different
  queue.
- Don't inflate demand signals — report the actual vote/reaction counts, not
  impressions.
- Don't file issues without user confirmation (step 6).
- Don't skip the de-duplication pass — the same feature often appears on five
  surfaces under five names.
- Don't treat a competitor's "planned" roadmap item as a user demand; it's a
  supply signal, not a demand signal. Focus on what users asked for, not what
  the competitor announced.
