---
name: scratch-stays-local
description: Jeff's global gitignore excludes .claude/scratch/ and .claude/agent-memory/; do not force-add them to a repo
metadata:
  type: feedback
---

`~/.gitignore_global` excludes `**/.claude/scratch/`, `**/.claude/agent-memory/`,
`**/.claude/worktrees/`, and `.worktrees/` under the comment *"Agent scratch that belongs to
the machine, not the repo."* Do not `git add -f` past it.

**Why:** on 2026-07-24 the estate hygiene rollup flagged rvc-homeowner-taxes for a dirty main
checkout. The untracked items were `.worktrees/` and a 399-line scratch build plan. Mid-session
(21:43) a concurrent session added both patterns to the global ignore, and the tree went clean
on its own. Committing the plan doc would have fought a policy Jeff had just reaffirmed that
hour.

**How to apply:** when a hygiene sweep reports a dirty tree, re-run `git status` and
`git check-ignore -v <path>` before acting — the flag may already be resolved, and another
session may have changed policy underneath you. Report what the dirty changes actually were
before committing or discarding either way.

Note the historical asymmetry in rvc-homeowner-taxes: some `.claude/scratch/` material was
force-added before the policy existed. Recipient-specific outreach content has since been
removed from the current head. Only public-safe templates may remain tracked; never restore or
add recipient drafts, contact details, routing, mailbox state, send logs, or private-resident
material.

Because `~/.gitignore_global` is machine-local and does not travel with a repo, genuinely
repo-wide patterns (`.worktrees/`, `__pycache__/`) still belong in the repo's own `.gitignore`.
