#!/bin/zsh
# Live smoke test for /api/signup against the DEPLOYED site (not local).
#
# Verifies: a consented signup writes an email-only roster row and bumps
# count:signup by exactly 1; the self-service deletion endpoint removes the
# row and restores the counter. Cloudflare KV is eventually consistent, so
# every verification is a bounded read-only poll. POST requests are made once
# each and are never retried.
#
# Usage: scripts/smoke-signup.sh
# Optional tuning: SMOKE_POLL_MAX_SECONDS=120 SMOKE_POLL_INTERVAL_SECONDS=3
#                  SMOKE_CURL_CONNECT_TIMEOUT=10 SMOKE_CURL_MAX_TIME=30
#                  SMOKE_WRANGLER_MAX_TIME=30
# Exit 0 pass, 1 fail. A trap makes one cleanup attempt if the test is
# interrupted after the signup request.
set -o pipefail

BASE="${SMOKE_BASE:-https://rvc-taxes.jeffpinto.com}"
NS="${SMOKE_KV_NAMESPACE_ID:-55371b2ca075430faeeae249f9b036cc}"
POLL_MAX_SECONDS="${SMOKE_POLL_MAX_SECONDS:-120}"
POLL_INTERVAL_SECONDS="${SMOKE_POLL_INTERVAL_SECONDS:-3}"
CURL_CONNECT_TIMEOUT="${SMOKE_CURL_CONNECT_TIMEOUT:-10}"
CURL_MAX_TIME="${SMOKE_CURL_MAX_TIME:-30}"
WRANGLER_MAX_TIME="${SMOKE_WRANGLER_MAX_TIME:-30}"
TS=$(date +%s)
EMAIL="smoke+${TS}@example.com"
KEY="signup:$(printf '%s' "${EMAIL}" | shasum -a 256 | awk '{print $1}')"
TMP_DIR=$(mktemp -d "${TMPDIR:-/tmp}/rvc-smoke-signup.XXXXXX") || exit 1

FAIL=0
before=""
expected=""
cleanup_pending=0
signup_post_attempted=0
unsubscribe_post_attempted=0
REMOTE_KEY_STATE=""
REMOTE_KEY_ERROR=""
REMOTE_SIGNUP_ROW=""
API_SIGNUP_COUNT=""
API_COUNT_ERROR=""
POST_CODE=""
POST_ERROR=""

require_positive_integer() {
  if [[ ! "$2" =~ '^[1-9][0-9]*$' ]]; then
    echo "FAIL: $1 must be a positive integer (got '$2')" >&2
    exit 2
  fi
}

require_positive_integer "SMOKE_POLL_MAX_SECONDS" "${POLL_MAX_SECONDS}"
require_positive_integer "SMOKE_POLL_INTERVAL_SECONDS" "${POLL_INTERVAL_SECONDS}"
require_positive_integer "SMOKE_CURL_CONNECT_TIMEOUT" "${CURL_CONNECT_TIMEOUT}"
require_positive_integer "SMOKE_CURL_MAX_TIME" "${CURL_MAX_TIME}"
require_positive_integer "SMOKE_WRANGLER_MAX_TIME" "${WRANGLER_MAX_TIME}"

echo "== smoke-signup: ${EMAIL} =="
echo "polling remote reads for up to ${POLL_MAX_SECONDS}s every ${POLL_INTERVAL_SECONDS}s"

# Python is already required below for JSON validation. Its subprocess timeout
# gives the otherwise unbounded Wrangler commands an explicit wall-clock cap.
run_with_timeout() {
  local seconds="$1"
  shift
  python3 -c '
import subprocess
import sys

try:
    completed = subprocess.run(sys.argv[2:], timeout=int(sys.argv[1]))
except subprocess.TimeoutExpired:
    print(f"command timed out after {sys.argv[1]} seconds", file=sys.stderr)
    raise SystemExit(124)
raise SystemExit(completed.returncode)
' "${seconds}" "$@"
}

