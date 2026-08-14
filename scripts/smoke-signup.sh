#!/bin/zsh
# Live smoke test for /api/signup against the DEPLOYED site (not local).
#
# Verifies: a consented signup writes an email-only roster row and bumps
# count:signup by exactly 1; the self-service deletion endpoint removes the
# row and restores the counter. A trap restores state if the check fails.
#
# Usage: scripts/smoke-signup.sh
# Exit 0 pass, 1 fail (state is restored either way if the failure happens
# after the write — see cleanup trap).
set -o pipefail

BASE="https://rvc-taxes.jeffpinto.com"
NS="55371b2ca075430faeeae249f9b036cc"
TS=$(date +%s)
EMAIL="smoke+${TS}@example.com"
KEY="signup:$(printf '%s' "${EMAIL}" | shasum -a 256 | awk '{print $1}')"
FAIL=0

echo "== smoke-signup: ${EMAIL} =="

before=$(curl -s "${BASE}/api/count" | python3 -c 'import sys,json; print(json.load(sys.stdin)["signup"])')
echo "count:signup before = ${before}"

cleanup() {
  echo "-- cleanup --"
  npx wrangler kv key delete "${KEY}" --namespace-id "${NS}" --remote >/dev/null 2>&1
  npx wrangler kv key put "count:signup" "${before}" --namespace-id "${NS}" --remote >/dev/null 2>&1
  after_cleanup=$(curl -s "${BASE}/api/count" | python3 -c 'import sys,json; print(json.load(sys.stdin)["signup"])')
  echo "count:signup restored to ${after_cleanup} (target ${before})"
  if [[ "${after_cleanup}" != "${before}" ]]; then
    echo "FAIL: cleanup did not restore the true counter value"
    exit 1
  fi
}
trap cleanup EXIT

# 1. New, explicitly consented signup.
code=$(curl -s -o /tmp/smoke-signup-1.json -w '%{http_code}' -X POST "${BASE}/api/signup" \
  -H "Origin: ${BASE}" \
  -H 'content-type: application/json' \
  -d "{\"email\":\"${EMAIL}\",\"consent\":true,\"source\":\"signup-strip:direct\"}")
if [[ "${code}" != "200" ]]; then
  echo "FAIL: signup POST returned ${code}"; FAIL=1
fi

# (a) roster key exists.
row=$(npx wrangler kv key get "${KEY}" --namespace-id "${NS}" --remote 2>/dev/null)
if [[ -z "${row}" ]]; then
  echo "FAIL: roster key ${KEY} not found in KV"; FAIL=1
else
  echo "PASS: roster key written: ${row}"
fi

# (a2) the roster contains only allowed update-list fields.
if ! printf '%s' "${row}" | python3 -c 'import json,sys; r=json.load(sys.stdin); bad=set(r)-{"email","source","consentAt","first","last"}; assert not bad, bad; assert r.get("email", "").startswith("smoke+")' 2>/dev/null; then
  echo "FAIL: signup row retained a disallowed field"; FAIL=1
else
  echo "PASS: roster row is email-only consent data"
fi

# (b) counter incremented by exactly 1.
after1=$(curl -s "${BASE}/api/count" | python3 -c 'import sys,json; print(json.load(sys.stdin)["signup"])')
expected=$((before + 1))
if [[ "${after1}" != "${expected}" ]]; then
  echo "FAIL: count:signup = ${after1}, expected ${expected}"; FAIL=1
else
  echo "PASS: count:signup incremented to ${after1}"
fi

# (c) self-service deletion removes the row and restores the active-signup count.
delete_code=$(curl -s -o /tmp/smoke-signup-2.json -w '%{http_code}' -X POST "${BASE}/api/unsubscribe" \
  -H "Origin: ${BASE}" \
  -H 'content-type: application/json' \
  -d "{\"email\":\"${EMAIL}\"}")
if [[ "${delete_code}" != "200" ]]; then
  echo "FAIL: unsubscribe POST returned ${delete_code}"; FAIL=1
fi
row_after_delete=$(npx wrangler kv key get "${KEY}" --namespace-id "${NS}" --remote 2>/dev/null)
after2=$(curl -s "${BASE}/api/count" | python3 -c 'import sys,json; print(json.load(sys.stdin)["signup"])')
if [[ -n "${row_after_delete}" ]]; then
  echo "FAIL: unsubscribe did not remove roster key ${KEY}"; FAIL=1
elif [[ "${after2}" != "${before}" ]]; then
  echo "FAIL: count:signup after deletion = ${after2}, expected ${before}"; FAIL=1
else
  echo "PASS: unsubscribe removed the row and restored count:signup to ${after2}"
fi

if [[ "${FAIL}" == "1" ]]; then
  echo "== smoke-signup: FAIL =="
  exit 1
fi
echo "== smoke-signup: PASS =="
exit 0
