---
name: deploy-verify-gotchas
description: Environment gotchas hit shipping the ledger-reframe PR (2026-07-20) — gh merge quirks with worktrees, and headless-Chrome hangs on live pages
metadata:
  type: feedback
---

Gotchas proven while shipping PR #8 (validation ledger reframe), 2026-07-20:

**If a `gh pr create` / `gh pr merge` call is denied by the permission system, that
is a declined action — stop and surface it to the main session / Jeff. Do NOT
switch to `gh api` or another tool to route around a denial.** (Transient "stage 2"
errors are different: those often clear on one retry of the same command.)

**`gh pr merge --squash --delete-branch` still deletes the REMOTE branch even when
it errors on the local checkout step** (main is held by the primary worktree) —
verify with `gh pr view N --json state` and `git ls-remote --heads origin`, don't
assume it failed.

**Headless Chrome hangs (~2min timeout, exit 143) screenshotting LIVE pages that load
Google Fonts; it still often writes the PNG before dying.** For a JS-injected element
(the nav label comes from nav.js), don't rely on a live screenshot — curl the deployed
asset and grep it: `curl -sL .../assets/nav.js | grep label`. A local `file://` render of
the source page works fine for layout. See [[rvc-taxes-project]].
