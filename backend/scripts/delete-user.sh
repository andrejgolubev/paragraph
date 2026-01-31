#!/usr/bin/env bash
set -euo pipefail

USER_EMAIL="${1?USER_EMAIL required}"

API_KEY="${2?API key required}"
BASE_URL="${3:-https://api.paragraph-schedule.ru}"


printf 'deleting %s via %s\n' "$USER_EMAIL" "$BASE_URL"

curl --fail-with-body --retry 3 --retry-delay 2 --show-error \
  --request POST \
  -H "API-Key: ${API_KEY}" \
  "${BASE_URL}/admin/delete-user?user_email=${USER_EMAIL}"



