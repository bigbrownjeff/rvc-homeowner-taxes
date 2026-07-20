---
name: fanout-checkout-discipline
description: Parallel fan-out agents twice left the primary checkout on their feature branch (2026-07-20) — coordinator must verify HEAD after every agent completes
metadata:
  type: feedback
---

During the 4-agent districts fan-out (2026-07-20), two agents worked in the PRIMARY
checkout (~/Projects/rvc-homeowner-taxes) instead of a worktree, leaving HEAD on
their feature branch. Symptom at the coordinator: `git pull --ff-only` fails with
"diverging branches" while `origin/main..main` looks empty (you are diffing main,
but HEAD is elsewhere).

**Why:** worktree instructions in the prompt are not reliably followed under long
multi-step tasks; the agent's first `git checkout -b` happens wherever it starts.

**How to apply:**
- Coordinator: after EVERY parallel agent completes, run `git branch --show-current`
  in the primary checkout before any merge/pull; restore with `git checkout main`.
- Prompts: tell agents their FIRST command must be `git worktree add <path> -b <branch>
  origin/main` and that they must never run checkout/commit in ~/Projects/rvc-homeowner-taxes.
- Stale-base hazard compounds this: batch PRs cut before earlier merges will DELETE
  other batches' files on squash-merge — check `git diff --name-only origin/main <branch>`
  shows ONLY the agent's own files; rebase otherwise (bit PRs #11 and #16 today).