bounded_timeout() {
  local configured="$1"
  local remaining="$2"
  if (( configured > remaining )); then
    print "${remaining}"
  else
    print "${configured}"
  fi
}

# List, rather than get, is how the test distinguishes a known missing key
# (a successful JSON [] response) from Wrangler authentication/network errors.
read_remote_key_state() {
  local max_time="${1:-${WRANGLER_MAX_TIME}}"
  local output="${TMP_DIR}/key-list.json"
  local error="${TMP_DIR}/key-list.err"
  local parse_error="${TMP_DIR}/key-list-parse.err"
  local rc state

  REMOTE_KEY_STATE=""
  REMOTE_KEY_ERROR=""
  run_with_timeout "${max_time}" npx wrangler kv key list --prefix "${KEY}" --namespace-id "${NS}" --remote >"${output}" 2>"${error}"
  rc=$?
  if (( rc != 0 )); then
    REMOTE_KEY_ERROR=$(<"${error}")
    return 1
  fi

  state=$(python3 -c '
import json
import sys

key = sys.argv[1]
rows = json.load(sys.stdin)
if not isinstance(rows, list):
    raise ValueError("Wrangler key-list response was not a JSON array")
print("present" if any(isinstance(row, dict) and row.get("name") == key for row in rows) else "missing")
' "${KEY}" <"${output}" 2>"${parse_error}")
  rc=$?
  if (( rc != 0 )) || [[ "${state}" != "present" && "${state}" != "missing" ]]; then
    REMOTE_KEY_ERROR=$(<"${parse_error}")
    [[ -n "${REMOTE_KEY_ERROR}" ]] || REMOTE_KEY_ERROR="unexpected Wrangler key-list output"
    return 1
  fi

  REMOTE_KEY_STATE="${state}"
  return 0
}

read_remote_signup_row() {
  local max_time="${1:-${WRANGLER_MAX_TIME}}"
  local output="${TMP_DIR}/key-get.txt"
  local error="${TMP_DIR}/key-get.err"
  local rc

  REMOTE_SIGNUP_ROW=""
  run_with_timeout "${max_time}" npx wrangler kv key get "${KEY}" --namespace-id "${NS}" --remote --text >"${output}" 2>"${error}"
  rc=$?
  if (( rc != 0 )); then
    REMOTE_KEY_ERROR=$(<"${error}")
    return 1
  fi
  REMOTE_SIGNUP_ROW=$(<"${output}")
  if [[ -z "${REMOTE_SIGNUP_ROW}" ]]; then
    REMOTE_KEY_ERROR="Wrangler reported the key but returned an empty roster row"
    return 1
  fi
  return 0
}

read_api_signup_count() {
  local max_time="${1:-${CURL_MAX_TIME}}"
  local output="${TMP_DIR}/count.json"
  local error="${TMP_DIR}/count.err"
  local parse_error="${TMP_DIR}/count-parse.err"
  local rc count

  API_SIGNUP_COUNT=""
  API_COUNT_ERROR=""
  local connect_time="${CURL_CONNECT_TIMEOUT}"
  if (( connect_time > max_time )); then connect_time="${max_time}"; fi
  curl --silent --show-error --fail --retry 0 \
    --connect-timeout "${connect_time}" --max-time "${max_time}" \
    "${BASE}/api/count" >"${output}" 2>"${error}"
  rc=$?
  if (( rc != 0 )); then
    API_COUNT_ERROR=$(<"${error}")
    return 1
  fi

  count=$(python3 -c '
import json
import sys

value = json.load(sys.stdin)["signup"]
if not isinstance(value, int) or value < 0:
    raise ValueError("signup count was not a non-negative integer")
print(value)
' <"${output}" 2>"${parse_error}")
  rc=$?
  if (( rc != 0 )); then
    API_COUNT_ERROR=$(<"${parse_error}")
    return 1
  fi
  API_SIGNUP_COUNT="${count}"
  return 0
}

# This makes exactly one HTTP POST. Curl retry is explicitly disabled; callers
# may poll only the corresponding remote reads after this returns.
post_json_once() {
  local endpoint="$1"
  local body="$2"
  local output="$3"
  local error="${output}.err"
  local rc

  POST_CODE=""
  POST_ERROR=""
  POST_CODE=$(curl --silent --show-error --retry 0 \
    --connect-timeout "${CURL_CONNECT_TIMEOUT}" --max-time "${CURL_MAX_TIME}" \
    --output "${output}" --write-out '%{http_code}' --request POST "${BASE}${endpoint}" \
    -H "Origin: ${BASE}" \
    -H 'content-type: application/json' \
    --data "${body}" 2>"${error}")
  rc=$?
  if (( rc != 0 )); then
    POST_ERROR=$(<"${error}")
    return 1
  fi
  return 0
}

# Return 0 when both read-only observations converge, 1 on a bounded mismatch,
# and 2 on a Wrangler/curl/auth/network/parse error. The latter must never be
# reinterpreted as a missing key.
wait_for_state() {
  local wanted_key_state="$1"
  local wanted_count="$2"
  local label="$3"
  local started deadline elapsed remaining sleep_for key_timeout count_timeout

  started=$(date +%s)
  deadline=$(( started + POLL_MAX_SECONDS ))
  while true; do
    remaining=$(( deadline - $(date +%s) ))
    if (( remaining <= 0 )); then
      echo "FAIL: ${label}: timed out after ${POLL_MAX_SECONDS}s before the next remote read" >&2
      return 1
    fi
    key_timeout=$(bounded_timeout "${WRANGLER_MAX_TIME}" "${remaining}")
    if ! read_remote_key_state "${key_timeout}"; then
      echo "ERROR: ${label}: cannot read remote key state: ${REMOTE_KEY_ERROR}" >&2
      return 2
    fi
    remaining=$(( deadline - $(date +%s) ))
    if (( remaining <= 0 )); then
      echo "FAIL: ${label}: timed out after ${POLL_MAX_SECONDS}s before the count read" >&2
      return 1
    fi
    count_timeout=$(bounded_timeout "${CURL_MAX_TIME}" "${remaining}")
    if ! read_api_signup_count "${count_timeout}"; then
      echo "ERROR: ${label}: cannot read /api/count: ${API_COUNT_ERROR}" >&2
      return 2
    fi
    elapsed=$(( $(date +%s) - started ))
    if (( elapsed > POLL_MAX_SECONDS )); then
      echo "FAIL: ${label}: timed out after ${elapsed}s" >&2
      return 1
    fi
    if [[ "${REMOTE_KEY_STATE}" == "${wanted_key_state}" && "${API_SIGNUP_COUNT}" == "${wanted_count}" ]]; then
      echo "PASS: ${label}: key is ${REMOTE_KEY_STATE}; count:signup is ${API_SIGNUP_COUNT}"
      return 0
    fi

    if (( elapsed >= POLL_MAX_SECONDS )); then
      echo "FAIL: ${label}: timed out after ${elapsed}s (key ${REMOTE_KEY_STATE}, count ${API_SIGNUP_COUNT}; expected ${wanted_key_state}, ${wanted_count})" >&2
      return 1
    fi
    remaining=$(( POLL_MAX_SECONDS - elapsed ))
    sleep_for=${POLL_INTERVAL_SECONDS}
    if (( sleep_for > remaining )); then sleep_for=${remaining}; fi
    echo "waiting: ${label}: key ${REMOTE_KEY_STATE}, count ${API_SIGNUP_COUNT}; retrying in ${sleep_for}s"
    sleep "${sleep_for}"
  done
}

wait_for_signup_row() {
  local started deadline elapsed remaining sleep_for key_timeout row_timeout

  started=$(date +%s)
  deadline=$(( started + POLL_MAX_SECONDS ))
  while true; do
    remaining=$(( deadline - $(date +%s) ))
    if (( remaining <= 0 )); then
      echo "FAIL: roster row: timed out after ${POLL_MAX_SECONDS}s before the next remote read" >&2
      return 1
    fi
    key_timeout=$(bounded_timeout "${WRANGLER_MAX_TIME}" "${remaining}")
    if ! read_remote_key_state "${key_timeout}"; then
      echo "ERROR: roster row: cannot read remote key state: ${REMOTE_KEY_ERROR}" >&2
      return 2
    fi
    if [[ "${REMOTE_KEY_STATE}" == "present" ]]; then
      remaining=$(( deadline - $(date +%s) ))
      if (( remaining <= 0 )); then
        echo "FAIL: roster row: timed out after ${POLL_MAX_SECONDS}s before reading the row" >&2
        return 1
      fi
      row_timeout=$(bounded_timeout "${WRANGLER_MAX_TIME}" "${remaining}")
      if read_remote_signup_row "${row_timeout}"; then
        return 0
      fi
    fi

    elapsed=$(( $(date +%s) - started ))
    if (( elapsed >= POLL_MAX_SECONDS )); then
      echo "FAIL: roster row: timed out after ${elapsed}s (state ${REMOTE_KEY_STATE}; ${REMOTE_KEY_ERROR})" >&2
      return 1
    fi
    remaining=$(( POLL_MAX_SECONDS - elapsed ))
    sleep_for=${POLL_INTERVAL_SECONDS}
    if (( sleep_for > remaining )); then sleep_for=${remaining}; fi
    echo "waiting: roster row state is ${REMOTE_KEY_STATE}; retrying in ${sleep_for}s"
    sleep "${sleep_for}"
  done
}

direct_cleanup_fallback() {
  local error="${TMP_DIR}/cleanup.err"
  local rc

  # The normal path uses the worker's single unsubscribe POST. Only after a
  # bounded read mismatch do we touch KV directly. We may remove the uniquely
  # named test row, but never overwrite the public tally: KV has no
  # compare-and-set, so even a just-read value can be stale or change under us.
  if ! read_remote_key_state; then
    echo "ERROR: cleanup fallback: cannot read remote key state: ${REMOTE_KEY_ERROR}" >&2
    return 1
  fi
  if [[ "${REMOTE_KEY_STATE}" != "present" ]]; then
    echo "ERROR: cleanup fallback: key is already absent; refusing to rewrite a divergent counter" >&2
    return 1
  fi
  # The unique smoke row is safe to remove even if the aggregate counter has
  # diverged. The tally itself is never changed by this fallback.
  run_with_timeout "${WRANGLER_MAX_TIME}" npx wrangler kv key delete "${KEY}" --namespace-id "${NS}" --remote >/dev/null 2>"${error}"
  rc=$?
  if (( rc != 0 )); then
    echo "ERROR: cleanup fallback: direct key delete failed: $(<"${error}")" >&2
    return 1
  fi

  if ! read_api_signup_count; then
    echo "ERROR: cleanup fallback: test row was removed but /api/count cannot be read: ${API_COUNT_ERROR}" >&2
    return 1
  fi
  if [[ "${API_SIGNUP_COUNT}" == "${before}" ]]; then
    echo "cleanup fallback: test row was removed and count has returned to baseline"
    return 0
  fi
  if [[ "${API_SIGNUP_COUNT}" != "${expected}" ]]; then
    echo "ERROR: cleanup fallback: test row was removed; count is ${API_SIGNUP_COUNT}, not baseline ${before}. Investigate the aggregate tally manually." >&2
    return 1
  fi
  echo "ERROR: cleanup fallback: test row was removed but count is still ${expected}; refusing to overwrite a shared eventually-consistent counter. Restore it manually if it does not converge." >&2
  return 1
}

cleanup() {
  local original_rc=$?
  local wait_rc

  trap - EXIT
  if (( cleanup_pending )); then
    echo "-- cleanup --"
    # If the regular unsubscribe was never attempted, this is its single
    # cleanup request. If it was attempted already, do not POST again.
    if (( unsubscribe_post_attempted == 0 )); then
      unsubscribe_post_attempted=1
      if post_json_once "/api/unsubscribe" "{\"email\":\"${EMAIL}\"}" "${TMP_DIR}/cleanup-unsubscribe.json"; then
        if [[ "${POST_CODE}" != "200" ]]; then
          echo "ERROR: cleanup unsubscribe returned ${POST_CODE}" >&2
        fi
      else
        echo "ERROR: cleanup unsubscribe transport failure: ${POST_ERROR}" >&2
      fi
    fi

    if [[ -n "${before}" && -n "${expected}" ]]; then
      wait_for_state "missing" "${before}" "cleanup verification"
      wait_rc=$?
      if (( wait_rc == 1 )); then
        direct_cleanup_fallback || echo "ERROR: cleanup fallback could not safely restore state; investigate ${KEY}" >&2
      elif (( wait_rc == 2 )); then
        echo "ERROR: cleanup verification failed to read remote state; no direct mutation attempted" >&2
      fi
    fi
  fi
  rm -rf "${TMP_DIR}"
  return "${original_rc}"
}
trap cleanup EXIT

if ! read_api_signup_count; then
  echo "FAIL: cannot read baseline /api/count: ${API_COUNT_ERROR}" >&2
  exit 1
fi
before="${API_SIGNUP_COUNT}"
expected=$(( before + 1 ))
echo "count:signup before = ${before}"

# 1. New, explicitly consented signup. This request is sent exactly once.
cleanup_pending=1
signup_post_attempted=1
if post_json_once "/api/signup" "{\"email\":\"${EMAIL}\",\"consent\":true,\"source\":\"signup-strip:direct\"}" "${TMP_DIR}/signup.json"; then
  if [[ "${POST_CODE}" != "200" ]]; then
    echo "FAIL: signup POST returned ${POST_CODE}"; FAIL=1
  fi
else
  echo "FAIL: signup POST transport failure: ${POST_ERROR}"; FAIL=1
fi

if [[ "${POST_CODE}" == "200" ]]; then
  if ! wait_for_state "present" "${expected}" "signup verification"; then FAIL=1; fi
  if wait_for_signup_row; then
    echo "PASS: roster row written"
    if ! printf '%s' "${REMOTE_SIGNUP_ROW}" | python3 -c 'import json,sys; r=json.load(sys.stdin); bad=set(r)-{"email","source","consentAt","first","last"}; assert not bad, bad; assert r.get("email", "").startswith("smoke+")' 2>/dev/null; then
      echo "FAIL: signup row retained a disallowed field"; FAIL=1
    else
      echo "PASS: roster row is email-only consent data"
    fi
  else
    FAIL=1
  fi
else
  echo "SKIP: signup verification after an unsuccessful or indeterminate POST"
fi

# 2. Self-service deletion. This is the one and only unsubscribe POST; all
# subsequent checks are read-only polls.
unsubscribe_post_attempted=1
if post_json_once "/api/unsubscribe" "{\"email\":\"${EMAIL}\"}" "${TMP_DIR}/unsubscribe.json"; then
  if [[ "${POST_CODE}" != "200" ]]; then
    echo "FAIL: unsubscribe POST returned ${POST_CODE}"; FAIL=1
  fi
else
  echo "FAIL: unsubscribe POST transport failure: ${POST_ERROR}"; FAIL=1
fi
if ! wait_for_state "missing" "${before}" "unsubscribe verification"; then FAIL=1; fi

if [[ "${FAIL}" == "1" ]]; then
  echo "== smoke-signup: FAIL =="
  exit 1
fi

cleanup_pending=0
trap - EXIT
rm -rf "${TMP_DIR}"
echo "== smoke-signup: PASS =="
exit 0
