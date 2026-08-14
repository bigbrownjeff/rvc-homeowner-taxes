# Handoff — Nassau coverage, public launch preparation, and source safety

**Date:** 2026-07-20 · **Project:** rvc-homeowner-taxes

## Goal

Extend the site from a local brief to a source-backed Nassau address tool, make
the facts ledger the single public source of truth, and prepare a public launch
without putting recipient-specific campaign operations in source control.

## What shipped

- **Facts ledger:** `site/validation.html` anchors each material claim to a
  source, verified date, and used-on pages. Update the ledger first, then
  propagate changes through the listed surfaces.
- **Redesign and action kit:** the site gained a consistent civic design system,
  address lookup, official public-action paths, and a working opt-in backend.
- **Nassau coverage:** district data and provenance were expanded through a
  pilot-then-fan-out method. The public coverage page states known gaps rather
  than presenting incomplete data as complete.
- **Official-attribution correction:** a public legislative attribution was
  corrected in the ledger and related materials after primary-source review.
  Do not reuse historical outreach wording or recipient assumptions.
- **Public-outreach plan:** messages were organized into a private preparation
  phase and a public communication phase. Recipient names, contact routes,
  direct-draft copy, send status, and replies have been removed from this
  repository.
- **Accuracy monitoring:** a recurring check compares live public claims with
  the facts ledger. It must continue after launch and alert on discrepancies.

## What worked

- Start with a small representative data pilot, write reusable methods, then
  fan out independent batches and integrate deliberately.
- Treat the ledger as a contract: a trusted primary source and a verified date
  are required before a claim travels to another page or artifact.
- Run independent review before merge and perform a fresh live verification
  after deployment.
- Use the coverage page to explain scope, uncertainty, and gaps plainly.

## What did not work

- A fact can propagate quickly when its source record is wrong. Verify public
  officeholder and bill-attribution claims directly at the authoritative source
  before publishing.
- Local agent scratch and recipient-specific campaign operations do not belong
  in a tracked repository. Do not force-add ignored material.
- Direct-contact work requires an owner-authorized messaging environment and a
  current operational record; a source checkout is not either of those.

## Key decisions

- Keep geographic scope explicit and present honest fallbacks for locations
  outside the supported coverage.
- Prefer a web-native, print-ready brief to a duplicate presentation artifact.
- Do not make cash-back promises where the supporting public data is not
  available.
- Consider external sources or amplifiers only through a nonpartisan,
  senior-protective lens. Never present support without explicit written
  permission and approved wording.

## How to reproduce safely

- Start with the current [facts and sources page](https://rvc-taxes.jeffpinto.com/validation).
- Read `site/assets/districts.json` and its provenance before changing coverage.
- Run `SWEEP_DRY=1 scripts/daily_posture_sweep.sh` for a side-effect-free
  monitoring rehearsal.
- Run `scripts/check_pdf_drift.sh` before releasing a generated public brief.
- Deploy only from a reviewed release head, then verify the live site with
  cache-aware checks.

## Open work

1. Re-verify changing public facts and official routes at time of use.
2. Continue closing data-coverage gaps only when a primary source supports the
   new value.
3. Keep public outreach copy in approved current artifacts. Direct outreach
   requires owner approval and must use the authorized operational record.
4. Continue the daily accuracy monitor after launch; never retire it solely
   because the initial launch window has passed.

## Historical engineering notes retained

- The address tool uses a public geocoder with JSONP because the service does
  not provide the required CORS headers. It must not retain visitor addresses.
- District-rate coverage used a small pilot, reusable source methods, and
  parallel source-specific batches. Parcel-level jurisdiction checks are the
  guardrail against assigning a rate from the wrong district.
- The data model distinguishes a published exemption-program count from an
  unavailable turnover-oriented measure. Do not substitute one for the other.
- Custom-domain propagation can lag a deployment, and edge caches can preserve
  a pre-deploy miss. Verify new assets with cache-aware checks before diagnosing
  a release failure.
- Keep calculation code byte-stable through visual or copy-only redesigns. A
  diff of script blocks is an effective release check when no logic change was
  requested.
- The print briefing is a rendered web artifact. Preserve its drift gate rather
  than reintroducing a parallel presentation source with its own stale figures.
