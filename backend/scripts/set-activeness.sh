#!/usr/bin/env bash
set -euo pipefail

USER_EMAIL="${1?user email required}"
USER_ACTIVENESS="${2?user activeness required}"

API_KEY="${3?API key required}"
BASE_URL="${4:-https://api.paragraph-schedule.ru}"

printf 'setting activeness for %s to %s via %s\n' "$USER_EMAIL" "$USER_ACTIVENESS" "$BASE_URL"

curl --fail-with-body --retry 3 --retry-delay 2 -L \
  --request PATCH \
  -H "API-Key: ${API_KEY}" \
  -w "\nHTTP %{http_code}\n" \
  --show-error \
  "${BASE_URL}/admin/set-user-activeness?user_email=${USER_EMAIL}&user_activeness=${USER_ACTIVENESS}"