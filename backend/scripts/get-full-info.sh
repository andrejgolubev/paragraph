#!/usr/bin/env bash
set -euo pipefail

USER_EMAIL="${1?user email required}"
API_KEY="${2?API key required}"
BASE_URL="${3:-https://api.paragraph-schedule.ru}"

printf 'querying %s for %s\n' "$BASE_URL" "$USER_EMAIL"

curl --fail-with-body --retry 3 --retry-delay 2 -L \
  -H "API-Key: ${API_KEY}" \
  -w "\nHTTP %{http_code}\n" \
  --show-error \
  "${BASE_URL}/admin/get-full-info/?user_email=${USER_EMAIL}"


