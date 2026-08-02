#!/bin/zsh
# Is site/RVC_Briefing_8pager.pdf still a faithful render of site/deck.html?
#
# The PDF is a snapshot artifact. Edit the deck, forget to re-render, and the site
# hands legislators a stale handout while the live page shows corrected figures.
# Nothing else catches that: the PDF stays a valid 200 forever.
#
# WHY NOT A BYTE DIFF. Chrome stamps /CreationDate and a fresh /ID into every render,
# so two renders of an UNCHANGED deck differ in every byte (verified 2026-08-02:
# 6ad2f810... vs 5d04174d... from identical input). A byte comparison would fire
# every single run. Extracted TEXT is deterministic (same input -> same sha256), so
# that is what we compare. It catches the drift that matters: changed figures, names,
# dates, copy. It does not catch pure styling drift, which is the right trade.
#
#   scripts/check_pdf_drift.sh          check only; exit 0 clean, 1 drift, 2 cannot check
#   scripts/check_pdf_drift.sh --fix    re-render the committed PDF in place
#
# Run before every deploy (see DEPLOY.md) and daily from daily_posture_sweep.sh.
# zsh-safe: null-glob (N) on any glob; no use of the reserved $status.
set -o pipefail

REPO="${0:A:h:h}"
DECK="$REPO/site/deck.html"
PDF="$REPO/site/RVC_Briefing_8pager.pdf"
HTML2PDF="$HOME/.claude/bin/html2pdf"
FIX=0
[[ "${1:-}" == "--fix" ]] && FIX=1

# A check that cannot run must be loud, never a silent pass.
for f in "$DECK" "$PDF"; do
  [[ -f "$f" ]] || { echo "check_pdf_drift: missing $f" >&2; exit 2 }
done
[[ -x "$HTML2PDF" ]] || { echo "check_pdf_drift: no html2pdf at $HTML2PDF" >&2; exit 2 }
command -v pdftotext >/dev/null || {
  echo "check_pdf_drift: pdftotext not found (brew install poppler)" >&2; exit 2
}

TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT

"$HTML2PDF" "$DECK" "$TMP/fresh.pdf" >/dev/null 2>&1 || {
  echo "check_pdf_drift: render failed for $DECK" >&2; exit 2
}

pdftotext -layout "$TMP/fresh.pdf" "$TMP/fresh.txt" 2>/dev/null || { echo "check_pdf_drift: pdftotext failed on the fresh render" >&2; exit 2 }
pdftotext -layout "$PDF" "$TMP/committed.txt" 2>/dev/null || { echo "check_pdf_drift: pdftotext failed on $PDF" >&2; exit 2 }

if diff -q "$TMP/committed.txt" "$TMP/fresh.txt" >/dev/null; then
  echo "PDF current: RVC_Briefing_8pager.pdf matches deck.html"
  exit 0
fi

CHANGED="$(diff "$TMP/committed.txt" "$TMP/fresh.txt" | grep -cE '^[<>]')"
echo "PDF DRIFT: deck.html has changed since RVC_Briefing_8pager.pdf was rendered ($CHANGED text lines differ)"
diff "$TMP/committed.txt" "$TMP/fresh.txt" | grep -E '^[<>]' | head -12

if (( FIX )); then
  cp "$TMP/fresh.pdf" "$PDF"
  echo "re-rendered $PDF; commit it"
  exit 0
fi

echo "fix: scripts/check_pdf_drift.sh --fix   then commit site/RVC_Briefing_8pager.pdf"
exit 1
