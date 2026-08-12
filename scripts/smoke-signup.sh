#!/bin/zsh
# Live smoke test for /api/signup against the DEPLOYED site (not local).
#
# Verifies: a NEW signup writes the roster row AND bumps count:signup by
# exactly 1; a REPEAT post of the same address does NOT double-count. Then
# cleans up after itself (deletes the test roster key, decrements the
# counter back) so it never pollutes the real signup numbers.
#
# Usage: scripts/smoke-signup.sh
# Exit 0 pass, 1 fail (state is restored either way if the failure happens
# after the write — see cleanup trap).
set -o pipefail

BASE="https://rvc-taxes.jeffpinto.com"
NS="55371b2ca075430faeeae249f9b036cc"
TS=$(date +%s)
EMAIL="smoke+${TS}@example.com"
KEY="signup:${EMAIL}"
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

# 1. New signup.
code=$(curl -s -o /tmp/smoke-signup-1.json -w '%{http_code}' -X POST "${BASE}/api/signup" \
  -H 'content-type: application/json' \
  -d "{\"email\":\"${EMAIL}\",\"name\":\"smoke test\",\"address\":\"\",\"source\":\"smoke-test\"}")
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

# (b) counter incremented by exactly 1.
after1=$(curl -s "${BASE}/api/count" | python3 -c 'import sys,json; print(json.load(sys.stdin)["signup"])')
expected=$((before + 1))
if [[ "${after1}" != "${expected}" ]]; then
  echo "FAIL: count:signup = ${after1}, expected ${expected}"; FAIL=1
else
  echo "PASS: count:signup incremented to ${after1}"
fi

# (c) repeat post of the same address does not double count.
curl -s -o /tmp/smoke-signup-2.json -X POST "${BASE}/api/signup" \
  -H 'content-type: application/json' \
  -d "{\"email\":\"${EMAIL}\",\"name\":\"smoke test repeat\",\"address\":\"\",\"source\":\"smoke-test-repeat\"}" >/dev/null
after2=$(curl -s "${BASE}/api/count" | python3 -c 'import sys,json; print(json.load(sys.stdin)["signup"])')
if [[ "${after2}" != "${expected}" ]]; then
  echo "FAIL: repeat signup changed count:signup to ${after2}, expected it to stay ${expected}"; FAIL=1
else
  echo "PASS: repeat signup did not double-count (still ${after2})"
fi

if [[ "${FAIL}" == "1" ]]; then
  echo "== smoke-signup: FAIL =="
  exit 1
fi
echo "== smoke-signup: PASS =="
exit 0
